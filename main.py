import math
import random
import pandas as pd
from geographiclib.geodesic import Geodesic
import matplotlib.pyplot as plt

geod = Geodesic.WGS84


class RandomAttributeSelector():

    def __init__(self, temp, runway_surface, gross_weight, altitude, wind, gradient):
        self.temp = temp.random_temperature()
        self.runway_surface = runway_surface.random_runway_surface()
        self.gross_weight = gross_weight.random_gross_weight()
        self.altitude = altitude.random_altitude()
        self.wind = wind.random_wind()
        self.gradient = gradient.random_gradient()


class TemperaturePredictor:

    def __init__(self):
        # https://www.washingtonpost.com/news/capital-weather-gang/wp/2018/07/27/sometimes-its-too-hot-for-airplanes-to-fly-heres-why/#:~:text=Every%20plane%20has%20a%20different,at%20more%20than%20174%2C200%20pounds.
        # https://www.cntraveler.com/stories/2016-06-20/its-so-hot-some-planes-cant-fly-heres-why
        self.temperature = random.choices(['freezing', 'cold', 'pleasant', 'hot', 'extreme'], weights=(20, 80, 120, 60,
                                                                                                       20), k=1)
        self.change_count = 0

    def random_temperature(self):
        """
        This function randomizes the temperature category using random choices based on the weights assigned
        to them
        """
        self.temperature = random.choices(['freezing', 'cold', 'pleasant', 'hot', 'extreme'], weights=(5, 60, 120, 60,
                                                                                                       20), k=1)
        return self.temperature[0]


class RunwaySurfacePredictor:

    def __init__(self):
        self.runway_surface = random.choices(['normal', 'wet', 'standing_water', 'snow', 'icy'], weights=(80, 60, 40,
                                                                                                          30, 22), k=1)
        self.change_count = 0

    def random_runway_surface(self):
        """
        This function randomizes the runway surface after every 10 iterations using random choices
        based on the weights assigned to them
        """
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
        """
        This function randomizes the weight category after every 3 iterations using random choices
        based on the weights assigned to them
        """
        if self.change_count % 3 == 0:
            self.gross_weight = random.choices(['light', 'medium', 'heavy', 'super'], weights=(40, 50, 30, 20), k=1)

        self.change_count += 1
        return self.gross_weight[0]


class AltitudePredictor:
    # Choosing altitude distribution as per our dataset and the mean value of all the rows
    def __init__(self):
        self.altitude = random.choices(['low', 'normal', 'high'], weights=(7, 100, 5), k=1)
        self.change_count = 0

    def random_altitude(self):
        """
        This function randomizes the altitude category using random choices based on the weights assigned to them
        """
        if self.change_count % 1 == 0:
            self.altitude = random.choices(['low', 'normal', 'high'], weights=(7, 100, 5), k=1)

        self.change_count += 1
        return self.altitude[0]


class WindPredictor:

    def __init__(self):
        self.wind = []
    def random_wind(self):
        """
        This function randomizes the wind type using random choices based on the weights assigned to them
        """
        self.wind = random.choices(['headwind', 'tailwind', 'crosswind'], weights=(80, 40, 10), k=1)
        return self.wind[0]


class GradientPredictor:

    def __init__(self):
        self.gradient = random.randint(50, 100)
        self.change_count = 0

    def random_gradient(self):
        """
        This function randomizes the gradient after every 10 iterations using randint
        """
        if self.change_count % 10 == 0:
            self.gradient = random.randint(50, 100)

        self.change_count += 1
        return self.gradient


