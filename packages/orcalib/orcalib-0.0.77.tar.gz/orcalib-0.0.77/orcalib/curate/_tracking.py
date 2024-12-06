from enum import Enum
from typing import Any, Literal, TypeAlias, TypedDict
from uuid import UUID

from orcalib.client import OrcaClient, OrcaMetadataDict


class FeedbackKind(str, Enum):
    """
    The kind of feedback that can be recorded.

    Attributes:
        CONTINUOUS: any float values between -1.0 and 1.0 are allowed
        BINARY: only the float or integer -1 or 1 is allowed
        FLAG: only the float or integer 1 is allowed
    """

    CONTINUOUS = "CONTINUOUS"
    BINARY = "BINARY"
    FLAG = "FLAG"


RunId: TypeAlias = int
"""The id of a model run."""


def generate_run_ids(
    db_name: str,
    batch_size: int,
    tags: set[str],
    metadata: OrcaMetadataDict,
    model_id: str,
    model_version: str | None = None,
    seq_id: UUID | None = None,
) -> list[RunId]:
    """Generates run ids for the next model run.

    Args:
        db_name: The name of the database.
        model_id: The id of the model.
        model_version: The version of the model. (default: None)
        batch_size: The batch size.
        tags: The tags for the model run.
        metadata: The metadata for the model run.
        seq_id: The sequence id for the model run. (default: None)
    """
    return OrcaClient.init_forward_pass(
        db_name=db_name,
        model_id=model_id,
        model_version=model_version,
        batch_size=batch_size,
        tags=tags,
        metadata=metadata,
        seq_id=seq_id,
    )


def record_memory_weights(
    db_name: str,
    layer_name: str,
    run_ids: list[RunId] | RunId,
    memory_ids: list[int] | int,
    memory_weights: list[float] | float,
) -> None:
    """Records attention weights for the given memory lookups

    Args:
        db_name: The name of the database.
        layer_name: The name of the lookup layer for which the weights are recorded.
        run_ids: The run ids of the memory lookups to record the weights for, this needs to be the
            same length as `memory_ids` and `memory_weights` which might mean repeating the same run
             id multiple times since typically several memories are looked up in a single forward pass.
        memory_ids: The table row ids of the memories for which to record the weights for, these can
            be selected as `'$row_id'` when calling [`vector_scan`][orcalib.IndexHandle.vector_scan].
        memory_weights: The attention weights to be recorded.
    """
    if not isinstance(run_ids, list):
        run_ids = [run_ids]
    if not isinstance(memory_ids, list):
        memory_ids = [memory_ids]
    if not isinstance(memory_weights, list):
        memory_weights = [memory_weights]
    if len(memory_weights) != len(run_ids) != len(memory_ids):
        raise ValueError(
            f"Run ids length ({len(run_ids)}), memory ids length ({len(memory_ids)}) and weights length ({len(memory_weights)}) did not match"
        )
    OrcaClient.record_memory_weights(db_name, layer_name, run_ids, memory_ids, memory_weights)


def record_model_feedback(
    db_name: str,
    run_ids: list[RunId] | RunId,
    values: float | list[float] | int | list[int] | bool | list[bool],
    name: str = "default",
    kind: FeedbackKind | Literal["CONTINUOUS", "BINARY", "FLAG"] = FeedbackKind.CONTINUOUS,
) -> None:
    """Records feedback for the given model runs.

    Args:
        db_name: The name of the database.
        run_ids: The run ids for which the feedback is recorded.
        values: The feedback to be recorded.
        name: The name of the feedback. (default: "default")
        kind: The kind of feedback. (default: FeedbackKind.CONTINUOUS)
    """
    # Ensure feedback is a list of the right length
    if isinstance(values, (float, int)):
        values = [values]
    if isinstance(run_ids, int):
        run_ids = [run_ids]
    if len(values) != len(run_ids):
        raise ValueError(f"Feedback length ({len(values)}) did not match run_ids length ({len(run_ids)})")
    # Ensure feedback is a list of correct floats based on the passed kind
    float_feedback: list[float] = []
    for val in values:
        float_value = float(val)
        match kind:
            case FeedbackKind.FLAG:
                if float_value != 1.0:
                    raise ValueError(f"Unary feedback must be 1.0, got {float_value}")
            case FeedbackKind.BINARY:
                if isinstance(val, bool):
                    float_value = +1.0 if val else -1.0
                if float_value not in (-1.0, +1.0):
                    raise ValueError(f"Binary feedback must be -1 or +1, got {float_value}")
            case FeedbackKind.CONTINUOUS:
                if float_value > 1.0 or float_value < -1.0:
                    raise ValueError(f"Continuous feedback must be between -1 and +1, got {float_value}")
            case _:
                raise ValueError(f"Unsupported feedback kind: {kind}")
        float_feedback.append(float_value)
    OrcaClient.record_model_feedback(db_name, run_ids, float_feedback, name, kind)


def record_model_input_output(
    db_name: str,
    run_ids: list[RunId] | RunId,
    inputs: list[Any] | Any | None,
    outputs: list[Any] | Any | None,
) -> None:
    """Records the inputs and outputs of the given model runs.

    Args:
        db_name: The name of the database.
        run_ids: The run ids for which the inputs and outputs are
            recorded.
        inputs: The inputs to be recorded.
        outputs: The outputs to be recorded.
    """
    if not isinstance(run_ids, list):
        run_ids = [run_ids]
    if inputs is None:
        inputs = [None] * len(run_ids)
    if not isinstance(inputs, list):
        inputs = [inputs]
    if outputs is None:
        outputs = [None] * len(run_ids)
    if not isinstance(outputs, list):
        outputs = [outputs]
    if not (len(inputs) == len(outputs) == len(run_ids)):
        raise ValueError(
            f"Inputs length ({len(inputs)}), output length ({len(outputs)}) and run_ids length ({len(run_ids)}) did not match"
        )
    OrcaClient.record_model_input_output(db_name, run_ids, inputs, outputs)
