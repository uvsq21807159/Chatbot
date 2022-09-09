CREATE TABLE Pollution (
    loc NVARCHAR(256),
    timestamp NVARCHAR(256),
    aqi FLOAT NOT NULL,
    co FLOAT NOT NULL,
    no FLOAT NOT NULL,
    no2 FLOAT NOT NULL,
    o3 FLOAT NOT NULL,
    so2 FLOAT NOT NULL,
    nh3 FLOAT NOT NULL,
    pm2_5 FLOAT NOT NULL,
    pm10 FLOAT NOT NULL,
    CONSTRAINT pk_pollution PRIMARY KEY(loc, timestamp)
);