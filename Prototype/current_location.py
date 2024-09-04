import requests

def get_current_location():
    # Use the ipinfo.io API to get detailed location information
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        location = data['loc'].split(',')
        return f"Latitude: {location[0]}, Longitude: {location[1]}, City: {data['city']}, Region: {data['region']}, Country: {data['country']}"
    except Exception as e:
        return "Location not available"

# Example usage
location = get_current_location()
print(location)
