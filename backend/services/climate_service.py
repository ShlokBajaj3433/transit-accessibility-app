# backend/services/climate_service.py

class ClimateEngine:
    def __init__(self):
        # Emission factors (kg CO2 per km)
        # Source: EPA / UK DEFRA average factors
        self.EMISSION_CAR = 0.171  # Average passenger car
        self.EMISSION_BUS = 0.089  # Average local bus (per passenger approx)
        self.EMISSION_WALK = 0.0
        self.EMISSION_BIKE = 0.0

    def calculate_savings(self, distance_km: float, mode: str):
        """
        Calculates kg of CO2 saved by NOT driving a car.
        Returns:
            dict: { "co2_saved_kg": float, "points_earned": int }
        """
        # 1. Calculate what the emissions WOULD be if they drove
        baseline_emissions = distance_km * self.EMISSION_CAR

        # 2. Calculate actual emissions based on mode
        if mode.lower() == "bus":
            actual_emissions = distance_km * self.EMISSION_BUS
        elif mode.lower() in ["walk", "bike", "subway"]:
            # Subway is often considered near-zero at point of use,
            # or significantly lower than bus. For MVP, we treat as very low.
            actual_emissions = 0.02 * distance_km
        else:
            # Default to car emissions if unknown mode
            actual_emissions = baseline_emissions

        # 3. Calculate Savings
        saved_kg = baseline_emissions - actual_emissions

        # Ensure we don't return negative savings (e.g. if bus was somehow worse)
        if saved_kg < 0:
            saved_kg = 0.0

        # 4. Gamification: 100 points per 1 kg of CO2 saved
        points = int(saved_kg * 100)

        return {
            "mode": mode,
            "distance_km": distance_km,
            "baseline_car_kg": round(baseline_emissions, 3),
            "actual_kg": round(actual_emissions, 3),
            "co2_saved_kg": round(saved_kg, 3),
            "points_earned": points
        }


# Simple test to run this file directly
if __name__ == "__main__":
    engine = ClimateEngine()

    # Test Scenario: 5km Bus ride
    result = engine.calculate_savings(distance_km=5.0, mode="bus")
    print(f"Bus Trip Results: {result}")

    # Test Scenario: 2km Walk
    result_walk = engine.calculate_savings(distance_km=2.0, mode="walk")
    print(f"Walk Trip Results: {result_walk}")