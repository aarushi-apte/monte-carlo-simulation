import sys
import random
import pandas as pd


class RandomAttributeSelector():

    def __init__(self, temp, runway_surface, gross_weight, altitude, wind):
        self.temp = temp.random_temperature()
        self.runway_surface = runway_surface.random_runway_surface()
        self.gross_weight = gross_weight.random_gross_weight()
        self.altitude = altitude.random_altitude()
        self.wind = wind.random_wind()


class TemperaturePredictor:

    def __init__(self):
        self.temperature = random.choices(['sunny', 'cloudy', 'rainy', 'snowy', 'foggy', 'thunder'],
                                          weights=(80, 50, 40, 10, 5, 5), k=1)
        self.change_count = 0

    def random_temperature(self):
        if self.change_count % 200 == 0:
            self.temperature = random.choices(['sunny', 'cloudy', 'rainy', 'snowy', 'foggy', 'thunder'],
                                              weights=(80, 50, 40, 10, 5, 5), k=1)

        self.change_count += 1
        return self.temperature[0]


class RunwaySurfacePredictor:

    def __init__(self):
        self.runway_surface = random.choices(['normal', 'wet', 'standing_water', 'snow', 'icy'],
                                             weights=(80, 60, 40, 30, 22), k=1)
        self.change_count = 0

    def random_runway_surface(self):
        if self.change_count % 10 == 0:
            self.runway_surface = random.choices(['normal', 'wet', 'standing_water', 'snow', 'icy'],
                                             weights=(80, 60, 40, 30, 22), k=1)

        self.change_count += 1
        return self.runway_surface[0]


class GrossWeightPredictor:

    # https://www.portofbellingham.com/DocumentCenter/View/7196/Revised-Runway-Length-Discussion-20171206?bidId=
    # Boeing 737-800 is the most widely used hence the max weightage -
    # https://en.wikipedia.org/wiki/Boeing_737#:~:text=The%20%2D800%20replaced%20directly%20the,primarily%20with%20the%20Airbus%20A320.
    def __init__(self):
        self.gross_weight = random.choices(['light', 'medium', 'heavy', 'super'], weights=(40, 50, 30, 20), k=1)
        self.change_count = 0

    def random_gross_weight(self):
        if self.change_count % 3 == 0:
            self.gross_weight = random.choices(['light', 'medium', 'heavy', 'super'], weights=(40, 50, 30, 20), k=1)

        self.change_count += 1
        return self.gross_weight[0]


class AltitudePredictor:
    # The lowest non-negative altitude airport in The US
    # https://www.boldmethod.com/blog/lists/2014/10/7-lowest-civilian-airports-us/
    # The highest altitude airport in The US
    # https://www.boldmethod.com/blog/lists/2014/08/10-highest-airports-in-the-united-states/
    def __init__(self):
        self.altitude = random.randint(0, 9934)
        self.change_count = 0

    def random_altitude(self):
        if self.change_count % 10 == 0:
            self.altitude = random.randint(0, 9934)

        self.change_count += 1
        return self.altitude


class WindPredictor:

    def __init__(self):
        self.wind = []

    def random_wind(self):
        self.wind = random.choices(['headwind', 'tailwind', 'crosswind', 'gust'], weights=(80, 40, 10, 8), k=1)
        return self.wind[0]


def altitude_calculation():
    if altitude <= 8000:
        distance_percent = (altitude / 1000) * 0.12
    else:
        distance_percent = 0.96
        distance_percent = distance_percent - ((altitude - 8000) / 1000) * 0.20

def effect_by_temp(temp):
    distance_percent = (temp/10) * .10
    return distance_percent


def effect_by_runway_surface(runway_surface):
    if runway_surface == "normal":
        distance_percent = 1.01
    elif runway_surface == "wet":
        distance_percent = 1.013
    elif runway_surface == "standing_water":
        distance_percent = 1.0165
    elif runway_surface == "snowy":
        distance_percent = 1.0215
    else:
        distance_percent = 1.04
    return distance_percent


