import json
import os
import aiohttp
from dhisana.utils.assistant_tool_tag import assistant_tool

@assistant_tool
async def search_google_custom(
    query: str,
    number_of_results: int = 10
):
    """
    Search Google using the Google Custom Search JSON API and return the results as an array of serialized JSON strings.
    
    Parameters:
    - **query** (*str*): The search query.
    - **number_of_results** (*int*): The number of results to return.
    """

    API_KEY = os.environ.get('GOOGLE_SEARCH_KEY')
    CX = os.environ.get('GOOGLE_SEARCH_CX')  # Custom Search Engine ID
    if not API_KEY or not CX:
        return {'error': "Google Custom Search API key or CX not found in environment variables"}

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "num": number_of_results
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result}
                
                # Serialize each result to JSON string
                serialized_results = [json.dumps(item) for item in result.get('items', [])]
                return serialized_results
    except Exception as e:
        return {'error': str(e)}




@assistant_tool
async def search_google_places(
    query: str,
    location_bias: dict = None,  # e.g., {"latitude": 37.7749, "longitude": -122.4194, "radius": 5000}
    number_of_results: int = 3
):
    """
    Search Google Places API (New) and return the results as an array of serialized JSON strings.

    Parameters:
    - **query** (*str*): The search query.
    - **location_bias** (*dict*): Optional. A dictionary with 'latitude', 'longitude', and 'radius' (in meters) to bias the search.
    - **number_of_results** (*int*): The number of results to return.
    """
    GOOGLE_SEARCH_KEY = os.environ.get('GOOGLE_SEARCH_KEY')
    if not GOOGLE_SEARCH_KEY:
        return {'error': "Google Places API key not found in environment variables"}

    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': GOOGLE_SEARCH_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location,places.websiteUri,places.rating,places.reviews'
    }

    request_body = {
        "textQuery": query
    }

    if location_bias:
        request_body["locationBias"] = {
            "circle": {
                "center": {
                    "latitude": location_bias.get("latitude"),
                    "longitude": location_bias.get("longitude")
                },
                "radius": location_bias.get("radius", 5000)  # Default to 5 km if radius not provided
            }
        }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=request_body) as response:
                result = await response.json()
                if response.status != 200:
                    return {'error': result.get('error', {}).get('message', 'Unknown error')}

                # Extract the required number of results
                places = result.get('places', [])[:number_of_results]

                # Serialize each place result to JSON string
                serialized_results = [json.dumps(place) for place in places]
                return serialized_results
    except Exception as e:
        return {'error': str(e)}

