SELECT
    CAST(loc AS NVARCHAR(max)) loc, 
    CAST(dt AS NVARCHAR(max)) timestamp, aqi, co, no, no2, o3, so2, nh3, pm2_5, pm10
INTO
    [pollutiondb]
FROM
    [datahub]