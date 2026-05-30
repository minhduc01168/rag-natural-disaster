from typing import Dict, Any, Optional, Tuple, List
import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
import json

logger = logging.getLogger(__name__)

MODEL_DIR = Path(__file__).parent / "models"


class LSMModelTrainer:
    """
    Train Random Forest / XGBoost model for Landslide Susceptibility Mapping.
    
    Model được train trên Kaggle và export ra .pkl file.
    Class này load model đã train để predict real-time.
    """

    def __init__(self):
        self.model = None
        self.metadata = None
        self.encoders = None
        self.feature_columns = None
        self.trained = False
        self._load_model()

    def _load_model(self):
        """Load trained model from Kaggle output."""
        try:
            model_path = MODEL_DIR / "lsm_xgboost_model.pkl"
            metadata_path = MODEL_DIR / "model_metadata.json"
            encoders_path = MODEL_DIR / "label_encoders.pkl"

            if model_path.exists():
                import joblib
                self.model = joblib.load(model_path)
                self.metadata = json.load(open(metadata_path, encoding="utf-8"))
                self.encoders = joblib.load(encoders_path)
                self.feature_columns = self.metadata["feature_columns"]
                self.trained = True
                logger.info(
                    f"Model loaded: {self.metadata['model_name']} "
                    f"v{self.metadata['version']} "
                    f"(ROC-AUC: {self.metadata['metrics']['test_roc_auc']:.4f})"
                )
            else:
                logger.warning(
                    f"Model files not found at {model_path}. "
                    "Using mock mode. Run training notebook first."
                )
        except Exception as e:
            logger.error(f"Failed to load model: {e}")

    def prepare_features(self, gis_data: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare features and labels from GIS data.
        Returns (X, y) for training.
        
        NOTE: Chỉ dùng khi training trên Kaggle.
        Trong production, model đã được train sẵn.
        """
        try:
            n_samples = 1000
            X = np.random.rand(n_samples, len(self.feature_columns or ["elevation", "slope", "precipitation", "land_use"]))
            y = (X[:, 0] * 0.3 + X[:, 2] * 0.5 + np.random.rand(n_samples) * 0.2 > 0.5).astype(int)
            return X, y
        except Exception as e:
            logger.error(f"Feature preparation failed: {e}")
            return np.array([]), np.array([])

    def _encode_categorical(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Encode categorical features using saved label encoders."""
        if self.encoders is None:
            return features

        encoded = features.copy()

        if "soil_type" in encoded and "soil_type" in self.encoders:
            le = self.encoders["soil_type"]
            if encoded["soil_type"] in le.classes_:
                encoded["soil_encoded"] = int(le.transform([encoded["soil_type"]])[0])
            else:
                encoded["soil_encoded"] = 0
            del encoded["soil_type"]

        if "lithology" in encoded and "lithology" in self.encoders:
            le = self.encoders["lithology"]
            if encoded["lithology"] in le.classes_:
                encoded["lithology_encoded"] = int(le.transform([encoded["lithology"]])[0])
            else:
                encoded["lithology_encoded"] = 0
            del encoded["lithology"]

        if "land_use" in encoded and "land_use" in self.encoders:
            le = self.encoders["land_use"]
            if encoded["land_use"] in le.classes_:
                encoded["landuse_encoded"] = int(le.transform([encoded["land_use"]])[0])
            else:
                encoded["landuse_encoded"] = 0
            del encoded["land_use"]

        return encoded

    def _add_engineered_features(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Add engineered features matching training pipeline."""
        f = features.copy()

        slope = f.get("slope", 15)
        precip = f.get("annual_precipitation", 1500)
        elev = f.get("elevation", 300)
        fault = f.get("distance_to_fault", 5)
        river = f.get("distance_to_river", 3)

        f["slope_rainfall_interaction"] = slope * precip / 1000
        f["elevation_slope_ratio"] = elev / (slope + 1)
        f["terrain_ruggedness"] = elev * slope / 100
        f["rainfall_elevation_index"] = precip * elev / 10000
        f["fault_river_combined"] = 1 / (fault + 1) + 1 / (river + 1)

        return f

    def predict(self, features: Dict[str, Any]) -> float:
        """
        Predict susceptibility score for a single point.
        Returns score 0-1 (0 = low risk, 1 = high risk).
        """
        if not self.trained or self.model is None:
            # Mock prediction
            slope = features.get("slope", 15)
            precip = features.get("annual_precipitation", 1500)
            return min(1.0, max(0.0, (slope * 0.01 + precip * 0.0002 + np.random.rand() * 0.1)))

        try:
            # Encode categorical & add engineered features
            processed = self._encode_categorical(features)
            processed = self._add_engineered_features(processed)

            # Create DataFrame with correct feature order
            X = pd.DataFrame([processed])[self.feature_columns]

            # Predict
            score = float(self.model.predict_proba(X)[:, 1][0])
            return round(score, 4)
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return 0.5

    def predict_batch(self, features_list: List[Dict[str, Any]]) -> List[float]:
        """Predict susceptibility scores for multiple points."""
        if not self.trained or self.model is None:
            return [self.predict(f) for f in features_list]

        try:
            processed = [
                self._add_engineered_features(self._encode_categorical(f))
                for f in features_list
            ]
            X = pd.DataFrame(processed)[self.feature_columns]
            scores = self.model.predict_proba(X)[:, 1].tolist()
            return [round(s, 4) for s in scores]
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}")
            return [0.5] * len(features_list)

    def generate_lsm_grid(
        self, bounds: list, resolution: float = 0.01
    ) -> Dict[str, Any]:
        """
        Generate LSM map as GeoJSON grid.
        bounds: [min_lon, min_lat, max_lon, max_lat]
        """
        try:
            min_lon, min_lat, max_lon, max_lat = bounds

            lons = np.arange(min_lon, max_lon, resolution)
            lats = np.arange(min_lat, max_lat, resolution)

            features = []
            for lon in lons:
                for lat in lats:
                    # Trong production: lấy GIS features từ PostGIS
                    # Ở đây dùng mock data
                    point_features = {
                        "elevation": float(np.random.exponential(300)),
                        "slope": float(np.random.exponential(15)),
                        "aspect": float(np.random.uniform(0, 360)),
                        "curvature": float(np.random.normal(0, 0.5)),
                        "annual_precipitation": float(np.random.exponential(1500)),
                        "max_daily_rainfall": float(np.random.exponential(80)),
                        "rainfall_intensity": float(np.random.exponential(20)),
                        "distance_to_fault": float(np.random.exponential(5)),
                        "soil_type": "clay",
                        "lithology": "sedimentary",
                        "land_use": "forest",
                        "ndvi": float(np.random.uniform(-0.1, 0.8)),
                        "distance_to_river": float(np.random.exponential(3)),
                        "drainage_density": float(np.random.exponential(2)),
                        "distance_to_road": float(np.random.exponential(2)),
                        "population_density": float(np.random.exponential(500)),
                    }

                    susceptibility = self.predict(point_features)

                    features.append(
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [float(lon), float(lat)],
                            },
                            "properties": {
                                "susceptibility": susceptibility,
                                "risk_level": (
                                    "high"
                                    if susceptibility > 0.7
                                    else "medium" if susceptibility > 0.4 else "low"
                                ),
                            },
                        }
                    )

            return {
                "type": "FeatureCollection",
                "features": features,
                "metadata": {
                    "bounds": bounds,
                    "resolution": resolution,
                    "total_points": len(features),
                    "model_version": (
                        self.metadata.get("version", "unknown")
                        if self.metadata
                        else "mock"
                    ),
                    "generated_at": datetime.now().isoformat(),
                },
            }

        except Exception as e:
            logger.error(f"LSM grid generation failed: {e}")
            return {"type": "FeatureCollection", "features": []}

    def get_model_info(self) -> Dict[str, Any]:
        """Return model metadata for API."""
        if self.metadata:
            return {
                "loaded": True,
                "model_name": self.metadata["model_name"],
                "version": self.metadata["version"],
                "metrics": self.metadata["metrics"],
                "n_features": self.metadata["n_features"],
                "trained_at": self.metadata["trained_at"],
            }
        return {"loaded": False, "mode": "mock"}


lsm_trainer = LSMModelTrainer()
