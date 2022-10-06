
def _scale(pm_25, x1, x2, y1, y2) -> int:
    '''
    $$ helper method that performs the p 2.5 conversion and returns the output
    in aqi
    '''
    x_x1 = pm_25-x1
    y2_y1 = y2-y1
    x2_x1 = x2-x1
    interpolation = int((y1 + x_x1*y2_y1/x2_x1)+0.5)
    return interpolation

def p2toaqi(pm_25: float) -> int:
    '''
    && converts any positive value p2 and turns it into an aqi
    value that is approximately equivalent
    '''
    if 0 <= pm_25 and pm_25 < 12.1:
        return _scale(pm_25, 0, 12, 0, 50)
    elif 12.1 <= pm_25 and pm_25 < 35.5:
        return _scale(pm_25, 12.1, 35.4, 51, 100)
    elif 35.5 <= pm_25 and pm_25 < 55.5:
        return _scale(pm_25, 35.5, 55.4, 101, 150)
    elif 55.5 <= pm_25 and pm_25 < 150.5:
        return _scale(pm_25, 55.5, 150.4, 151, 200)
    elif 150.5 <= pm_25 and pm_25 < 250.5:
        return _scale(pm_25, 150.5, 250.4, 201, 300)
    elif 250.5 <= pm_25 and pm_25 < 350.5:
        return _scale(pm_25, 250.5, 350.4, 301, 400)
    elif 350.5 <= pm_25 and pm_25 < 500.5:
        return _scale(pm_25, 350.5, 500.5, 401, 500)
    elif 500.5 <= pm_25:
        return 501

def test() -> None:
    print(p2toaqi(6))
    print(p2toaqi(23.75))
    print(p2toaqi(45.45))
    print(p2toaqi(102.95))
    print(p2toaqi(200.45))
    print(p2toaqi(300.45))
    print(p2toaqi(425.45))
    print(p2toaqi(525))

if __name__ == '__main__':
    test()
