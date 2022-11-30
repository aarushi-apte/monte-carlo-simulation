import sys
import random
import pandas as pd

class WeatherPredictor:

    def __init__(self):
        self.weather = random.choice(['sunny', 'cloudy', 'rainy', 'snowy', 'foggy', 'thunder'], weights=(80, 10, 5, 5), k=1)
        self.change_count = 0

    def random_weather(self):


class RunwaySurfacePredictor:

    def __init__(self):
        self.runway_surface = random.choice(['dry','wet', 'snow', 'slush', 'non melting ice'], weights=(70, 50, 5, 5), k=1)

    def get_runway_surface(self):


class GrossWeightPredictor:

    #https://www.portofbellingham.com/DocumentCenter/View/7196/Revised-Runway-Length-Discussion-20171206?bidId=
    def __init__(self):
        self.gross_weight = random.choice(['medium', 'light', 'heavy', 'super'], weights=(50, 25, 10), k=1)

class AltitudePredictor:
    # The lowest non-negative altitude airport in The US
    # https://www.boldmethod.com/blog/lists/2014/10/7-lowest-civilian-airports-us/
    # The highest altitude airport in The US
    # https://www.boldmethod.com/blog/lists/2014/08/10-highest-airports-in-the-united-states/
    def __init__(self):
        #self.altitude = random.choice(['low', 'high' ], weights=(50, 25), k=1)
        self.altitude =  random.randint(0, 9934)
    if altitude <= 8000:
        distance_percent = (altitude/1000) * 0.12
    else:
        distance_percent =  0.96
        distance_percent = distance_percent - ((altitude-8000)/1000) * 0.20

class WindPredictor:

    def __init__(self):
        self.altitude = random.choice(['headwind', 'tailwind', 'crosswind', 'gustwind' ], weights=(80, 40, 10, 8), k=1)




if __name__ == '__main__':