import requests

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another."""
    api_key = "fca_live_t0StDQuMo6RgcqaFQmVyaUgPTCBXRD9Ce23mm4tN"  # API key directly from the URL
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'data' in data and from_currency in data['data'] and to_currency in data['data']:
            from_rate = data['data'][from_currency]
            to_rate = data['data'][to_currency]
            converted_amount = amount * (to_rate / from_rate)
            return round(converted_amount, 2)  # Round to 2 decimal places
        else:
            return f"Rates not found for {from_currency} and {to_currency}."
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
