import json
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"


def fetch_nasa_exoplanet_data(planet_name: str) -> Optional[Dict[str, Any]]:
    """
    Query the official NASA Exoplanet Archive TAP web API for planetary
    and stellar parameters given a planet name.
    """
    query = (
        f"SELECT pl_name, pl_orbsmax, st_lum "
        f"FROM ps "
        f"WHERE default_flag=1 AND LOWER(pl_name)=LOWER('{planet_name}')"
    )

    params = {
        "query": query,
        "format": "json",
    }

    url = f"{NASA_TAP_URL}?{urllib.parse.urlencode(params)}"

    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "EarthInABox/2.0 Scientific Climate Engine"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                if data and len(data) > 0:
                    record = data[0]
                    dist = record.get("pl_orbsmax")
                    lum_log = record.get("st_lum")

                    lum_ratio = None
                    if lum_log is not None:
                        lum_ratio = 10**lum_log

                    return {
                        "planet_name": record.get("pl_name"),
                        "distance_au": dist,
                        "luminosity_ratio": lum_ratio,
                    }
    except Exception:
        return None

    return None