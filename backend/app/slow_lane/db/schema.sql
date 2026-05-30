-- PostGIS Schema for TerraAlert
-- Enable PostGIS extension

CREATE EXTENSION IF NOT EXISTS postgis;

-- Elevation data table
CREATE TABLE IF NOT EXISTS elevation (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Point, 4326) NOT NULL,
    elevation FLOAT NOT NULL,
    source VARCHAR(50) DEFAULT 'srtm',
    fetched_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create spatial index for elevation
CREATE INDEX IF NOT EXISTS idx_elevation_geom ON elevation USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_elevation_source ON elevation (source);

-- Precipitation data table
CREATE TABLE IF NOT EXISTS precipitation (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Point, 4326) NOT NULL,
    amount FLOAT NOT NULL,
    date DATE NOT NULL,
    source VARCHAR(50) DEFAULT 'gpm',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create spatial index for precipitation
CREATE INDEX IF NOT EXISTS idx_precipitation_geom ON precipitation USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_precipitation_date ON precipitation (date);

-- Disasters history table
CREATE TABLE IF NOT EXISTS disasters (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Geometry, 4326) NOT NULL,
    type VARCHAR(100) NOT NULL,
    severity VARCHAR(50),
    date DATE,
    description TEXT,
    affected_population INTEGER,
    source VARCHAR(50) DEFAULT 'hdx',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create spatial index for disasters
CREATE INDEX IF NOT EXISTS idx_disasters_geom ON disasters USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_disasters_type ON disasters (type);
CREATE INDEX IF NOT EXISTS idx_disasters_date ON disasters (date);

-- LSM predictions table
CREATE TABLE IF NOT EXISTS lsm_predictions (
    id SERIAL PRIMARY KEY,
    geom GEOMETRY(Point, 4326) NOT NULL,
    susceptibility FLOAT NOT NULL CHECK (susceptibility >= 0 AND susceptibility <= 1),
    risk_level VARCHAR(20) NOT NULL,
    model_version VARCHAR(50),
    predicted_at TIMESTAMP DEFAULT NOW()
);

-- Create spatial index for LSM predictions
CREATE INDEX IF NOT EXISTS idx_lsm_geom ON lsm_predictions USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_lsm_risk ON lsm_predictions (risk_level);

-- Model metadata table
CREATE TABLE IF NOT EXISTS ml_models (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    accuracy FLOAT,
    features_used TEXT[],
    trained_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT FALSE,
    model_path VARCHAR(500)
);

-- Create index for model version
CREATE INDEX IF NOT EXISTS idx_models_name ON ml_models (model_name);
CREATE INDEX IF NOT EXISTS idx_models_active ON ml_models (is_active);
