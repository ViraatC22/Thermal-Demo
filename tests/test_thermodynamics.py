import unittest

from thermodynamics import (
    MATERIALS,
    simulation_speed_factor,
    thermal_exchange_step,
)


class ThermalExchangeStepTests(unittest.TestCase):
    def test_extreme_controls_do_not_overshoot_equilibrium(self):
        hot = 200.0 + 273.15
        cold = 0.0 + 273.15
        properties = MATERIALS["Gold"]

        result = thermal_exchange_step(
            hot,
            cold,
            mass_kg=0.1,
            specific_heat_j_per_kg_k=properties["specific_heat"],
            conductivity=properties["conductivity"],
            speed_factor=simulation_speed_factor(properties["conductivity"]),
        )

        equilibrium = (hot + cold) / 2.0
        self.assertGreaterEqual(result.hot_temperature_k, equilibrium)
        self.assertLessEqual(result.cold_temperature_k, equilibrium)
        self.assertGreater(result.entropy_change_j_per_k, 0.0)

    def test_each_step_conserves_total_thermal_energy(self):
        hot = 373.15
        cold = 293.15
        mass = 2.5
        properties = MATERIALS["Copper"]
        heat_capacity = mass * properties["specific_heat"]

        result = thermal_exchange_step(
            hot,
            cold,
            mass_kg=mass,
            specific_heat_j_per_kg_k=properties["specific_heat"],
            conductivity=properties["conductivity"],
            speed_factor=simulation_speed_factor(properties["conductivity"]),
        )

        initial_energy = heat_capacity * (hot + cold)
        final_energy = heat_capacity * (
            result.hot_temperature_k + result.cold_temperature_k
        )
        self.assertAlmostEqual(initial_energy, final_energy, places=8)

    def test_all_materials_reach_equilibrium_with_slowest_mass_setting(self):
        for material_name, properties in MATERIALS.items():
            with self.subTest(material=material_name):
                hot = 473.15
                cold = 273.15
                cumulative_entropy = 0.0

                for _ in range(5000):
                    result = thermal_exchange_step(
                        hot,
                        cold,
                        mass_kg=5.0,
                        specific_heat_j_per_kg_k=properties["specific_heat"],
                        conductivity=properties["conductivity"],
                        speed_factor=simulation_speed_factor(
                            properties["conductivity"]
                        ),
                    )
                    hot = result.hot_temperature_k
                    cold = result.cold_temperature_k
                    cumulative_entropy += result.entropy_change_j_per_k
                    if hot - cold <= 0.05:
                        break

                self.assertLessEqual(hot - cold, 0.05)
                self.assertGreater(cumulative_entropy, 0.0)

    def test_invalid_physical_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            thermal_exchange_step(0.0, 273.15, 1.0, 450.0, 0.1, 150.0)


if __name__ == "__main__":
    unittest.main()