def effect_by_temp(temperature):
    """
    In this function, we first identify which category a particular temperature belongs to and generate
    a random temperature that falls under that category range.
    Following are the temperature categories and their ranges:
    1. Freezing : -50C to -20C
    2. Cold : -20C to 10C
    3. Pleasant : 10C to 30C
    4. Hot : 30C to 40C
    5. Extreme : 40C to 50C

    After a random temperature value has been generated, we calculate its difference from ISA (International
    Standard Atmosphere) and finally calculate how the landing distance is affected by temperature conditions.

    :param temperature: a string value which tells us the temperature category
    :return: returns a value that tells us how the landing distance is affected by temperature condition
    """
    # https://www.experimentalaircraft.info/flight-planning/aircraft-performance-7.php
    isa_base = 15

    if temperature == 'freezing':
        temp = random.randint(-50, -20)
    elif temperature == 'cold':
        temp = random.randint(-20, 10)
    elif temperature == 'pleasant':
        temp = random.randint(10, 30)
    elif temperature == 'hot':
        temp = random.randint(30, 40)
    else:
        temp = random.randint(40, 50)

    if temp < isa_base:
        temp_diff = (abs(temp - isa_base)) / 10
        distance_percent = 1 - (0.05 * temp_diff)
    elif temp > isa_base:
        temp_diff = (temp - isa_base) / 10
        distance_percent = 1 + (0.05 * temp_diff)
    else:
        distance_percent = 1
    return distance_percent


def effect_by_runway_surface(runway_surface):
    """
    In this function, we calculate how the runway surface affects the landing distance of an airplane
    There are five different categories and each affects the runway distance in the following range:
    1. Normal : 1
    2. Wet : 1.3 - 1.4
    3. Standing Water : 2 - 2.3
    4. Snow : 1.6 - 1.7
    5. Icy : 3.5 - 4.5

    We randomly generate multiplying factor from the range of a particular surface.

    :param runway_surface: a string value that tells us about the runway surface condition
    :return: a value that tells us how the landing distance is affected by runway surface
    """
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
    """
    The function calculates how the landing distance changes based on the weight of the plane by
    randomizing the minimum and maximum weight in a particular category
    Here the weight of the airplane is classified into four main categories:
    1. light - 83000 to 129200 lbs
    2. medium - 91300 to 146300 lbs
    3. heavy - 93680 to 147300 lbs
    4. super - 98495 to 138450 lbs
    :param gross_weight: a string that tells us the category of the airplane weight
    :return: returns the effect of the plane weight on the landing distance
    """
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
    """
    Here we take as input the altitude above sea level as a category. Then we generate a random altitude based
    on the range of the corresponding category. Finally, we calculate the effect of that altitude on the landing
    distance.
    We have considered the following categories for altitude:
    1. low : -14 to 0
    2. normal : 0 to 1000
    3. high : 1000 to 8355
    :param altitude: the string that gives us the altitude category
    :return: we return the factor by which the altitude changes the landing distance
    """
    # https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak/media/13_phak_ch11.pdf

    if altitude == 'low':
        alt = random.randint(-14, 0)
        distance_multiply = (0.035 * (alt / 1000)) + 1
    elif altitude == 'normal':
        alt = random.randint(0, 1000)
        distance_multiply = (0.035 * (alt / 1000)) + 1
    else:
        alt = random.randint(1000, 8355)
        distance_multiply = (0.035 * (alt / 1000)) + 1

    return distance_multiply


def effect_by_wind(wind):
    """
    In this function we calculate the effect of wind in kt on the landing distance
    We have considered three types of wind:
    1. Headwind
    2. Tailwind
    3. Crosswind (in case of crosswind we randomize the angle of wind as well)
    :param wind: a srting that tells us what type of wind it is
    :return: it retunns a value to tell us how wind affects landing distance
    """
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
    """
    This function calculates the effect of gradient which is the difference between the highest and lowest point
    on the runway on the landing distance of an airplane
    :param runway_gradient: the difference between the highest and lowest point on the runway
    :return: it returns the distance that needs to be added to the original landing distance
    >>> effect_by_gradient(60)
    600
    """
    # https://www.portofbellingham.com/DocumentCenter/View/7196/Revised-Runway-Length-Discussion-20171206?bidId=

    distance_to_add = runway_gradient * 10
    return distance_to_add


def random_direction():
    return (round(random.uniform(-90, 90), 5),
            round(random.uniform(-180, 180), 5))


def get_sign(direction):
    """
    A simple functions that returns a boolean based on the direction
    :param direction: a symbol for the direction
    :return: returns a boolean based on the direction
    >>> get_sign('N')
    1
    """
    if direction == 'W' or direction == 'S':
        return -1
    return 1


