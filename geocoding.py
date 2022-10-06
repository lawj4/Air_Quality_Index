from pathlib import Path
import urllib.request
import json
import urllib.parse

class PhysicalForward:
    '''
    $$ creates an object based on a file input; detects if it exists; detects if it is json;
    returns a tuple of lat and long
    '''
    def __init__(self, file:str) -> None:
        self._path = Path(file)
    def search(self) -> tuple:
        try:
            f = open(self._path)
        except:
            print('FAILED')
            print(self._path)
            print('MISSING')
            exit()
        self._encoded = f.read()
        f.close()
        try:
            json_dict = json.loads(self._encoded)[0]
        except:
            print('FAILED')
            print(self._path)
            print('FORMAT')
            exit()
        return ((float(json_dict['lat']), float(json_dict['lon'])))
                

class PhysicalBackward:
    def __init__(self, file:str) -> None:
        '''
        $$ creates an object based on path file
        '''
        self._path = Path(file)
    def search(self) -> tuple:
        '''
        $$ detects if path exists; reads the file path; attempts to make dictionary from json;
        returns 3-tuple of lat, lon, name
        '''
        try:
            f = open(self._path)
        except:
            print('FAILED')
            print(self._path)
            print('MISSING')
            exit()
        self._encoded = f.read()
        f.close()
        try:
            json_dict = json.loads(self._encoded)
        except:
            print('FAILED')
            print(self._path)
            print('FORMAT')
            exit()
        return (float(json_dict['lat']),float(json_dict['lon']), json_dict['display_name'])

class WebForward:
    def __init__(self, description: str) -> None:
        '''
        $$ creates an object based on user defined description
        '''
        self._desc = description
        
    def search(self) -> tuple:
        '''
        $$ searches the website using query parameters; detects if it can be opened; detects if code is not 200;
        detects if it is json; returns tuple lat, lon
        '''
        query_parameters = [
            ('q', self._desc),
            ('format', 'json'),
            ('limit', 1)
        ]
        url = 'https://nominatim.openstreetmap.org/search?'+urllib.parse.urlencode(query_parameters)
        request = urllib.request.Request(url, headers = {'Referer': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/70796407'})
        try:
            response = urllib.request.urlopen(request)
        except:
            print('FAILED')
            print(url)
            print('NETWORK')
            exit()
            
        read = response.read()

        if response.getcode() != 200:
            print('FAILED')
            print(response.getcode(), url)
            print('NOT 200')
            exit()
        
        try:
            json_dict = json.loads(read)[0]
        except:
            print('FAILED')
            print(response.getcode(), url)
            print('FORMAT')
            exit()
            
        return ((float(json_dict['lat']), float(json_dict['lon'])))

class WebBackward:
    def __init__(self, lat: float, lon: float) -> tuple:
        '''
        $$ creates an object based on lat and lon
        '''
        self._lat = str(lat)
        self._lon = str(lon)
    def search(self):
        '''
        $$ searches the website using query; detects if it can be open; detects if code is not 200;
        detects if text is not json; returns 3-tuple lat, lon, name
        '''
        query_parameters = [
            ('lat', self._lat),
            ('lon', self._lon),
            ('format','json')
        ]
        url = 'https://nominatim.openstreetmap.org/reverse?'+urllib.parse.urlencode(query_parameters)
        request = urllib.request.Request(url, headers = {'Referer': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/70796407'}) 
        try:
            response = urllib.request.urlopen(request)
        except:
            print('FAILED')
            print(url)
            print('NETWORK')
            
        read = response.read()
    
        if response.getcode() != 200:
            print('FAILED')
            print(response.getcode(), url)
            print('NOT 200')
            exit()
        
        try:
            json_dict = json.loads(read)
        except:
            print('FAILED')
            print(response.getcode(), url)
            print('FORMAT')
            exit()
            
        return (float(json_dict['lat']),float(json_dict['lon']), json_dict['display_name'])



        
def test():
    #x = PhysicalForward('nominatim_center.json')
    #print(x.search())
    y = WebForward('Bren Hall, Irvine, CA')
    print(y.search())
    z = WebBackward(33.64324045, -117.84185686276017)
    yes = (z.search())
    print(yes)
    #a = PhysicalBackward(r'C:\Users\jlaw0\Desktop\python_proj\project\project3\nominatim_reverse1.json')
    #print(a.search())

if __name__ == '__main__':
    test()
