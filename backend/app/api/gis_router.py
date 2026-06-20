from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import json

from app.db.session import get_db
from app.models.gis import SpatialFeature

router = APIRouter()

@router.get("/{layer}")
def get_gis_layer(
    layer: str,
    risk_level: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    # Query spatial features and convert geometry to GeoJSON string directly in DB
    query = db.query(
        SpatialFeature.properties,
        func.ST_AsGeoJSON(SpatialFeature.geom).label('geom_json')
    ).filter(SpatialFeature.layer_name == layer)
    
    db_features = query.all()
    
    geojson_features = []
    for f in db_features:
        props = f.properties or {}
        
        # Apply risk_level filter if provided
        if risk_level and props.get("risk_level") != risk_level:
            continue
            
        geom = json.loads(f.geom_json) if f.geom_json else None
        
        geojson_features.append({
            "type": "Feature",
            "geometry": geom,
            "properties": props
        })
        
    return {
        "type": "FeatureCollection",
        "features": geojson_features
    }