def create_lat_long(lat_long):
    lat_long = lat_long.split(' ')
    direction_lat = lat_long[0][-1]
    direction_long = lat_long[1][-1]
    lat = lat_long[0][:-1]
    long = lat_long[1][:-1]
    float_lat = float(lat[:2] + '.' + lat[2:])
    float_long = float(long[:2] + '.' + long[2:])
    return float_lat * get_sign(direction_lat), float_long * get_sign(direction_long)


def mc_simulation(randomAttributeMap, hypo_type):
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
    if hypo_type == '1':

        ld = (min_distance * temp_effect * runway_surface_effect * wind_effect * altitude_effect
              ) + gross_weight_effect + gradient_effect
    else:
        ld = (min_distance * temp_effect * runway_surface_effect * wind_effect * altitude_effect
              ) + gross_weight_effect
    return ld, randomAttributeMap


def get_nearest_accommodating_airport(curr_pos_lat, curr_pos_long):
    """
    This function iterates through the airport dataset and finds the closest airport that can accomodate
    the current flight's landing distance
    location
    :param curr_pos_lat: the latitude of the current position
    :param curr_pos_long: the longitude of the current position
    :return: it returns the nearest airport that can accommodate the flight
    """
    nearest_airport = float('inf')

    for index, row in airport_df.iterrows():
        airport_loc = row['Geographic Location']
        airport_altitude = row['Elevation (ft)']
        runway_length = row['Length (ft)']

        airport_lat, airport_long = create_lat_long(airport_loc)

        geoAns = geod.Inverse(airport_lat, airport_long, curr_pos_lat, curr_pos_long)
        dist_btw_currpos_and_airport = float(geoAns['s12']) / 1000

        random_attribute_map = {'temp': random.randint(15, 20), 'runway_surface': 'normal', 'gross_weight': 'medium',
                                'altitude': airport_altitude, 'wind': 'headwind', 'gradient': 75}
        ld, random_attribute_map = mc_simulation(random_attribute_map, '2')

        if runway_length * 0.6 > ld:
            if dist_btw_currpos_and_airport < nearest_airport:
                nearest_airport = dist_btw_currpos_and_airport

    return nearest_airport


def get_flight_path(airport_df):
    """
    This function iterates through the airport dataset and checks if the distance between those airports
    is less than 6570, if yes, we return the location coordinates of those two airports
    :param airport_df: the airport information dataset
    :return: returns the latitude and longitude of the two airports
    """
    while True:
        two_airports = airport_df.sample(n=2)
        two_airports = two_airports.reset_index()
        airport1 = two_airports.iloc[0]['Geographic Location']
        airport2 = two_airports.iloc[1]['Geographic Location']
        lat1, long1 = create_lat_long(airport1)
        lat2, long2 = create_lat_long(airport2)
        geoAns = geod.Inverse(lat1, long1, lat2, long2)
        dist_btw_airports = float(geoAns['s12']) / 1000
        if dist_btw_airports <= 6570:
            break

    return lat1, long1, lat2, long2


