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
        # https://www.washingtonpost.com/news/capital-weather-gang/wp/2018/07/27/sometimes-its-too-hot-for-airplanes-to-fly-heres-why/#:~:text=Every%20plane%20has%20a%20different,at%20more%20than%20174%2C200%20pounds.
        # https://www.cntraveler.com/stories/2016-06-20/its-so-hot-some-planes-cant-fly-heres-why
        self.temperature = random.randint(-55, 54)
        self.change_count = 0

    def random_temperature(self):
        if self.change_count % 200 == 0:
            self.temperature = random.randint(-55, 54)

        self.change_count += 1
        return self.temperature


class RunwaySurfacePredictor:

    def __init__(self):
        self.runway_surface = random.choices(['normal', 'wet', 'standing_water', 'snow', 'icy'], weights=(80, 60, 40,
                                                                                                          30, 22), k=1)
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
    # # https://en.wikipedia.org/wiki/List_of_highest_airports
    def __init__(self):
        self.altitude = random.randint(0, 14472)
        self.change_count = 0

    def random_altitude(self):
        if self.change_count % 10 == 0:
            self.altitude = random.randint(0, 14472)

        self.change_count += 1
        return self.altitude


class WindPredictor:

    def __init__(self):
        self.wind = []

    def random_wind(self):
        self.wind = random.choices(['headwind', 'tailwind', 'crosswind'], weights=(80, 40, 10), k=1)
        return self.wind[0]


class GradientPredictor:

    def __init__(self):
        # https://www.insider.com/worlds-most-terrifying-airport-runways-2016-7#courchevel-airport-in-courchevel-france-has-an-incredibly-steep-runway-that-ends-in-a-sheer-rock-face-drop-14
        self.gradient = random.uniform(0, 18.5)
        self.change_count = 0

    def random_temperature(self):
        if self.change_count % 100 == 0:
            self.gradient = random.uniform(0, 18.5)

        self.change_count += 1
        return self.gradient


def effect_by_temp(temperature):
    # https://www.experimentalaircraft.info/flight-planning/aircraft-performance-7.php
    isa_base = 15
    if temperature < 15:
        temp_diff = abs(abs(temperature) - isa_base)
        distance_percent = 1 - (temp_diff / 100)
    elif temperature > 15:
        temp_diff = temperature - isa_base
        distance_percent = 1 + (temp_diff / 100)
    else:
        distance_percent = 0
    return distance_percent


def effect_by_runway_surface(runway_surface):
    if runway_surface == "normal":
        distance_percent = 0
    elif runway_surface == "wet":
        distance_percent = 1.013
    elif runway_surface == "standing_water":
        # https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range
        perc = random.uniform(2, 2.4)
        distance_percent = 1 + (perc / 100)
    elif runway_surface == "snowy":
        perc = random.uniform(1.6, 1.7)
        distance_percent = 1 + (perc / 100)
    else:
        perc = random.uniform(3.5, 4.5)
        distance_percent = 1 + (perc / 100)
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
    # https://www.mountainflying.com/pages/mountain-flying/rule_of_thumb.html
    if altitude <= 8000:
        distance_percent = ((altitude / 1000) * 0.12) + 1
    else:
        distance_percent = 1.96
        distance_percent = (distance_percent + ((altitude - 8000) / 1000) * 0.20)
    return distance_percent


def effect_by_wind(wind):
    # https://www.aviation.govt.nz/assets/publications/gaps/Take-off-and-landing-performance.pdf
    def calculating_wind(max_wind):
        speed = random.randint(0, max_wind)
        return speed

    if wind == "headwind":
        wind_speed = calculating_wind(20)
        total_percent = 1.5 * wind_speed
        distance_percent = (100 - total_percent) / 100

    elif wind == "tailwind":
        wind_speed = calculating_wind(10)
        if wind_speed <= 5:
            distance_percent = 1.25
        else:
            distance_percent = 1.55
    # https://pilotworkshop.com/tips/quick-crosswind-calculation/
    elif wind == "crosswind":
        angle_value = [0.17, 0.25, 0.34, 0.5, 0.75, 1]
        crosswind_angle = random.choice(angle_value)
        wind_speed = calculating_wind(35)
        crosswind = wind_speed * crosswind_angle
        if crosswind > 0:
            distance_percent = 0.85
        else:
            distance_percent = 0
    return distance_percent


def effect_by_gradient(runway_gradient, alt):
    # https://www.portofbellingham.com/DocumentCenter/View/7196/Revised-Runway-Length-Discussion-20171206?bidId=
    gradient_diff = (runway_gradient * alt) / 100
    add_distance = gradient_diff * 10
    return add_distance


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
    gradient = GradientPredictor()

    hypo1_optimum_dist_header = ['temperature', 'runway_surface', 'gross_weight', 'altitude', 'wind', 'distance',
                                 'gradient']
    df_for_hypo1 = pd.DataFrame(columns=hypo1_optimum_dist_header)
    hypo1_distance_list = []

    for times in range(1, 5001):
        randomSelector = RandomAttributeSelector(temp, runway_surface, gross_weight, altitude, wind, gradient)
        randomAttributeMap = randomSelector.__dict__
        effect_by_temp = effect_by_temp(randomAttributeMap['temp'])
        effect_by_runway_surface = effect_by_runway_surface(randomAttributeMap['runway_surface'])
        effect_by_gross_weight = effect_by_gross_weight(randomAttributeMap['gross_weight'])
        effect_by_altitude = effect_by_altitude(randomAttributeMap['altitude'])
        effect_by_wind = effect_by_wind(randomAttributeMap['wind'])
        effect_by_gradient = effect_by_gradient(randomAttributeMap['gradient'], randomAttributeMap['altitude'])
        distance = (meanDistance * effect_by_temp * effect_by_runway_surface * effect_by_gross_weight * \
                   effect_by_altitude * effect_by_wind) + effect_by_gradient

        hypo1_distance_list.append(distance)

        df_data = [randomAttributeMap['temp'],randomAttributeMap['runway_surface'], randomAttributeMap['gross_weight'], randomAttributeMap['altitude'],
                     randomAttributeMap['wind'], randomAttributeMap['gradient'], distance]
        columns = pd.Series(df_data, index=df_for_hypo1.columns)
        df_for_hypo1 = df_for_hypo1.append(columns, ignore_index=True)


