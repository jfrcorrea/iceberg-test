import dlt
import requests
from dlt.sources.helpers import requests as dlt_requests

def get_opensky_token(client_id: str, client_secret: str) -> str:
    """Obtains an OAuth2 access token from OpenSky Network."""
    auth_url = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(auth_url, data=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("access_token")

@dlt.source
def opensky(client_id: str = dlt.secrets.value, client_secret: str = dlt.secrets.value):
    return states(client_id=client_id, client_secret=client_secret)

@dlt.resource(write_disposition="append")
def states(
    client_id: str = dlt.secrets.value,
    client_secret: str = dlt.secrets.value,
    last_contact=dlt.sources.incremental("last_contact", initial_value=0),
):
    """Fetches all state vectors from OpenSky Network.
    
    This resource is incremental and uses 'last_contact' to track the last loaded state.
    """
    
    # Get the token
    token = get_opensky_token(client_id, client_secret)
    
    url = "https://opensky-network.org/api/states/all"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    params = {}
    
    response = dlt_requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    time_stamp = data.get("time")
    states_list = data.get("states", [])
    
    # Column mapping according to OpenSky REST API documentation
    columns = [
        "icao24", "callsign", "origin_country", "time_position",
        "last_contact", "longitude", "latitude", "baro_altitude",
        "on_ground", "velocity", "true_track", "vertical_rate",
        "sensors", "geo_altitude", "squawk", "spi", "position_source", "category"
    ]
    
    for state in states_list:
        # Convert list to dict for better downstream handling
        record = dict(zip(columns, state))
        # Add the request time for reference
        record["request_time"] = time_stamp
        yield record
