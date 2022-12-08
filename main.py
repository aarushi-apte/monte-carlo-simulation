import random
import pandas as pd
from geographiclib.geodesic import Geodesic

geod = Geodesic.WGS84


class RandomAttributeSelector():

    def __init__(self, temp, runway_surface, gross_weight, altitude, wind, gradient, gross_weight_fixed,
                 gross_weight_to_be_changed=False):
        self.temp = temp.random_temperature()
        self.runway_surface = runway_surface.random_runway_surface()
        if gross_weight_to_be_changed:
            self.gross_weight = gross_weight.random_gross_weight()
        else:
            self.gross_weight = gross_weight_fixed
        self.altitude = altitude.random_altitude()
        self.wind = wind.random_wind()
        self.gradient = gradient.random_gradient()


class TemperaturePredictor:

    def __init__(self):
        # https://www.washingtonpost.com/news/capital-weather-gang/wp/2018/07/27/sometimes-its-too-hot-for-airplanes-to-fly-heres-why/#:~:text=Every%20plane%20has%20a%20different,at%20more%20than%20174%2C200%20pounds.
        # https://www.cntraveler.com/stories/2016-06-20/its-so-hot-some-planes-cant-fly-heres-why
        self.temperature = []

    def random_temperature(self):
        minRange = -13
        maxRange = 40

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
    # choose from a dataset
    # if not this should "median of all 1000ft,  pert distribution.

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
    if temperature < isa_base:
        temp_diff = (abs(temperature - isa_base)) / 10
        distance_percent = 1 - (0.05 * temp_diff)
    elif temperature > isa_base:
        temp_diff = (temperature - isa_base) / 10
        distance_percent = 1 + (0.05 * temp_diff)
    else:
        distance_percent = 1
    return distance_percent


def effect_by_runway_surface(runway_surface):
    if runway_surface == "normal":
        distance_multiply = 1
    elif runway_surface == "wet":
        # https://stackoverflow.com/questions/6088077/how-to-get-a-random-number-between-a-float-range
        distance_multiply = random.uniform(1.3, 1.4)
    elif runway_surface == "standing_water":
        distance_multiply = random.uniform(2, 2.3)
    elif runway_surface == "snowy":
        distance_multiply = random.uniform(1.6, 1.7)
    else:
        distance_multiply = random.uniform(3.5, 4.5)
    return distance_multiply


def effect_by_gross_weight(gross_weight):
    # Weight limitations - https://simpleflying.com/boeing-737-family-variants-weight-differences/
    # https://www.experimentalaircraft.info/flight-planning/aircraft-performance-7.php
    def weight_distance_calculator(min_weight, max_weight, min_runway):
        flight_weight = random.randint(min_weight, max_weight)
        weight_diff = flight_weight - min_weight
        if weight_diff > 0:
            weight_percent = weight_diff / min_weight
            dist_to_add = weight_percent * min_runway
        else:
            dist_to_add = 0
        return dist_to_add

    # Boeing 737-700
    if gross_weight == "light":
        distance_add = weight_distance_calculator(83000, 129200, 4800)
    # Boeing 737-800
    elif gross_weight == "medium":
        distance_add = weight_distance_calculator(91300, 146300, 5800)
    # Boeing 737-900
    elif gross_weight == "heavy":
        distance_add = weight_distance_calculator(93680, 147300, 5800)
    # Boeing 737-900ER
    else:
        distance_add = weight_distance_calculator(98495, 138450, 5800)

    return distance_add


def effect_by_altitude(altitude):
    # https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak/media/13_phak_ch11.pdf
    distance_multiply = (0.035 * (altitude / 1000)) + 1
    return distance_multiply


def effect_by_wind(wind):
    # https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak/media/13_phak_ch11.pdf
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


def random_direction():
    return (round(random.uniform(-90, 90), 5),
            round(random.uniform(-180, 180), 5))


def get_sign(direction):
    if direction == 'W' or direction == 'S':
        return -1
    return 1


def create_lat_long(lat_long):
    return lat_long[:2] + '.' + lat_long[2:]


def mc_simulation(randomAttributeMap):
    if randomAttributeMap['gross_weight'] == 'light':
        min_distance = 4800
    else:
        min_distance = 5800

    temp_effect = effect_by_temp(randomAttributeMap['temp'])
    runway_surface_effect = effect_by_runway_surface(randomAttributeMap['runway_surface'])
    gross_weight_effect = effect_by_gross_weight(randomAttributeMap['gross_weight'])
    altitude_effect = effect_by_altitude(randomAttributeMap['altitude'])
    wind_effect = effect_by_wind(randomAttributeMap['wind'])
    gradient_effect = effect_by_gradient(randomAttributeMap['gradient'])
    ld = (min_distance * temp_effect * runway_surface_effect * wind_effect * altitude_effect
          ) + gross_weight_effect + gradient_effect
    return ld, randomAttributeMap