def effect_by_gross_weight(mean_weight, gross_weight):
    # Weight limitations - https://simpleflying.com/boeing-737-family-variants-weight-differences/

    # Boeing 737-700
    if gross_weight == "light":
        min_weight = 83000
        max_weight = 154500
        flight_weight = random.randint(min_weight, max_weight)
    # Boeing 737-800
    elif gross_weight == "medium":
        min_weight = 91300
        max_weight = 174200
        flight_weight = random.randint(min_weight, max_weight)
    # Boeing 737-900
    elif gross_weight == "heavy":
        min_weight = 93680
        max_weight = 187679
        flight_weight = random.randint(min_weight, max_weight)
    # Boeing 737-900ER
    else:
        min_weight = 98495
        max_weight = 187700
        flight_weight = random.randint(min_weight, max_weight)

    weight = flight_weight - min_weight

    # https://www.experimentalaircraft.info/flight-planning/aircraft-performance-7.php
    if weight > 0:
        weight_percent = (weight * 100) / mean_weight
        distance_percent = (weight_percent * 2) / 100
    return distance_percent


def effect_by_altitude(altitude):
    if altitude <= 8000:
        distance_percent = (altitude / 1000) * 0.12
    else:
        distance_percent = 0.96
        distance_percent = distance_percent - ((altitude - 8000) / 1000) * 0.20
    return distance_percent


def effect_by_wind(wind, wind_speed):
    # https://www.aviation.govt.nz/assets/publications/gaps/Take-off-and-landing-performance.pdf
    if wind == "headwind":
        max_headwind = 20
        wind_speed = random.randint(0, max_headwind)
        total_percent = 1.5 * wind_speed
        distance_percent = (100 - total_percent) / 100
    elif wind == "tailwind":
        possible_values = [5,10]
        wind_speed = random.choice(possible_values)
        if wind_speed == 5:
            distance_percent = 1.25
        else:
            distance_percent =  1.55
    elif wind == "crosswind":
        pass
    else:
        pass
    return distance_percent


if __name__ == '__main__':

    meanDistance = 6000

    weight_input = input(
        "Hi, Please inout the weight from the below chooses to get the optimum distance of take off - \n1) light and fully filled \n"
        "2) light and medium filled \n"
        "3) light and lightly filled \n"
        "4)medium and fully filled \n"
        "5)medium and medium filled \n"
        "6)medium and lightly filled \n"
        "7)heavy and fully filled \n"
        "8)heavy and medium filled \n"
        "9)heavy and lightly filled \n"
        "10)super and fully filled \n"
        "11)super and medium filled \n"
        "12)super and lightly filled \n")
    temp = TemperaturePredictor()
    runway_surface = RunwaySurfacePredictor()
    gross_weight = GrossWeightPredictor()
    altitude = AltitudePredictor()
    wind = WindPredictor()

    hypo1_optimum_dist_header = ['temperature', 'runway_surface', 'gross_weight', 'altitude', 'wind', 'distance']
    df_for_hypo1 = pd.DataFrame(columns=hypo1_optimum_dist_header)
    hypo1_distance_list = []

    for times in range(1, 5001):
        randomSelector = RandomAttributeSelector(temp, runway_surface, gross_weight, altitude, wind)
        randomAttributeMap = randomSelector.__dict__
        effect_by_temp = effect_by_temp(randomAttributeMap['temp'])
        effect_by_runway_surface = effect_by_runway_surface(randomAttributeMap['runway_surface'])
        effect_by_gross_weight = effect_by_gross_weight(randomAttributeMap['gross_weight'])
        effect_by_altitude = effect_by_altitude(randomAttributeMap['altitude'])
        effect_by_wind = effect_by_wind(randomAttributeMap['wind'])
        distance = meanDistance * effect_by_temp * effect_by_runway_surface * effect_by_gross_weight * effect_by_altitude * effect_by_wind

        hypo1_distance_list.append(distance)

        df_data = [randomAttributeMap['temp'],randomAttributeMap['runway_surface'], randomAttributeMap['gross_weight'], randomAttributeMap['altitude'],
                     randomAttributeMap['wind'], distance]
        columns = pd.Series(df_data, index=df_for_hypo1.columns)
        df_for_hypo1 = df_for_hypo1.append(columns, ignore_index=True)


