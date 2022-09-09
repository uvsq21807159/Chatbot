import calendar
import datetime as dt

NOW = "DATEDIFF(second, '19700101', sysutcdatetime())"
HOUR = "DATEPART(hour, (DATEADD(second, convert(INT, timestamp), '1970-01-01')))"
DAY = "DATEPART(weekday, (DATEADD(second, convert(INT, timestamp), '1970-01-01')))"

def AQI(column) :
    if (column == 1.0):
        return 'good'
    if (column == 2.0):
        return 'fair'
    if (column == 3.0):
        return 'moderate'
    if (column == 4.0):
        return 'poor'
    if (column == 5.0):
        return 'very poor'

def current_data(row):
    return (
        "At "
        + str(row[0])
        + ", the AQI(="
        + str(round(row[2], 2))
        + ") is "
        + AQI(row[2])
        + ": <br />\n CO="
        + str(round(row[3], 2))
        + ", NO="
        + str(round(row[4], 2))
        + ", NO2="
        + str(round(row[5], 2))
        + ", O3="
        + str(round(row[6], 2))
        + ", SO2="
        + str(round(row[7], 2))
        + ", NH3="
        + str(round(row[8], 2))
        + ", PM2.5="
        + str(round(row[9], 2))
        + ", PM10="
        + str(round(row[10], 2))
    )


# tag = function name


