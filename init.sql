-- ================================
-- Smart City Streaming Schema
-- ================================

DROP TABLE IF EXISTS vehicle_data CASCADE;
DROP TABLE IF EXISTS gps_data CASCADE;
DROP TABLE IF EXISTS traffic_data CASCADE;
DROP TABLE IF EXISTS weather_data CASCADE;
DROP TABLE IF EXISTS emergency_data CASCADE;

-- ----------------
-- Vehicle Data
-- ----------------
CREATE TABLE vehicle_data (
    id VARCHAR(100) PRIMARY KEY,
    device_id VARCHAR(100),
    timestamp TIMESTAMP,
    location VARCHAR(100),
    speed DOUBLE PRECISION,
    direction VARCHAR(50),
    brand VARCHAR(50),
    model VARCHAR(50),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------
-- GPS Data
-- ----------------
CREATE TABLE gps_data (
    id VARCHAR(100) PRIMARY KEY,
    device_id VARCHAR(100),
    timestamp TIMESTAMP,
    speed DOUBLE PRECISION,
    direction VARCHAR(50),
    vehicle_type VARCHAR(50),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------
-- Traffic Camera Data
-- ----------------
CREATE TABLE traffic_data (
    id VARCHAR(100) PRIMARY KEY,
    device_id VARCHAR(100),
    timestamp TIMESTAMP,
    location VARCHAR(100),
    camera_id VARCHAR(50),
    snapshot TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------
-- Weather Data
-- ----------------
CREATE TABLE weather_data (
    id VARCHAR(100) PRIMARY KEY,
    device_id VARCHAR(100),
    timestamp TIMESTAMP,
    location VARCHAR(100),
    temperature DOUBLE PRECISION,
    weather_condition VARCHAR(50),
    precipitation DOUBLE PRECISION,
    wind_speed DOUBLE PRECISION,
    humidity INTEGER,
    air_quality_index DOUBLE PRECISION,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------
-- Emergency Incidents
-- ----------------
CREATE TABLE emergency_data (
    id VARCHAR(100) PRIMARY KEY,
    device_id VARCHAR(100),
    incident_id VARCHAR(100),
    timestamp TIMESTAMP,
    location VARCHAR(100),
    type VARCHAR(50),
    status VARCHAR(50),
    description TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------
-- Indexes (Performance)
-- ----------------
CREATE INDEX idx_vehicle_timestamp ON vehicle_data(timestamp);
CREATE INDEX idx_gps_timestamp ON gps_data(timestamp);
CREATE INDEX idx_traffic_timestamp ON traffic_data(timestamp);
CREATE INDEX idx_weather_timestamp ON weather_data(timestamp);
CREATE INDEX idx_emergency_timestamp ON emergency_data(timestamp);

-- ----------------
-- Permissions
-- ----------------
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bigdata;