def plot_hypo2(min, max, mean):
    # https://www.geeksforgeeks.org/adding-value-labels-on-a-matplotlib-bar-chart/
    x = [1, 2, 3]
    y = [min, mean, max]

    tick_label = ['Min', 'Mean', 'Max']
    plt.bar(x, y, tick_label=tick_label,
            width=0.8, color=['green', 'blue', 'orange'])

    for i in range(len(x)):
        plt.text(i+1, y[i], y[i], ha='center')

    plt.xlabel('x - axis')
    plt.ylabel('Distance')

    plt.title('The Minimum, Mean & Maximum Distance to the Nearest Airport.')
    plt.show()


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

    # Hypothesis 1
    hypo1_header = ['temperature', 'runway_surface', 'gross_weight', 'altitude', 'wind', 'gradient',
                    'accommodating_airports', '% of accommodating airports']
    df_for_hypo1 = pd.DataFrame(columns=hypo1_header)

    for times in range(1, 1001):
        randomSelector = RandomAttributeSelector(temp, runway_surface, gross_weight, altitude, wind, gradient)
        randomAttributeMap = randomSelector.__dict__
        ld, randomAttributeMap = mc_simulation(randomAttributeMap, '1')
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
    hypo_1_result = sum(df_for_hypo1['% of accommodating airports']) / len(df_for_hypo1['% of accommodating airports'])
    print("Considering all given situation,an average of {}% of airports can accommodate the various types of flights.".
          format(round(hypo_1_result, 2)))

    # Hypothesis 2
    hypo2_header = ['arrival_lat', 'arrival_long', 'destination_lat', 'destination_long', 'curr_lat', 'curr_long',
                    'nearest_airport_distance']

    df_for_hypo2 = pd.DataFrame(columns=hypo2_header)

    takeoff_lat, takeoff_long, destination_lat, destination_long = get_flight_path(airport_df)
    l = geod.InverseLine(takeoff_lat, takeoff_long, destination_lat, destination_long)
    ds = 100e3;
    n = int(math.ceil(l.s13 / ds))
    for i in range(n + 1):
        if i == 0:
            pass
        s = min(ds * i, l.s13)
        g = l.Position(s, Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        curr_pos_lat = g['lat2']
        curr_pos_long = g['lon2']
        # print(curr_pos_lat, curr_pos_long)
        distance_to_nearest_airport = get_nearest_accommodating_airport(curr_pos_lat, curr_pos_long)
        df_data = [takeoff_lat, takeoff_long, destination_lat, destination_long, curr_pos_lat, curr_pos_long,
                   distance_to_nearest_airport]
        columns = pd.Series(df_data, index=df_for_hypo2.columns)
        df_for_hypo2 = df_for_hypo2.append(columns, ignore_index=True)

    df_for_hypo2.to_csv('hypo2.csv')
    hypo2_description = df_for_hypo2.describe()
    minimum_distance = round(hypo2_description['nearest_airport_distance']['min'], 2)
    maximum_distance = round(hypo2_description['nearest_airport_distance']['max'], 2)
    mean_distance = round(hypo2_description['nearest_airport_distance']['mean'], 2)
    plot_hypo2(minimum_distance, maximum_distance, mean_distance)
    print(f"A flight from {takeoff_lat, takeoff_long} to {destination_lat, destination_long}, will encounter a \nminimum distance of {minimum_distance} kms, \nmean distance of {mean_distance} kms and \nmaximum distance of {maximum_distance} kms \nto the nearest airport along the entire route for an emergency landing that could accommodate the landing distance required by it.")



    # 112.654kms when both engine fails
    # https://www.telegraph.co.uk/travel/travel-truths/can-a-plane-fly-with-no-one-engines/#:~:text=Flying%20at%20a%20typical%20altitude,miles%20before%20reaching%20the%20ground.
    # for 2500 tested with 100 random lat and long and took nearest 10 airports and found the avg distance

    # total_airport_in_vicinity = airports_in_vicinity_df.shape[0]
    #
    # for times in range(1, 101):
    #     randomSelector = RandomAttributeSelector(temp, runway_surface, gross_weight, altitude, wind, gradient,
    #                                              fixed_gross_weight,
    #                                              False)
    #     randomAttributeMap = randomSelector.__dict__
    #     ld, randomAttributeMap = mc_simulation(randomAttributeMap)
    #     accommodating_airport_in_this_condition = \
    #     airports_in_vicinity_df[airports_in_vicinity_df['Length (ft)'] * .6 >= ld].shape[0]
    #
    #     df_data = [randomAttributeMap['temp'], randomAttributeMap['runway_surface'], randomAttributeMap['gross_weight'],
    #                randomAttributeMap['altitude'],
    #                randomAttributeMap['wind'], randomAttributeMap['gradient'], total_airport_in_vicinity,
    #                accommodating_airport_in_this_condition]
    #     columns = pd.Series(df_data, index=df_for_hypo2.columns)
    #     df_for_hypo2 = df_for_hypo2.append(columns, ignore_index=True)

    # df_for_hypo2.to_csv('hypo2.csv')

    # for times in range(1, 1001):
    #     ld, randomAttributeMap = mc_simulation(temp, runway_surface, gross_weight, altitude, wind, gradient)
    #     if row['Length (ft)']*.6 >= ld:
