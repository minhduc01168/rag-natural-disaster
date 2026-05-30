from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataNormalizer:
    """
    Normalize GIS data from various sources into standard format for PostGIS storage.
    """

    def normalize_elevation(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Normalize SRTM elevation data.
        Returns list of records with: geom (WKT), elevation, source, fetched_at
        """
        try:
            records = []
            for point in raw_data.get("records", []):
                records.append({
                    "geom": f"POINT({point['lon']} {point['lat']})",
                    "elevation": point["elevation"],
                    "source": "srtm",
                    "fetched_at": datetime.now().isoformat(),
                })
            return records
        except Exception as e:
            logger.error(f"Elevation normalization failed: {e}")
            return []

    def normalize_precipitation(self, raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Normalize GPM precipitation data.
        Returns list of records with: geom (WKT), amount, date, source
        """
        try:
            records = []
            bounds = raw_data.get("bounds", [102, 8, 110, 24])
            center_lon = (bounds[0] + bounds[2]) / 2
            center_lat = (bounds[1] + bounds[3]) / 2

            for precip in raw_data.get("precipitation", []):
                records.append({
                    "geom": f"POINT({center_lon} {center_lat})",
                    "amount": precip["amount"],
                    "date": precip["date"],
                    "source": "gpm",
                })
            return records
        except Exception as e:
            logger.error(f"Precipitation normalization failed: {e}")
            return []

    def normalize_disasters(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize HDX disaster data.
        Returns list of records with: geom (WKT), type, severity, date, source
        """
        try:
            records = []
            for disaster in raw_data:
                coords = disaster.get("coordinates", {})
                records.append({
                    "geom": f"POINT({coords.get('lon', 0)} {coords.get('lat', 0)})",
                    "type": disaster.get("type", "unknown"),
                    "severity": disaster.get("severity", "unknown"),
                    "date": disaster.get("date"),
                    "source": "hdx",
                })
            return records
        except Exception as e:
            logger.error(f"Disaster normalization failed: {e}")
            return []

    def validate_geometry(self, wkt: str) -> bool:
        """
        Validate WKT geometry string.
        """
        try:
            if not wkt or not isinstance(wkt, str):
                return False

            # Basic validation
            if wkt.startswith("POINT(") and wkt.endswith(")"):
                coords = wkt[6:-1].split()
                if len(coords) == 2:
                    lon, lat = float(coords[0]), float(coords[1])
                    return -180 <= lon <= 180 and -90 <= lat <= 90

            return False
        except (ValueError, IndexError):
            return False


data_normalizer = DataNormalizer()
