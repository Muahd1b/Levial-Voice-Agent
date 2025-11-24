import os
import logging
import os
import logging
import requests
from mcp.server.fastmcp import FastMCP

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aviation_server")

mcp = FastMCP("Aviation Server")

def get_api_key():
    key = os.environ.get("CHECKWX_API_KEY")
    if not key:
        raise ValueError("CHECKWX_API_KEY environment variable not set.")
    return key

@mcp.tool()
def get_metar(icao: str) -> str:
    """
    Get the METAR (weather report) for an airport (ICAO code).
    """
    try:
        api_key = get_api_key()
        # checkwx-python usage might vary, assuming standard API
        # If library is not standard, we might need requests.
        # Let's use requests for reliability if library is unknown, 
        # but since we installed checkwx-python, let's try to use it.
        # Actually, let's use requests to be safe as I don't have docs for the lib.
        import requests
        response = requests.get(
            f"https://api.checkwx.com/metar/{icao}/decoded",
            headers={"X-API-Key": api_key}
        )
        if response.status_code != 200:
            return f"Error fetching METAR: {response.text}"
            
        data = response.json()
        if data.get("results") == 0:
            return f"No METAR found for {icao}"
            
        metar = data["data"][0]
        # Format a nice string
        raw = metar.get("raw_text", "No raw text")
        flight_category = metar.get("flight_category", "Unknown")
        temp = metar.get("temperature", {}).get("celsius", "N/A")
        wind = metar.get("wind", {})
        wind_str = f"{wind.get('degrees', 'N/A')}@{wind.get('speed_kts', 'N/A')}kts"
        
        return f"METAR for {icao} ({flight_category}):\nTemp: {temp}C, Wind: {wind_str}\nRaw: {raw}"
        
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_taf(icao: str) -> str:
    """
    Get the TAF (forecast) for an airport.
    """
    try:
        api_key = get_api_key()
        import requests
        response = requests.get(
            f"https://api.checkwx.com/taf/{icao}/decoded",
            headers={"X-API-Key": api_key}
        )
        if response.status_code != 200:
            return f"Error fetching TAF: {response.text}"
            
        data = response.json()
        if data.get("results") == 0:
            return f"No TAF found for {icao}"
            
        taf = data["data"][0]
        raw = taf.get("raw_text", "No raw text")
        return f"TAF for {icao}:\n{raw}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
