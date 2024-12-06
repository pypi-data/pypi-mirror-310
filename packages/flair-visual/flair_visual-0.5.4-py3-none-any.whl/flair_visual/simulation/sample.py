from collections import Counter
from functools import cached_property
from dataclasses import (
    dataclass as python_dataclass,
    field as python_field,
)
from typing import (
    Set,
    Dict,
    Generic,
    Optional,
    Any,
    Tuple,
)
import numpy as np
from flair_visual.simulation.constructor import (
    CircuitConstructorABC,
    CircuitType,
)
from flair_visual.simulation import schema


@python_dataclass
class AtomLossCircuitSampler(Generic[CircuitType]):
    """A sampler for a noisy quantum circuit with atom loss.

    Fields:
        circuit (schema.NoiseModel): The noise model of the quantum circuit.
        circuit_generator (CircuitConstructorABC[CircuitType]): The circuit generator.


    """

    circuit: schema.NoiseModel
    circuit_generator: CircuitConstructorABC[CircuitType]

    survival_probs: np.ndarray[float] = python_field(init=False)
    measure_tags: Set[str] = python_field(init=False, default_factory=set)
    all_qubits: Tuple[int, ...] = python_field(init=False)

    def __post_init__(self):
        assert isinstance(self.circuit_generator, CircuitConstructorABC)
        self.all_qubits = self.circuit.all_qubits

        assert all(
            len(gate.error.survival_prob) == self.num_qubits
            for gate in self.circuit.gate_events
        ), "Survival probabilities must be of shape (num_qubits,)"

        self.survival_probs = np.asarray(
            [list(block.error.survival_prob) for block in self.circuit.gate_events]
        )
        self.survival_probs = self.survival_probs.reshape(
            (len(self.circuit.gate_events), self.num_qubits)
        )

        assert self.survival_probs.shape == (
            len(self.circuit.gate_events),
            self.num_qubits,
        ), "Survival probabilities must be of shape (num_gates, num_qubits)"

        measure_tags = [
            gate.operation.measure_tag
            for gate in self.circuit.gate_events
            if isinstance(gate.operation, schema.Measurement)
        ]
        self.measure_tags.update(measure_tags)
        assert len(self.measure_tags) == len(
            measure_tags
        ), "Duplicate measurement tags found in gate events"
        assert (
            self.num_qubits == 0 or len(self.measure_tags) > 0
        ), "No measurement tags found in gate events"

    @property
    def num_qubits(self) -> int:
        """Get the number of qubits in the circuit."""
        return len(self.all_qubits)

    def active_qubit_states(
        self, generator: Optional[np.random.Generator] = None
    ) -> np.ndarray[Any, bool]:
        """Sample the survival state for each all gate events.

        Args:
            generator (Optional[np.random.Generator], optional): The random number generator. Defaults to None.

        Returns:
            active_qubits, (np.ndarray[Any, bool]):
                A boolean array of shape (num_gates, num_qubits) where `True` indicates the qubit survived.

        """
        if generator is None:
            generator = np.random.default_rng()

        return (
            (
                generator.random(size=(len(self.circuit.gate_events), self.num_qubits))
                <= self.survival_probs
            )
            .cumprod(axis=0)
            .astype(bool)
        )

    @cached_property
    def clean_circuit(self) -> CircuitType:
        """The effective circuit that is executed by the hardware."""
        operations = (gate_event.operation for gate_event in self.circuit.gate_events)
        return self.circuit_generator.join(
            list(map(self.circuit_generator.emit_operation, operations))
        )

    @cached_property
    def noise_model(self) -> CircuitType:
        """The noise model for representing the execution of the circuit on the hardware assuming no atom loss."""
        active_qubits = np.ones_like(self.survival_probs, dtype=bool)
        return self.generate_noise_model(active_qubits)

    def generate_noise_model(self, active_qubits: np.ndarray[Any, bool]) -> CircuitType:
        """Generates an instance of the noise model given the active qubits.

        Args:
            active_qubits (np.ndarray[Any, bool]): The active qubits.
                use `active_qubit_states` to generate this array.

        Returns:
            noise_model (CircuitType): The noise model for the circuit.
                accounts for atom loss and other noise sources.

        """
        return self.circuit_generator.join(
            list(
                map(
                    self.circuit_generator.emit,
                    self.circuit.gate_events,
                    active_qubits,
                )
            )
        )

    def run(
        self, shots: int, generator: Optional[np.random.Generator] = None
    ) -> Dict[str, Dict[str, int]]:
        """Run the circuit with atom loss and return the measurement results.

        Args:
            shots (int): The number of shots to run the circuit.
            generator (Optional[np.random.Generator], optional): The random number generator. Defaults to None.

        Returns:
            result (Dict[str, Dict[str, int]]): The measurement results for each tag. The first key is the
                measurement tag and the second key is the bitstrings for that tag.

        """
        if len(self.measure_tags) == 0:
            return {}

        counters = {tag: Counter() for tag in self.measure_tags}
        for _ in range(shots):
            active_qubits = self.active_qubit_states(generator)
            noise_model = self.generate_noise_model(active_qubits)
            results = self.circuit_generator.run(noise_model, self.measure_tags)
            for tag, result in results.items():
                counters[tag][result] += 1

        return {tag: dict(counter) for tag, counter in counters.items()}
