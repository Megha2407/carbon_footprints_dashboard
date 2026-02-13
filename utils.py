def calculate_carbon(transport_km, electricity_kwh, meat_meals):
    transport_emission = transport_km * 0.21      # kg CO2 per km
    electricity_emission = electricity_kwh * 0.82 # kg CO2 per kWh
    food_emission = meat_meals * 2.5              # kg CO2 per meal
    
    total = transport_emission + electricity_emission + food_emission
    
    return {
        "Transport": transport_emission,
        "Electricity": electricity_emission,
        "Food": food_emission,
        "Total": total
    }
