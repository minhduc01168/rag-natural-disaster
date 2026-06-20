from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from app.db.session import Base

class SpatialFeature(Base):
    __tablename__ = "spatial_features"

    id = Column(Integer, primary_key=True, index=True)
    layer_name = Column(String, index=True, nullable=False) # 'lsm', 'disasters', 'elevation'
    properties = Column(JSONB, default={})
    geom = Column(Geometry(geometry_type='GEOMETRY', srid=4326))
