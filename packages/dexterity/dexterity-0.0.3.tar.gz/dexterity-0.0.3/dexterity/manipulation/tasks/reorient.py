"""Tasks involving in-hand object re-orientation."""

import collections
import dataclasses
from typing import Dict, Optional

import numpy as np
from dm_control import composer
from dm_control import mjcf
from dm_control.composer import initializers
from dm_control.composer.observation import observable
from dm_control.composer.variation import distributions
from dm_control.composer.variation import rotations
from dm_control.utils import containers
from dm_control.utils import rewards as reward_utils
from dm_robotics.transformations import transformations as tr

from dexterity import effector
from dexterity import effectors
from dexterity import task
from dexterity.manipulation import arenas
from dexterity.manipulation import props
from dexterity.manipulation.shared import cameras
from dexterity.manipulation.shared import constants
from dexterity.manipulation.shared import observations
from dexterity.manipulation.shared import rewards
from dexterity.manipulation.shared import tags
from dexterity.manipulation.shared import workspaces
from dexterity.models.hands import fingered_hand
from dexterity.models.hands import shadow_hand_e
from dexterity.utils import geometry_utils
from dexterity.utils import mujoco_collisions


@dataclasses.dataclass(frozen=True)
class Workspace:
    prop_bbox: workspaces.BoundingBox


# The position of the hand relative in the world frame, in meters.
_HAND_POS = (0, 0.2, 0.1)
# The orientation of the hand relative to the world frame.
_HAND_QUAT = tr.axisangle_to_quat(
    np.pi * np.array([0, np.sqrt(2) / 2, -np.sqrt(2) / 2])
)

# Alpha value of the visual goal hint.
_HINT_ALPHA = 0.4
# Position of the hint in the world frame, in meters.
_HINT_POS = (0.12, 0.0, 0.15)

# Size of the prop, in meters.
_PROP_SIZE = 0.02

# Fudge factor for taking the inverse of the orientation error, in radians.
_ORIENTATION_EPS = 0.1
# Threshold for successful orientation, in radians.
_ORIENTATION_THRESHOLD = 0.1
# Reward shaping coefficients.
_ORIENTATION_WEIGHT = 1.0
_SUCCESS_BONUS_WEIGHT = 800.0
_ACTION_SMOOTHING_WEIGHT = -0.1  # NOTE(kevin): negative sign.

# Timestep of the physics simulation.
_PHYSICS_TIMESTEP: float = 0.005

# Interval between agent actions, in seconds.
_CONTROL_TIMESTEP: float = 0.025

# Maximum number of steps per episode.
_STEP_LIMIT: int = 300

_BBOX_SIZE = 0.05
_WORKSPACE = Workspace(
    prop_bbox=workspaces.BoundingBox(
        lower=(-_BBOX_SIZE / 2, -0.13 - _BBOX_SIZE / 2, 0.16),
        upper=(+_BBOX_SIZE / 2, -0.13 + _BBOX_SIZE / 2, 0.16),
    ),
)

# Observable settings.
_FREEPROP_OBSERVABLES = observations.ObservableNames(
    prop_pose=("position", "orientation", "linear_velocity", "angular_velocity"),
)
_TARGETPROP_OBSERVABLES = observations.ObservableNames(
    prop_pose=("orientation",),
)

SUITE = containers.TaggedTasks()


class ReOrient(task.Task):
    """Manipulate an object to a goal orientation."""

    def __init__(
        self,
        arena: composer.Arena,
        hand: fingered_hand.FingeredHand,
        hand_effector: effector.Effector,
        observable_settings: observations.ObservationSettings,
        workspace: Workspace = _WORKSPACE,
        restrict_orientation: bool = False,
        fall_termination: bool = True,
        control_timestep: float = _CONTROL_TIMESTEP,
        physics_timestep: float = _PHYSICS_TIMESTEP,
    ) -> None:
        """Construct a new `ReOrient` task.

        Args:
            arena: The arena to use.
            hand: The hand to use.
            hand_effector: The effector to use for the hand.
            observable_settings: The observation settings to use.
            workspace: The workspace to use.
            restrict_orientation: If True, the goal orientation is restricted about the
                Z-axis. Otherwise, it is fully sampled from SO(3).
            fall_termination: Whether to terminate if the prop falls off the hand and
                onto the ground.
            control_timestep: The control timestep, in seconds.
            physics_timestep: The physics timestep, in seconds.
        """
        super().__init__(arena=arena, hand=hand, hand_effector=hand_effector)

        # Attach the hand to the arena.
        self._arena.attach_offset(hand, position=_HAND_POS, quaternion=_HAND_QUAT)

        # Add prop.
        prop_obs_options = observations.make_options(
            observable_settings, _FREEPROP_OBSERVABLES
        )
        self._prop = props.OpenAICube(
            size=_PROP_SIZE, observable_options=prop_obs_options, name="prop"
        )
        arena.add_free_entity(self._prop)

        # Translucent, contactless prop with no observables. This is used to provide a
        # visual hint of the goal state.
        target_prop_obs_options = observations.make_options(
            observable_settings, _TARGETPROP_OBSERVABLES
        )
        self._hint_prop = props.OpenAICube(
            size=_PROP_SIZE,
            observable_options=target_prop_obs_options,
            name="target_prop",
        )
        _hintify(self._hint_prop, _HINT_ALPHA)
        arena.attach_offset(self._hint_prop, position=_HINT_POS)

        # Place the prop slightly above the hand.
        self._prop_placer = initializers.PropPlacer(
            props=[self._prop],
            position=distributions.Uniform(
                workspace.prop_bbox.lower,
                workspace.prop_bbox.upper,
            ),
            quaternion=rotations.UniformQuaternion(),
            settle_physics=False,
        )
        if restrict_orientation:
            self._prop_orientation_sampler = workspaces.uniform_z_rotation
        else:
            self._prop_orientation_sampler = rotations.UniformQuaternion()

        # Add custom cameras obserbables.
        self._task_observables = cameras.add_camera_observables(
            arena,
            observable_settings,
            cameras.FRONT_CLOSE,
            cameras.TOP_DOWN,
            cameras.LEFT_CLOSE,
            cameras.RIGHT_CLOSE,
        )

        # Add angular difference between prop and target prop as an observable.
        angular_diff_observable = observable.Generic(self._get_quaternion_difference)
        angular_diff_observable.configure(
            **dataclasses.asdict(observable_settings.prop_pose)
        )
        self._task_observables["angular_difference"] = angular_diff_observable

        # Add action taken at the previous timestep as an observable.
        self._action_observable = observable.Generic(self._get_action)
        self._action_observable.configure(
            **dataclasses.asdict(observable_settings.proprio)
        )
        self._task_observables["action"] = self._action_observable

        self.set_timesteps(
            control_timestep=control_timestep,
            physics_timestep=physics_timestep,
        )

        # Visual debugging.
        workspaces.add_bbox_site(
            body=self.root_entity.mjcf_model.worldbody,
            lower=workspace.prop_bbox.lower,
            upper=workspace.prop_bbox.upper,
            rgba=constants.GREEN,
            name="prop_spawn_area",
            visible=False,
        )

        self._fall_termination = fall_termination
        self._discount = 1.0

    @property
    def task_observables(self) -> Dict[str, observable.Observable]:
        return self._task_observables

    @property
    def root_entity(self) -> composer.Entity:
        return self._arena

    def initialize_episode(
        self, physics: mjcf.Physics, random_state: np.random.RandomState
    ) -> None:
        self._discount = 1.0

        # Randomly sample a starting configuration for the prop.
        self._prop_placer(physics=physics, random_state=random_state)

        # Randomly sample a goal orientation and use it to configure the orientation of
        # the translucent hint prop.
        self._goal_quat = self._prop_orientation_sampler(random_state=random_state)
        self._hint_prop.set_pose(physics=physics, quaternion=self._goal_quat)

    def get_reward(self, physics: mjcf.Physics) -> float:
        shaped_reward = _get_shaped_reorientation_reward(
            physics,
            prop_quat=physics.bind(self._prop.orientation).sensordata,
            goal_quat=self._goal_quat,
        )
        return rewards.weighted_average(shaped_reward)

    def after_step(
        self, physics: mjcf.Physics, random_state: np.random.RandomState
    ) -> None:
        del random_state  # Unused.
        self._failure_termination = False
        if self._fall_termination:
            if self._is_prop_fallen(physics):
                self._failure_termination = True

    def should_terminate_episode(self, physics: mjcf.Physics) -> bool:
        """Returns true if episode termination criteria are met."""
        if self._failure_termination:
            self._discount = 0.0
            return True
        else:
            if self._is_goal_reached(physics):
                return True
            return False

    def get_discount(self, physics: mjcf.Physics) -> float:
        del physics  # Unused.
        return self._discount

    @property
    def step_limit(self) -> Optional[int]:
        return _STEP_LIMIT

    # Helper methods.

    def _get_quaternion_difference(self, physics: mjcf.Physics) -> np.ndarray:
        """Returns the quaternion difference between the prop and the target prop."""
        prop_quat = physics.bind(self._prop.orientation).sensordata
        target_prop_quat = physics.bind(self._hint_prop.orientation).sensordata
        return tr.quat_diff_active(source_quat=prop_quat, target_quat=target_prop_quat)

    def _get_action(self, physics: mjcf.Physics) -> np.ndarray:
        """Returns the action that was applied."""
        return np.array(physics.data.ctrl)

    def _is_goal_reached(self, physics: mjcf.Physics) -> bool:
        """Returns True if the prop has reached the goal orientation."""
        angular_error = np.linalg.norm(self._get_quaternion_difference(physics))
        assert isinstance(angular_error, float)
        return np.isclose(angular_error, 0.0)

    def _is_prop_fallen(self, physics: mjcf.Physics) -> bool:
        """Returns True if the prop has fallen from the hand."""
        return mujoco_collisions.has_collision(
            physics=physics,
            collision_geom_prefix_1=[f"{self._prop.name}/"],
            collision_geom_prefix_2=[self._arena.ground.full_identifier],
        )


def _get_shaped_reorientation_reward(
    physics: mjcf.Physics,
    prop_quat: np.ndarray,
    goal_quat: np.ndarray,
) -> Dict[str, rewards.Reward]:
    """Returns a tuple of shaping reward components, as defined in [1].

    The reward is a weighted sum of the following components:
        - orientation reward: The inverse of the absolute value of the angular error
            between the prop's current orientation and the goal orientation.
        - success reward: 1.0 if the the angular error is within a tolerance and 0.0
            otherwise.
        - action smoothness reward: The negative of the squared L2 norm of the control
            action.

    Args:
        physics: An `mjcf.Physics` instance.
        prop_quat: The current orientation of the prop, as a quaternion.
        goal_quat: The goal orientation of the prop, as a quaternion.

    References:
        [1]: A System for General In-Hand Object Re-Orientation,
        https://arxiv.org/abs/2111.03043
    """
    shaped_reward = collections.OrderedDict()

    # Orientation component.
    angular_error = np.linalg.norm(
        geometry_utils.get_orientation_error(to_quat=prop_quat, from_quat=goal_quat)
    )
    angular_error_abs = np.abs(angular_error)
    orientation_reward = 1.0 / (angular_error_abs + _ORIENTATION_EPS)
    shaped_reward["orientation"] = rewards.Reward(
        value=orientation_reward, weight=_ORIENTATION_WEIGHT
    )

    # Success bonus component.
    success_bonus_reward = reward_utils.tolerance(
        x=angular_error_abs,
        bounds=(0, _ORIENTATION_THRESHOLD),
        margin=0.0,
    )
    assert isinstance(success_bonus_reward, float)
    shaped_reward["success_bonus"] = rewards.Reward(
        value=success_bonus_reward,
        weight=_SUCCESS_BONUS_WEIGHT,
    )

    # Action smoothing component.
    action_smoothing_reward = np.linalg.norm(physics.data.ctrl) ** 2
    assert isinstance(action_smoothing_reward, float)
    shaped_reward["action_smoothing"] = rewards.Reward(
        value=action_smoothing_reward,
        weight=_ACTION_SMOOTHING_WEIGHT,
    )

    return shaped_reward


def _replace_alpha(rgba: np.ndarray, alpha: float = 0.3) -> np.ndarray:
    """Replaces the alpha value of a color tuple."""
    new_rgba = rgba.copy()
    new_rgba[3] = alpha
    return new_rgba


def _hintify(entity: composer.Entity, alpha: Optional[float] = None) -> None:
    """Modifies an entity for use as a visual hint.

    Specifically, contacts are disabled for all geoms within the entity, and its bodies
    are converted to mocap bodies which are viewed as fixed from the perspective of the
    dynamics. Additionally, the geom alpha values can be overriden to render the geoms
    as translucent.
    """
    for subentity in entity.iter_entities():
        if (
            alpha is not None
            and subentity.mjcf_model.default.geom is not None
            and subentity.mjcf_model.default.geom.rgba is not None
        ):
            subentity.mjcf_model.default.geom.rgba = _replace_alpha(
                subentity.mjcf_model.default.geom.rgba, alpha=alpha
            )
        for body in subentity.mjcf_model.find_all("body"):
            body.mocap = "true"
        for geom in subentity.mjcf_model.find_all("geom"):
            if alpha is not None and geom.rgba is not None:
                geom.rgba = _replace_alpha(geom.rgba, alpha=alpha)
            # This deals with textures.
            if alpha is not None and geom.material is not None:
                material = subentity.mjcf_model.find("material", geom.material)
                material.rgba = _replace_alpha(material.rgba, alpha=alpha)
            geom.contype = 0
            geom.conaffinity = 0


def reorient_task(
    observation_set: observations.ObservationSet,
) -> composer.Task:
    """Configure and instantiate a `ReOrient` task."""
    arena = arenas.Standard()

    hand = shadow_hand_e.ShadowHandSeriesE(
        observable_options=observations.make_options(
            observation_set.value,
            observations.HAND_OBSERVABLES,
        ),
    )

    hand_effector = effectors.HandEffector(hand=hand, hand_name=hand.name)

    return ReOrient(
        arena=arena,
        hand=hand,
        hand_effector=hand_effector,
        observable_settings=observation_set.value,
    )


@SUITE.add(tags.STATE)
def state_dense() -> composer.Task:
    return reorient_task(
        observation_set=observations.ObservationSet.STATE_ONLY,
    )
