from math import pi
from math import cos
from math import sqrt

def equi(lat1, lat2, long1, long2):
    '''
    $$ returns the distance between 2 sets of latitiude longitude
    points and returns the distance between them in respects to the
    curvature of the earth
    '''
    radifier = (pi/180.0)
    dlat = abs(lat1-lat2)*radifier
    dlon = abs(long1-long2)*radifier
    alat = (abs(lat1+lat2)/2.0)*radifier
    R = 3958.8
    x = dlon*cos(alat)
    d = (sqrt(x*x + dlat*dlat))*R
    return(d)

def test() -> None:
    print(equi(-90,90,10,20))
    print(equi(33.64324045,33.53814, -117.84185686276017, -117.5998))
    print(equi(34.001476,33.64324045,-117.5749,-117.84185686276017))

if __name__ == '__main__':
    test()
