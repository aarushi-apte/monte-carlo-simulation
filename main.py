import sys
import random
import pandas as pd

class weather_predictor():

    def __init__(self):
        self.weather = random.choice(['sunny', 'cloudy', 'rainy', 'snowy', 'foggy', 'thunder'], weights=(80, 10, 5, 5), k=1)
        self.change_count = 0

    def random_weather(self):


class runway_surface_predictor():

    def __init__(self):
        self.runway_surface = random.choice(['dry','wet', 'snow', 'slush', 'non melting ice'], weights=(70, 50, 5, 5), k=1)

    def get_runway_surface(self):


class gross_weight_predictor():

    #https://www.portofbellingham.com/DocumentCenter/View/7196/Revised-Runway-Length-Discussion-20171206?bidId=
    def __init__(self):
        self.gross_weight = random.choice(['medium', 'light', 'heavy', 'super'], weights=(50, 25, 10), k=1)

class altitude_predictor():

    def __init__(self):
        self.altitude = random.choice(['low', 'high' ], weights=(50, 25), k=1)


class altitude_predictor():

    def __init__(self):
        self.altitude = random.choice(['headwind', 'tailwind', 'crosswind', 'gustwind' ], weights=(80, 40, 10, 8), k=1)




if __name__ == '__main__':