if __name__ == '__main__':

    # imported Df
    airport_df = pd.read_excel("airport_info.xlsx")

    # classes called
    temp = TemperaturePredictor()
    runway_surface = RunwaySurfacePredictor()
    gross_weight = GrossWeightPredictor()
    altitude = AltitudePredictor()
    wind = WindPredictor()
    gradient = GradientPredictor()

    # Hypo 1

    hypo1_header = ['temperature', 'runway_surface', 'gross_weight', 'altitude', 'wind', 'gradient',
                    'accommodating_airports', 'accommodating airports']
    df_for_hypo1 = pd.DataFrame(columns=hypo1_header)

    for times in range(1, 1001):
        randomSelector = RandomAttributeSelector(temp, runway_surface, gross_weight, altitude, wind, gradient, None,
                                                 True)
        randomAttributeMap = randomSelector.__dict__
        ld, randomAttributeMap = mc_simulation(randomAttributeMap)
        accommodating_airports = airport_df[airport_df['Length (ft)'] * 0.6 >= ld].shape[0]
        total_airports = airport_df.shape[0]
        percent_of_accommodating_airport = (accommodating_airports / total_airports) * 100

        df_data = [randomAttributeMap['temp'], randomAttributeMap['runway_surface'], randomAttributeMap['gross_weight'],
                   randomAttributeMap['altitude'],
                   randomAttributeMap['wind'], randomAttributeMap['gradient'], accommodating_airports,
                   percent_of_accommodating_airport]
        columns = pd.Series(df_data, index=df_for_hypo1.columns)
        df_for_hypo1 = df_for_hypo1.append(columns, ignore_index=True)

    df_for_hypo1.to_csv('hypo1.csv')

    # Hypo 2

    random_lat, random_long = random_direction()
    airports_in_vicinity_df_header = airport_df.columns
    airports_in_vicinity_df = pd.DataFrame(columns=airports_in_vicinity_df_header)

    hypo2_header = ['temperature', 'runway_surface', 'gross_weight', 'altitude', 'wind', 'gradient',
                    'airports_within_vicinity', 'accommodating_in_this_condition']
    df_for_hypo2 = pd.DataFrame(columns=hypo2_header)

    # 112.654kms when both engine fails
    # https://www.telegraph.co.uk/travel/travel-truths/can-a-plane-fly-with-no-one-engines/#:~:text=Flying%20at%20a%20typical%20altitude,miles%20before%20reaching%20the%20ground.
    # for 2500 tested with 100 random lat and long and took nearest 10 airports and found the avg distance
    random_distance_available = random.randint(2000, 3500)
    fixed_gross_weight = gross_weight.random_gross_weight()

    for index, row in airport_df.iterrows():
        airport_loc = row['Geographic Location']
        lat_long = airport_loc.split(' ')
        airport_lat, airport_long = float(create_lat_long(lat_long[0][:-1])) * get_sign(lat_long[0][-1]), float(
            create_lat_long(lat_long[1][:-1])) * get_sign(lat_long[1][-1])

        geoAns = geod.Inverse(airport_lat, airport_long, random_lat, random_long)
        distance_btw_airports = float(geoAns['s12']) / 1000

        if distance_btw_airports <= random_distance_available:
            airports_in_vicinity_df = airports_in_vicinity_df.append(row, ignore_index=True)

    airports_in_vicinity_df.to_csv('airports_in_vicinity_df.csv')
    total_airport_in_vicinity = airports_in_vicinity_df.shape[0]

    for times in range(1, 101):
        randomSelector = RandomAttributeSelector(temp, runway_surface, gross_weight, altitude, wind, gradient,
                                                 fixed_gross_weight,
                                                 False)
        randomAttributeMap = randomSelector.__dict__
        ld, randomAttributeMap = mc_simulation(randomAttributeMap)
        accommodating_airport_in_this_condition = \
        airports_in_vicinity_df[airports_in_vicinity_df['Length (ft)'] * .6 >= ld].shape[0]

        df_data = [randomAttributeMap['temp'], randomAttributeMap['runway_surface'], randomAttributeMap['gross_weight'],
                   randomAttributeMap['altitude'],
                   randomAttributeMap['wind'], randomAttributeMap['gradient'], total_airport_in_vicinity,
                   accommodating_airport_in_this_condition]
        columns = pd.Series(df_data, index=df_for_hypo2.columns)
        df_for_hypo2 = df_for_hypo2.append(columns, ignore_index=True)

    df_for_hypo2.to_csv('hypo2.csv')

    # for times in range(1, 1001):
    #     ld, randomAttributeMap = mc_simulation(temp, runway_surface, gross_weight, altitude, wind, gradient)
    #     if row['Length (ft)']*.6 >= ld:
