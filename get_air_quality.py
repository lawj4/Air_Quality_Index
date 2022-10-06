from pathlib import Path
import urllib.request
import json
from aqi_value import *
from math import sqrt
from equi_approximation import *

def display_coords_nicely(coordinate: tuple) -> None:
    '''
    $$ displays a tuple coordinate input into the format based on NSWE instead of cartesian
    '''
    if coordinate[0] >= 0:
        print(f'{coordinate[0]}/N ',end='')
    elif coordinate[0] < 0:
        print(f'{-coordinate[0]}/S ',end='')
    if coordinate[1] > 0:
        print(f'{coordinate[1]}/N')
    elif coordinate[1] <= 0:
        print(f'{-coordinate[1]}/W')
        
def _descending_aqi_list(aqi_dict: dict, display_num: int) -> list:
    '''
    $$ helper function that returns the coordinates of each dictionary value by AQI descending,
    based on the max number of values wanted
    '''
    count = 0
    aqi_list = []
    sort_dict = sorted(aqi_dict, reverse = True)
    for i in sort_dict:
        aqi_list.append((i, aqi_dict[i]))
        count+=1
        if count >= display_num:
            return aqi_list 
        
class PhysicalAQI:
    def __init__(self, file:str) -> None:
        '''
        $$ creates an object based on the str file a user gives; detects if it exists;
        decodes the text; reads it; then closes
        '''
        self._path = Path(file)
        try:
            f = open(self._path, encoding = 'utf-8')
        except:
            print('FAILED')
            print(self._path)
            print('MISSING')
            exit()
        self._read = f.read()
        f.close()  
    def get_important_val(self, coordinate: tuple, radius: int, threshold_num: int, display_num: int) -> list:
        '''
        $$ creates a dictionary if file is in json; filters though every parameter: (coord,
        radius, aqi threshold, and display number); returns a list of the coordinates
        '''
        try:
            json_dict = json.loads(self._read)
        except:
            print('FAILED')
            print(self._path)
            print('FORMAT')
            exit()
        aqi_dict = {}
        
        for i in json_dict['data']:
    
            if (
            i[1]  != None and
            i[4]  != None and
            i[25] != None and
            i[27] != None and
            i[28] != None
            ):
                if (
                p2toaqi(i[1]) >= threshold_num and
                i[4] <= 3600 and
                i[25] == 0 and
                equi(coordinate[0],i[27],coordinate[1],i[28]) <= radius
                ):
                    aqi_dict[p2toaqi(i[1])] = i[27],i[28]
        if _descending_aqi_list(aqi_dict, display_num) == None:
            return []
        else:
            return _descending_aqi_list(aqi_dict, display_num)
        
class WebAQI:
    def __init__(self, url: str) -> None:
        '''
        creates an object out of a url; attempts to open it and detects if there is a connection or gives wrong code
        '''
        self._url = url
        request = urllib.request.Request(url, headers = {'Referer': 'http://www.python.org/'})
        try:
            self._response = urllib.request.urlopen(request)
        except:
            print('FAILED')
            print(url)
            print('NETWORK')
            exit()
        self._read = self._response.read()
        if self._response.getcode() != 200:
            print('FAILED')
            print(self._response.getcode(), self._url)
            print('NOT 200')
            exit()
        
    def get_important_val(self, coordinate: tuple, radius: int, threshold_num: int, display_num: int):
        '''
        creates a dictionary if website is i njson and filters though every parameter: (coord,
        radius, aqi threshold, and display number); returns a list of the coordinates
        '''
        try:
            json_dict = json.loads(self._read)
        except:
            print('FAILED')
            print(response.getcode(), url)
            print('FORMAT')
            exit()
        aqi_dict = {}
        for i in json_dict['data']:
    
            if (
            i[1]  != None and
            i[4]  != None and
            i[25] != None and
            i[27] != None and
            i[28] != None
            ):
                if (
                p2toaqi(i[1]) >= threshold_num and
                i[4] <= 3600 and
                i[25] == 0 and
                equi(coordinate[0],i[27],coordinate[1],i[28]) <= radius
                ):
                    aqi_dict[p2toaqi(i[1])] = i[27],i[28]
                    
        if _descending_aqi_list(aqi_dict, display_num) == None:
            return []
        else:
            return _descending_aqi_list(aqi_dict, display_num)
        

def _test_web():        
    y = WebAQI(r'https://www.purpleair.com/data.json')
    print(y.get_important_val((33.64324045,-117.84185686276017),30,20,3))
def _test_phys():
    y = PhysicalAQI(r'purpleair.json')
    print(y.get_important_val((33.64324045,-117.84185686276017),30,50,3))
    #x = PhysicalAQI(r"C:\Users\jlaw0\Desktop\python_proj\project\project3\purplebob.json")
    #print(x.get_important_val((33.64324045,-117.84185686276017),30,50,3))

if __name__ == '__main__':
    _test_web()
    #_test_phys()
