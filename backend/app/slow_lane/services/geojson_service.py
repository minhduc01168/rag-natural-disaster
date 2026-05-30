from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GeoJSONService:
    """
    Service for converting data to GeoJSON format.
    """

    def create_feature_collection(
        self,
        features: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a GeoJSON FeatureCollection.
        """
        return {
            "type": "FeatureCollection",
            "features": features,
            "metadata": metadata or {},
        }

    def create_point_feature(
        self,
        lon: float,
        lat: float,
        properties: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create a GeoJSON Point Feature.
        """
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat],
            },
            "properties": properties,
        }

    def create_polygon_feature(
        self,
        coordinates: List[List[List[float]]],
        properties: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create a GeoJSON Polygon Feature.
        """
        return {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": coordinates,
            },
            "properties": properties,
        }

    def elevation_to_geojson(
        self,
        data: List[Dict[str, Any]],
        bbox: Optional[List[float]] = None,
        page: int = 1,
        per_page: int = 100,
    ) -> Dict[str, Any]:
        """
        Convert elevation data to GeoJSON.
        """
        features = []
        for item in data:
            feature = self.create_point_feature(
                lon=item.get("lon", 0),
                lat=item.get("lat", 0),
                properties={
                    "elevation": item.get("elevation", 0),
                    "source": item.get("source", "srtm"),
                },
            )
            features.append(feature)

        # Apply pagination
        start = (page - 1) * per_page
        end = start + per_page
        paginated_features = features[start:end]

        return self.create_feature_collection(
            features=paginated_features,
            metadata={
                "total": len(features),
                "page": page,
                "per_page": per_page,
                "type": "elevation",
            },
        )

    def precipitation_to_geojson(
        self,
        data: List[Dict[str, Any]],
        bbox: Optional[List[float]] = None,
        page: int = 1,
        per_page: int = 100,
    ) -> Dict[str, Any]:
        """
        Convert precipitation data to GeoJSON.
        """
        features = []
        for item in data:
            feature = self.create_point_feature(
                lon=item.get("lon", 0),
                lat=item.get("lat", 0),
                properties={
                    "amount": item.get("amount", 0),
                    "date": item.get("date"),
                    "source": item.get("source", "gpm"),
                },
            )
            features.append(feature)

        start = (page - 1) * per_page
        end = start + per_page
        paginated_features = features[start:end]

        return self.create_feature_collection(
            features=paginated_features,
            metadata={
                "total": len(features),
                "page": page,
                "per_page": per_page,
                "type": "precipitation",
            },
        )

    def disasters_to_geojson(
        self,
        data: List[Dict[str, Any]],
        bbox: Optional[List[float]] = None,
        page: int = 1,
        per_page: int = 100,
    ) -> Dict[str, Any]:
        """
        Convert disaster data to GeoJSON.
        """
        features = []
        for item in data:
            feature = self.create_point_feature(
                lon=item.get("lon", 0),
                lat=item.get("lat", 0),
                properties={
                    "type": item.get("type", "unknown"),
                    "severity": item.get("severity", "unknown"),
                    "date": item.get("date"),
                    "description": item.get("description", ""),
                    "source": item.get("source", "hdx"),
                },
            )
            features.append(feature)

        start = (page - 1) * per_page
        end = start + per_page
        paginated_features = features[start:end]

        return self.create_feature_collection(
            features=paginated_features,
            metadata={
                "total": len(features),
                "page": page,
                "per_page": per_page,
                "type": "disasters",
            },
        )

    def lsm_to_geojson(
        self,
        data: List[Dict[str, Any]],
        bbox: Optional[List[float]] = None,
        page: int = 1,
        per_page: int = 100,
    ) -> Dict[str, Any]:
        """
        Convert LSM predictions to GeoJSON.
        """
        features = []
        for item in data:
            feature = self.create_point_feature(
                lon=item.get("lon", 0),
                lat=item.get("lat", 0),
                properties={
                    "susceptibility": item.get("susceptibility", 0),
                    "risk_level": item.get("risk_level", "low"),
                    "model_version": item.get("model_version", "v1"),
                },
            )
            features.append(feature)

        start = (page - 1) * per_page
        end = start + per_page
        paginated_features = features[start:end]

        return self.create_feature_collection(
            features=paginated_features,
            metadata={
                "total": len(features),
                "page": page,
                "per_page": per_page,
                "type": "lsm",
            },
        )


geojson_service = GeoJSONService()
