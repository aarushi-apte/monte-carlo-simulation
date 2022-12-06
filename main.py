import sys
import random
import pandas as pd


class RandomAttributeSelector():

    def __init__(self, temp, runway_surface, gross_weight, altitude, wind, gradient,year):
        self.temp = temp.random_temperature(year)
        self.runway_surface = runway_surface.random_runway_surface()
        self.gross_weight = gross_weight.random_gross_weight()
        self.altitude = altitude.random_altitude()
        self.wind = wind.random_wind()
        self.gradient = gradient.random_gradient()


class TemperaturePredictor:

    def __init__(self):
        # https://www.washingtonpost.com/news/capital-weather-gang/wp/2018/07/27/sometimes-its-too-hot-for-airplanes-to-fly-heres-why/#:~:text=Every%20plane%20has%20a%20different,at%20more%20than%20174%2C200%20pounds.
        # https://www.cntraveler.com/stories/2016-06-20/its-so-hot-some-planes-cant-fly-heres-why
        self.temperature = []

    def random_temperature(self, year):
        #min max temp in 2000
        minRange = -13
        maxRange = 40

        #every decade an expected increase in 0.25Deg celsius
        decade_diff = (year - 2000)/10
        minRange += decade_diff * 0.25
        maxRange += decade_diff * 0.25
        self.temperature = random.randint(int(minRange), int(maxRange))
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
        if self.change_count % 1 == 0:
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
        self.gradient = random.uniform(50, 100)
        self.change_count = 0

    def random_gradient(self):
        if self.change_count % 10 == 0:
            self.gradient = random.randint(50, 100)

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
        distance_percent = 1
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


def effect_by_gross_weight(gross_weight):
    # Weight limitations - https://simpleflying.com/boeing-737-family-variants-weight-differences/
    # https://www.experimentalaircraft.info/flight-planning/aircraft-performance-7.php
    def weight_distance_calculator(min_weight, max_weight, min_runway):
        flight_weight = random.randint(min_weight, max_weight)
        weight_diff = flight_weight - min_weight
        if weight_diff > 0:
            weight_percent = weight_diff / min_weight
            dist_to_add = ((weight_percent * 2) / 100) * min_runway
        else:
            dist_to_add = 0
        return dist_to_add

    # Boeing 737-700
    if gross_weight == "light":
        distance_add = weight_distance_calculator(83000, 154500, 5315)
    # Boeing 737-800
    elif gross_weight == "medium":
        distance_add = weight_distance_calculator(91300, 174200, 6791)
    # Boeing 737-900
    elif gross_weight == "heavy":
        distance_add = weight_distance_calculator(93680, 187679, 6791)
    # Boeing 737-900ER
    else:
        distance_add = weight_distance_calculator(98495, 187700, 6791)

    return distance_add


def effect_by_altitude(altitude):
    distance_percent = (0.007 * (altitude / 985)) + 1
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


def effect_by_gradient(runway_gradient):
    # https://www.portofbellingham.com/DocumentCenter/View/7196/Revised-Runway-Length-Discussion-20171206?bidId=

    distance_to_add = runway_gradient * 10
    return distance_to_add


if __name__ == '__main__':

    year = int(input('Please type a year for which you would like to know the estimated mean take off distance.'
                     '\nWe will randomise temperature, runway surface, gross weight, altitute of the airpord, wind and runway gradient.'))

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
        randomSelector = RandomAttributeSelector(temp, runway_surface, gross_weight, altitude, wind, gradient, year)
        randomAttributeMap = randomSelector.__dict__

        if randomAttributeMap['gross_weight'] == 'light':
            min_distance = 5315
        else:
            min_distance = 6791

        temp_effect = effect_by_temp(randomAttributeMap['temp'])
        runway_surface_effect = effect_by_runway_surface(randomAttributeMap['runway_surface'])
        gross_weight_effect = effect_by_gross_weight(randomAttributeMap['gross_weight'])
        altitude_effect = effect_by_altitude(randomAttributeMap['altitude'])
        wind_effect = effect_by_wind(randomAttributeMap['wind'])
        gradient_effect = effect_by_gradient(randomAttributeMap['gradient'])
        distance = (min_distance * temp_effect * runway_surface_effect * wind_effect * altitude_effect
                    ) + gross_weight_effect + gradient_effect

        if distance < min_distance:
            # Not an optimum condition to fly
            continue

        hypo1_distance_list.append(distance)

        df_data = [randomAttributeMap['temp'], randomAttributeMap['runway_surface'], randomAttributeMap['gross_weight'],
                   randomAttributeMap['altitude'],
                   randomAttributeMap['wind'], randomAttributeMap['gradient'], distance]
        columns = pd.Series(df_data, index=df_for_hypo1.columns)
        df_for_hypo1 = df_for_hypo1.append(columns, ignore_index=True)

    df_for_hypo1.to_csv('hypo1.csv')

    print(sum(hypo1_distance_list) / len(hypo1_distance_list))

    hypo2_temp_effect = effect_by_temp(40)
    hypo2_runway_surface_effect = effect_by_runway_surface('icy')
    hypo2_gross_weight_effect = effect_by_gross_weight(randomAttributeMap['gross_weight'])
    hypo2_altitude_effect = effect_by_altitude(14472)
    hypo2_wind_effect = effect_by_wind('tailwind')
    hypo2_gradient_effect = effect_by_gradient(randomAttributeMap['gradient'])
    hypo2_distance = (min_distance * temp_effect * runway_surface_effect * wind_effect * altitude_effect
                ) + gross_weight_effect + gradient_effect
    max_change_at_extreme = (hypo2_distance - min_distance)/min_distance * 100
    print(max_change_at_extreme)


# notes-

# Hypo1-
# the optimum runway distance at a perticular year. (input - year /  output - takeoff distance)

# the optimum runway distance at an extreme condition would not deffer by xyz ft or will not be more than xyz feet.
