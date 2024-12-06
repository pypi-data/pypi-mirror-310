import requests

def stats():
    """Get current stats from Flare Radio."""
    try:
        response = requests.get('https://flareradio.net/staff/api/stats')
        return response.json()
    except:
        return None

def upcoming():
    """Get upcoming shows from Flare Radio."""
    try:
        response = requests.get('https://flareradio.net/staff/api/upcoming')
        return response.json()
    except:
        return None
