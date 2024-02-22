import requests


def find_places(api_key, location=None, radius=1000, name=None, place_type="cafe", num_photos=3):
    """
    Finds places within a specified radius of a given location, returning detailed information,
    including a specified number of photo URLs.

    Parameters:
    - api_key: str. Your Google Places API key.
    - location: str or tuple. A place name (str) or a tuple of (latitude, longitude).
    - radius: int. The radius within which to search for places, in meters.
    - name: str. Optional. A name to further refine the search within the specified type.
    - place_type: str. The type of place to search for. Default is "cafe".
    - num_photos: int. The number of photos to return for each place.

    Returns:
    - list: A detailed list of places within the specified radius, including photo URLs.
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
        "type": place_type,
        "keyword": name if name else place_type
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    places = []
    if data["status"] == "OK":
        for place in data["results"]:
            place_details = {
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "location": place["geometry"]["location"],
                "rating": place.get("rating", ""),
                "user_ratings_total": place.get("user_ratings_total", ""),
                "price_level": place.get("price_level", ""),
                "business_status": place.get("business_status", ""),
                "vicinity": place.get("vicinity", ""),
                "icon": place.get("icon", ""),
                "icon_mask_base_uri": place.get("icon_mask_base_uri", ""),
                "icon_background_color": place.get("icon_background_color", ""),
                "photos": []
            }

            # Handle photos
            if "photos" in place and num_photos > 0:
                for photo in place["photos"][:num_photos]:
                    photo_reference = photo["photo_reference"]
                    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
                    place_details["photos"].append(photo_url)

            # Opening hours (limited information from Nearby Search)
            if "opening_hours" in place:
                place_details["opening_now"] = place["opening_hours"].get("open_now", "")

            places.append(place_details)
        return places
    else:
        return "Failed to find places."


# Example usage
api_key = "API KEY"
location = "George Western Cape"  # You can also use a tuple of latitude and longitude, e.g., (40.7128, -74.0060)
radius = 5000  # Search within 500 meters
# coffee_shops = find_coffee_shops(api_key, location, radius)
place_type = "restaurant"  # Try changing to "restaurant", "hotel", etc.
num_photos = 3  # Specify the number of photos you want
places = find_places(api_key, location, radius, place_type=place_type, num_photos=num_photos)
for place in places:
    print(place)


"""
Common Place Types:

accounting
airport
amusement_park
aquarium
art_gallery
atm
bakery
bank
bar
beauty_salon
bicycle_store
book_store
bowling_alley
bus_station
cafe
campground
car_dealer
car_rental
car_repair
car_wash
casino
cemetery
church
city_hall
clothing_store
convenience_store
courthouse
dentist
department_store
doctor
drugstore
electrician
electronics_store
embassy
fire_station
florist
funeral_home
furniture_store
gas_station
gym
hair_care
hardware_store
hindu_temple
home_goods_store
hospital
insurance_agency
jewelry_store
laundry
lawyer
library
light_rail_station
liquor_store
local_government_office
locksmith
lodging (e.g., hotels, motels)
meal_delivery
meal_takeaway
mosque
movie_rental
movie_theater
moving_company
museum
night_club
painter
park
parking
pet_store
pharmacy
physiotherapist
plumber
police
post_office
primary_school
real_estate_agency
restaurant
roofing_contractor
rv_park
school
secondary_school
shoe_store
shopping_mall
spa
stadium
storage
store
subway_station
supermarket
synagogue
taxi_stand
tourist_attraction
train_station
transit_station
travel_agency
university
veterinary_care
zoo
"""
