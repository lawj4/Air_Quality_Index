from geocoding import *
from get_air_quality import *


def nominatim() -> tuple:

    # takes in a user defined CENTER, which can either be a file or a str
    # description and displays the coordinates of said location
    wq = False
    lf = False
    while True:
        command = input("Local Files[L] or Web Query?[W]: ")
        if command.lower() == 'l':
            lf = True
            break
        elif command.lower() == 'w':
            wq = True
            break

    if wq:
        while True:
            command = input("Enter a location: ")
            if len(command) > 0:
                center = WebForward(command)
                coord = center.search()
                return coord
            else:
                print("INVALID")
    elif lf:
        while True:
            command = input("Enter a file: ")
            if len(command) > 0:
                center = PhysicalForward(command)
                coord = center.search()
                return coord
            else:
                print("INVALID")


def rangefinder():

    # asks user for a valid nonnegative integer for range until one suffices
    while True:
        user_range = input("Radius in miles from location: ")
        try:
            user_range = int(user_range)
            if user_range >= 0:
                return user_range
            else:
                raise ValueError
        except:
            print('INVALID RANGE')


def threshold():

    # asks user for a valid nonnegative integer for threshold until one suffices

    while True:
        user_threshold = input("Danger levels:")
        try:
            user_threshold = int(user_threshold)
            if user_threshold >= 0:
                return user_threshold
            else:
                raise ValueError
        except:
            print('INVALID THRESHOLD')

def maxfinder():
    '''
    asks user for a valid nonnegative integer for max until one suffices
    '''
    while True:
        user_max = input("Numbers of results: ")
        try:
            user_max = int(user_max)
            if user_max >= 0:
                return user_max
            else:
                raise ValueError
        except:
            print('INVALID MAX')



def aqi(coordinate: tuple, radius: int, threshold_num: int, display_num: int):
    '''
    loops until there is an AQI FILE or a AQI PURPLEAIR and then decides to aqi physically or web
    '''

    while True:
        #user_text = input()
        #user_text = 'AQI FILE purpleair.json'
        user_text = 'AQI PURPLEAIR'
        if 'AQI PURPLEAIR' in user_text:
            filtered = WebAQI(r'https://www.purpleair.com/data.json')
            return filtered.get_important_val(coordinate, radius, threshold_num, display_num)

        elif 'AQI FILE' in user_text:
            file = user_text.replace('AQI FILE','').strip()
            filtered = PhysicalAQI(file)
            return filtered.get_important_val(coordinate, radius, threshold_num, display_num)

        else:
            print('ERROR: AQI FORMAT')




def mitanimon(coordinates: list):
    '''
    reverse nominatim; decides to use web based or file based reverse; returns a list of the locations
    based on the order of the coordinates received
    '''
    location_description_list = []

    while True:
        user_text = 'REVERSE NOMINATIM'
        #user_text = 'REVERSE FILES nominatim_reverse1.json nominatim_reverse2.json nominatim_reverse3.json'
        #user_text = input()

        if 'REVERSE NOMINATIM' in user_text: #looks good
            for i in range(len(coordinates)):
                x_coord = coordinates[i][1][0]
                y_coord = coordinates[i][1][1]
                location_description_list.append(WebBackward(x_coord, y_coord).search())
            break

        elif 'REVERSE FILES' in user_text:
            file = user_text.replace('REVERSE FILES','').strip().split()
            for i in file:
                location_description_list.append(PhysicalBackward(i).search())
            break

        else:
            print('ERROR: REVERSE FORMAT')

    return location_description_list

def run():
    coordinate = nominatim()
    radius = rangefinder()
    threshold_num = threshold()
    display_num = maxfinder()
    aqi_list = aqi(coordinate, radius, threshold_num, display_num)
    location_description_list = mitanimon(aqi_list)

    print('CENTER ',end='')
    display_coords_nicely(coordinate)

    for i in range(len(aqi_list)):
        print(f'AQI {aqi_list[i][0]}')
        display_coords_nicely(aqi_list[i][1])
        try:
            print(location_description_list[i][2])
        except:
            print('NOT ENOUGH LOCATION FILES GIVEN')


run()
