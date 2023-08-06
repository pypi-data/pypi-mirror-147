from typing import Any, Dict, cast
from unittest.mock import MagicMock, patch

from chaosreliably.controls import experiment
from chaosreliably.types import EntityContextExperimentRunLabels, EventType


@patch("chaosreliably.controls.experiment._create_experiment_event")
def test_after_method_control_calls_create_experiment_event(
    mock_create_experiment_event: MagicMock,
) -> None:
    run_labels = EntityContextExperimentRunLabels(name="hello", user="TestUser")
    title = "Test Experiment Title"
    name = f"{title} - Method End"
    configuration = {
        "chaosreliably": {"experiment_run_labels": run_labels.dict()}
    }
    probe = {
        "type": "probe",
        "name": "test-probe",
        "tolerance": True,
        "provider": {
            "type": "python",
            "module": "test.module",
            "func": "test_func",
        },
    }
    run = {
        "activity": probe,
        "output": False,
        "status": "succeeded",
        "start": "2021-08-17T08:34:46.884325",
        "end": "2021-08-17T08:34:46.891386",
        "duration": 0.007061,
        "tolerance_met": False,
    }

    experiment.after_method_control(
        context={
            "title": title,
            "description": "A test description",
            "method": [],
        },
        **cast(
            Dict[str, Any],
            {"state": [run], "configuration": configuration, "secrets": None},
        ),
    )

    mock_create_experiment_event.assert_called_once_with(
        event_type=EventType.METHOD_END,
        name=name,
        output=[run],
        experiment_run_labels=run_labels,
        configuration=configuration,
        secrets=None,
    )


@patch("chaosreliably.controls.experiment.logger")
def test_that_an_exception_does_not_get_raised_and_warning_logged(
    mock_logger: MagicMock,
) -> None:

    experiment.after_method_control(
        context={
            "title": "Test Experiment Title",
            "description": "A test description",
            "method": [],
        },
        **cast(
            Dict[str, Any], {"configuration": {}, "state": [], "secrets": None}
        ),
    )
    mock_logger.debug.assert_called_once_with(
        "An error occurred: 'chaosreliably', while running the After Method "
        "control, the Experiment execution won't be affected.",
        exc_info=True,
    )
