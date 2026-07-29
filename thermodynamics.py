"""Pure thermodynamic calculations used by the Streamlit interface."""

from dataclasses import dataclass
import math


MATERIALS = {
    "Iron": {"specific_heat": 450.0, "conductivity": 0.1},
    "Aluminum": {"specific_heat": 900.0, "conductivity": 0.2},
    "Copper": {"specific_heat": 385.0, "conductivity": 0.3},
    "Gold": {"specific_heat": 129.0, "conductivity": 0.4},
    "Wood": {"specific_heat": 1700.0, "conductivity": 0.01},
}


@dataclass(frozen=True)
class ThermalExchangeStep:
    """The state produced by one energy-conserving heat-transfer step."""

    hot_temperature_k: float
    cold_temperature_k: float
    heat_transferred_j: float
    entropy_change_j_per_k: float


def simulation_speed_factor(conductivity: float) -> float:
    """Return a display-oriented time multiplier for the selected material."""
    return 1000.0 if conductivity < 0.05 else 150.0


def thermal_exchange_step(
    hot_temperature_k: float,
    cold_temperature_k: float,
    mass_kg: float,
    specific_heat_j_per_kg_k: float,
    conductivity: float,
    speed_factor: float,
) -> ThermalExchangeStep:
    """Advance two identical blocks by one stable heat-transfer step.

    The requested heat transfer is capped at half of the energy required to
    reach equilibrium. This keeps the explicit simulation stable and prevents
    the two temperatures from crossing when a user selects a small mass or a
    highly conductive material.
    """
    if hot_temperature_k <= 0 or cold_temperature_k <= 0:
        raise ValueError("Temperatures must be greater than absolute zero.")
    if mass_kg <= 0 or specific_heat_j_per_kg_k <= 0:
        raise ValueError("Mass and specific heat must be positive.")
    if conductivity < 0 or speed_factor < 0:
        raise ValueError("Conductivity and speed factor cannot be negative.")

    temperature_gap = hot_temperature_k - cold_temperature_k
    if temperature_gap <= 0:
        return ThermalExchangeStep(
            hot_temperature_k,
            cold_temperature_k,
            0.0,
            0.0,
        )

    heat_capacity = mass_kg * specific_heat_j_per_kg_k
    requested_heat = conductivity * temperature_gap * speed_factor
    heat_to_equilibrium = heat_capacity * temperature_gap / 2.0
    transferred_heat = min(requested_heat, heat_to_equilibrium / 2.0)
    temperature_change = transferred_heat / heat_capacity

    next_hot = hot_temperature_k - temperature_change
    next_cold = cold_temperature_k + temperature_change
    entropy_change = heat_capacity * (
        math.log(next_hot / hot_temperature_k)
        + math.log(next_cold / cold_temperature_k)
    )

    # Floating-point cancellation can produce a tiny negative value near
    # equilibrium even though the analytical entropy change is non-negative.
    entropy_change = max(0.0, entropy_change)

    return ThermalExchangeStep(
        next_hot,
        next_cold,
        transferred_heat,
        entropy_change,
    )
