CREATE TABLE gps_data (
    timestamp TIMESTAMP,
    tracker_id SYMBOL,
    altitude DOUBLE,
    latitude DOUBLE,
    longitude DOUBLE,
    vel_horizontal_fps DOUBLE,
    vel_vertical_fps DOUBLE,
    heading_deg DOUBLE,
    fix INT,
    sats_total INT,
    sats_ge24_dbhz INT,
    sats_ge32_dbhz INT,
    sats_ge40_dbhz INT
    ) TIMESTAMP(timestamp) PARTITION BY DAY;