def calculate_carbon(transport_km, electricity_kwh, meat_meals):
    transport = transport_km * 0.21
    electricity = electricity_kwh * 0.82
    food = meat_meals * 2.5
    total = transport + electricity + food

    return {
        "Transport": transport,
        "Electricity": electricity,
        "Food": food,
        "Total": total
    }


def ai_suggestion(emissions):
    if emissions["Total"] < 10:
        return "Excellent job! Your carbon footprint is low. Continue sustainable practices."
    elif emissions["Transport"] > emissions["Electricity"] and emissions["Transport"] > emissions["Food"]:
        return "Transportation is your biggest contributor. Consider public transport or carpooling."
    elif emissions["Electricity"] > emissions["Food"]:
        return "Electricity usage is high. Try switching to LED bulbs and energy efficient appliances."
    else:
        return "Food emissions are significant. Reducing meat consumption can lower your carbon footprint."

