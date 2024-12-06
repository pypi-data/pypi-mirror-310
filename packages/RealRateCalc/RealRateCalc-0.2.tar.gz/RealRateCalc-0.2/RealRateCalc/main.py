import requests
import time

def points_calculator(points, api):

    points = points
    value = None

    # 5d0721749adfe9d9c6626a5e
        
    api_url = f"https://v6.exchangerate-api.com/v6/{api}/latest/USD"
    # Send the request to the API
    response = requests.get(api_url)
        # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Fetch conversion rates for INR, EUR, and USD
        conversion_rate_eur = data['conversion_rates']['EUR']
        conversion_rate_inr = data['conversion_rates']['INR']
        conversion_rate_usd = data['conversion_rates']['USD']
        
        # Assuming 1 point = 0.1 USD
        value_in_usd = points * 0.1
        value_in_eur = value_in_usd * conversion_rate_eur
        value_in_inr = value_in_usd * conversion_rate_inr
        last_updated = time.ctime()
        
        # Output the values
        values = {
            "points": points,
            "value_in_usd": value_in_usd,
            "value_in_eur": value_in_eur,
            "value_in_inr": value_in_inr,
            "last_updated": last_updated,
        }
        
        
        return values 
        print(values)
        
    else:
        print("Error fetching real-time exchange rates.")
    
    return points

def hello():
    print("Hello from Real Rate Calculator!! ^_^")
    
api_key = "5d0721749adfe9d9c6626a5e"
points_calculator(points=500, api=api_key)