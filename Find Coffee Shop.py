import requests

def find_coffee_shops(api_key, location=None, radius=1000, name="coffee"):
    """
    Finds coffee shops within a specified radius of a given location, returning detailed information,
    including placeholders for icon_mask_base_uri and icon_background_color if not available.

    Parameters:
    - api_key: str. Your Google Places API key.
    - location: str or tuple. A place name (str) or a tuple of (latitude, longitude).
    - radius: int. The radius within which to search for coffee shops, in meters.
    - name: str. The type of place to search for. Default is "coffee".

    Returns:
    - list: A detailed list of coffee shops within the specified radius.
    """
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Convert location name to lat/lng if necessary
    if isinstance(location, str):
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"
        geocode_resp = requests.get(geocode_url)
        geocode_data = geocode_resp.json()
        if geocode_data["status"] == "OK":
            location = geocode_data["results"][0]["geometry"]["location"]
            location = (location["lat"], location["lng"])
        else:
            return "Failed to find the location."

    if isinstance(location, tuple):
        lat, lng = location
        location_param = f"{lat},{lng}"
    else:
        return "Invalid location format. Please provide a place name or a tuple of latitude and longitude."

    params = {
        "key": api_key,
        "location": location_param,
        "radius": radius,
        "type": "cafe",
        "keyword": name
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    coffee_shops = []
    if data["status"] == "OK":
        for shop in data["results"]:
            shop_details = {
                "name": shop.get("name"),
                "address": shop.get("vicinity"),
                "location": shop["geometry"]["location"],
                "rating": shop.get("rating"),
                "user_ratings_total": shop.get("user_ratings_total"),
                "price_level": shop.get("price_level", ""),
                "business_status": shop.get("business_status", ""),
                "vicinity": shop.get("vicinity", ""),
                "icon": shop.get("icon", ""),
                "icon_mask_base_uri": shop.get("icon_mask_base_uri", ""),
                "icon_background_color": shop.get("icon_background_color", "")
            }

            # Handle photos
            if "photos" in shop:
                photo_reference = shop["photos"][0]["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                shop_details["photo_url"] = photo_url

            # Opening hours (limited information from Nearby Search)
            if "opening_hours" in shop:
                shop_details["opening_now"] = shop["opening_hours"].get("open_now", "")

            coffee_shops.append(shop_details)
        return coffee_shops
    else:
        return "Failed to find coffee shops."


# Example usage
api_key = "api_key"
location = "George Western Cape"  # You can also use a tuple of latitude and longitude, e.g., (40.7128, -74.0060)
radius = 5000  # Search within 500 meters
coffee_shops = find_coffee_shops(api_key, location, radius)
for shop in coffee_shops:
    print(shop)