def recent_news(cursor):
    response = ""
    request = (
        "SELECT * FROM Pollution WHERE timestamp <= "
        + NOW
        + " AND timestamp > "
        + NOW
        + " - 3600"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        response += current_data(row) + "<br />\n"
        row = cursor.fetchone()
    print(response)
    return response


def loc_ranking(cursor):
    response = "The average AQIs of cities are the following ones:"
    request = "SELECT loc, AVG(aqi) aqi FROM Pollution GROUP BY loc ORDER BY aqi DESC"
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        response += "<br />\n" + str(row[0]) + " : " + str(round(row[1], 2))
        row = cursor.fetchone()
    return response


def hour_ranking(cursor):
    response = "Here is the average AQI according to the time of the day: "
    request = (
        "SELECT "
        + HOUR
        + " hour, AVG(aqi) aqi FROM Pollution GROUP BY "
        + HOUR
        + " ORDER BY hour"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    for hour in range(24):
        if (hour < 13) :
            response += "<br />\n" + str(hour) + "AM : " + str(round(row[1], 2))
        else :
            response += "<br />\n" + str(hour - 12) + "PM : " + str(round(row[1], 2))
        row = cursor.fetchone()
    return response


def day_ranking(cursor):
    response = "Here is the average AQI according to the day of the week:"
    request = (
        "SELECT "
        + DAY
        + " day, AVG(aqi) aqi FROM Pollution GROUP BY "
        + DAY
        + " ORDER BY day"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        response += (
            "<br />\n" + calendar.day_name[int(row[0]) - 1] + " : " + str(round(row[1], 2))
        )
        row = cursor.fetchone()
    return response


def max_pollution_hour(cursor):
    avg_pollution_hour = (
        "(SELECT "
        + HOUR
        + " hour, AVG(aqi) aqi_h FROM Pollution GROUP BY "
        + HOUR
        + ") P"
    )
    request = (
        "SELECT hour, aqi_h FROM "
        + avg_pollution_hour
        + " INNER JOIN (SELECT MAX(aqi_h) aqi FROM "
        + avg_pollution_hour
        + ") M ON (aqi_h = aqi)"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        if (row[0] < 13):
            return (
                "The pollution peak is often reached around "
                + str(row[0])
                + "AM with an AQI of "
                + str(round(row[1], 2))
            )
        else:
            return (
                "The pollution peak is often reached around "
                + str(int(row[0]) - 12)
                + "PM with an AQI of "
                + str(round(row[1], 2))
            )



def min_pollution_hour(cursor):
    avg_pollution_hour = (
        "(SELECT "
        + HOUR
        + " hour, AVG(aqi) aqi_h FROM Pollution GROUP BY "
        + HOUR
        + ") P"
    )
    request = (
        "SELECT hour, aqi_h FROM "
        + avg_pollution_hour
        + " INNER JOIN (SELECT MIN(aqi_h) aqi FROM "
        + avg_pollution_hour
        + ") M ON (aqi_h = aqi)"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        if (row[0] < 13):
            return (
                "Pollution is lowest around "
                + str(row[0])
                + "AM with an AQI of "
                + str(round(row[1], 2))
            )
        else:
            return (
                "Pollution is lowest around "
                + str(int(row[0]) - 12)
                + "PM with an AQI of "
                + str(round(row[1], 2))
            )


def max_pollution_day(cursor):
    avg_pollution_day = (
        "(SELECT " + DAY + " day, AVG(aqi) aqi_d FROM Pollution GROUP BY " + DAY + ") P"
    )
    request = (
        "SELECT day, aqi_d FROM "
        + avg_pollution_day
        + " INNER JOIN (SELECT MAX(aqi_d) aqi FROM "
        + avg_pollution_day
        + ") M ON (aqi_d = aqi)"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        return (
            "The pollution peak is often reached on "
            + calendar.day_name[int(row[0]) - 1]
            + " with an AQI of "
            + str(round(row[1], 2))
        )


def min_pollution_day(cursor):
    avg_pollution_day = (
        "(SELECT " + DAY + " day, AVG(aqi) aqi_d FROM Pollution GROUP BY " + DAY + ") P"
    )
    request = (
        "SELECT day, aqi_d FROM "
        + avg_pollution_day
        + " INNER JOIN (SELECT MIN(aqi_d) aqi FROM "
        + avg_pollution_day
        + ") M ON (aqi_d = aqi)"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        return (
            "The pollution is lowest on "
            + calendar.day_name[int(row[0]) - 1]
            + " with an AQI of "
            + str(round(row[1], 2))
        )


def wrong_place_wrong_time(cursor):
    response = "The air quality index is poor at :"
    request = (
        "SELECT DISTINCT loc, "
        + HOUR
        + " hour, AVG(aqi) aqi FROM Pollution GROUP BY loc, "
        + HOUR
        + " HAVING AVG(aqi) >= 3 ORDER BY loc"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        if(row[1] < 13):
            response += (
                "<br />\n"
                + str(row[0])
                + " at "
                + str(row[1])
                + "AM with an AQI of "
                + str(round(row[2], 2))
            )
        else :
            response += (
                "<br />\n"
                + str(row[0])
                + " at "
                + str(row[1])
                + "PM with an AQI of "
                + str(round(row[2], 2))
            )
        row = cursor.fetchone()
    return response


def wrong_place_wrong_date(cursor):
    response = "The air quality index was very poor (AQI=5) at :"
    request = "SELECT  loc, timestamp, aqi FROM Pollution WHERE aqi = 5"
    cursor.execute(request)
    row = cursor.fetchone()
    while row:
        date = dt.datetime.fromtimestamp(int(row[1]))
        response += "<br />\n" + str(row[0]) + " -> " + str(date)
        row = cursor.fetchone()
    return response


def versailles_current_pollution(cursor):
    response = "The pollution "
    request = (
        "SELECT * FROM Pollution WHERE loc = 'Versailles' AND timestamp <= "
        + NOW
        + " AND timestamp > "
        + NOW
        + " - 3600"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    return current_data(row)


def lille_current_pollution(cursor):
    response = "The pollution "
    request = (
        "SELECT * FROM Pollution WHERE loc = 'Lille' AND timestamp <= "
        + NOW
        + " AND timestamp > "
        + NOW
        + " - 3600"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    return current_data(row)


def nice_current_pollution(cursor):
    response = "The pollution "
    request = (
        "SELECT * FROM Pollution WHERE loc = 'Nice' AND timestamp <= "
        + NOW
        + " AND timestamp > "
        + NOW
        + " - 3600"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    return current_data(row)


def brest_current_pollution(cursor):
    response = "The pollution "
    request = (
        "SELECT * FROM Pollution WHERE loc = 'Brest' AND timestamp <= "
        + NOW
        + " AND timestamp > "
        + NOW
        + " - 3600"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    return current_data(row)


def bayonne_current_pollution(cursor):
    response = "The pollution "
    request = (
        "SELECT * FROM Pollution WHERE loc = 'Bayonne' AND timestamp <= "
        + NOW
        + " AND timestamp > "
        + NOW
        + " - 3600"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    return current_data(row)


def strasbourg_current_pollution(cursor):
    request = (
        "SELECT * FROM Pollution WHERE loc = 'Strasbourg' AND timestamp <= "
        + NOW
        + " AND timestamp > "
        + NOW
        + " - 3600"
    )
    cursor.execute(request)
    row = cursor.fetchone()
    return current_data(row)
