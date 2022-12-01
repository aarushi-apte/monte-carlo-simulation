import sys
import random
import pandas as pd


class randomAttrituteSelector():

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
        self.runway_surface = random.choices(['dry', 'wet', 'snow', 'slush', 'non melting ice'],
                                             weights=(80, 60, 40, 30, 22), k=1)
        self.change_count = 0

    def random_runway_surface(self):
        if self.change_count % 10 == 0:
            self.runway_surface = random.choices(['dry', 'wet', 'snow', 'slush', 'non melting ice'],
                                             weights=(80, 60, 40, 30, 22), k=1)

        self.change_count += 1
        return self.runway_surface[0]


class GrossWeightPredictor:

    # https://www.portofbellingham.com/DocumentCenter/View/7196/Revised-Runway-Length-Discussion-20171206?bidId=
    def __init__(self):
        self.gross_weight = random.choices(['light', 'medium', 'heavy', 'super'], weights=(50, 40, 30, 20), k=1)
        self.change_count = 0

    def random_gross_weight(self):
        if self.change_count % 3 == 0:
            self.gross_weight = random.choices(['medium', 'light', 'heavy', 'super'], weights=(50, 40, 30, 20), k=1)

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
        self.wind = random.choices(['headwind', 'tailwind', 'crosswind', 'gustwind'], weights=(80, 40, 10, 8), k=1)
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
    if runway_surface == "dry":
        distance_percent = 1
    elif runway_surface == "wet":
        distance_percent = 1.3
    elif runway_surface == "snow":
        distance_percent = 1.65
    elif runway_surface == "slush":
        distance_percent = 2.15
    else:
        distance_percent = 4.0
    return  distance_percent


def effect_by_gross_weight(gross_weight):
    pass

def effect_by_altitude(altitude):
    if altitude <= 8000:
        distance_percent = (altitude / 1000) * 0.12
    else:
        distance_percent = 0.96
        distance_percent = distance_percent - ((altitude - 8000) / 1000) * 0.20
    return distance_percent

def effect_by_wind(wind):
    pass


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

    for times in range(1, 5001):
        randomSelector = randomAttrituteSelector(temp, runway_surface, gross_weight, altitude, wind)
        randomAttributeMap = randomSelector.__dict__
        effect_by_temp = effect_by_temp(randomAttributeMap['temp'])
        effect_by_runway_surface = effect_by_runway_surface(randomAttributeMap['runway_surface'])
        effect_by_gross_weight = effect_by_gross_weight(randomAttributeMap['gross_weight'])
        effect_by_altitude = effect_by_altitude(randomAttributeMap['altitude'])
        effect_by_wind = effect_by_wind(randomAttributeMap['wind'])
        distance = meanDistance * effect_by_temp * effect_by_runway_surface * effect_by_gross_weight * effect_by_altitude * effect_by_wind



