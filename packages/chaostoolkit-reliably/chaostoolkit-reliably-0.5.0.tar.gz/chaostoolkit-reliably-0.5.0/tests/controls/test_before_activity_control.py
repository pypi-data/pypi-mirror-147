from unittest.mock import MagicMock, patch

from chaosreliably.controls import experiment
from chaosreliably.types import EntityContextExperimentRunLabels, EventType


@patch("chaosreliably.controls.experiment._create_experiment_event")
def test_before_activity_control_calls_create_experiment_event(
    mock_create_experiment_event: MagicMock,
) -> None:
    run_labels = EntityContextExperimentRunLabels(name="hello", user="TestUser")
    name = "A Test Activity"
    configuration = {
        "chaosreliably": {"experiment_run_labels": run_labels.dict()}
    }
    activity = {
        "type": "action",
        "name": name,
        "provider": {
            "type": "python",
            "module": "test.module",
            "func": "test_func",
        },
        "controls": [],
    }

    experiment.before_activity_control(
        context=activity, **{"configuration": configuration, "secrets": None}
    )

    mock_create_experiment_event.assert_called_once_with(
        event_type=EventType.ACTIVITY_START,
        name=name,
        output=None,
        experiment_run_labels=run_labels,
        configuration=configuration,
        secrets=None,
    )


@patch("chaosreliably.controls.experiment.logger")
def test_that_an_exception_does_not_get_raised_and_warning_logged(
    mock_logger: MagicMock,
) -> None:
    activity = {
        "type": "action",
        "name": "A Test Activity",
        "provider": {
            "type": "python",
            "module": "test.module",
            "func": "test_func",
        },
        "controls": [],
    }

    experiment.before_activity_control(
        context=activity, **{"configuration": {}, "secrets": None}
    )

    mock_logger.debug.assert_called_once_with(
        "An error occurred: 'chaosreliably', while running the Before "
        "Activity control, the Experiment execution won't be affected.",
        exc_info=True,
    )
