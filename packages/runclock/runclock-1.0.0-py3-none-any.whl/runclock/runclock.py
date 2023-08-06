from time import sleep
from time import ctime

def run_at(hour:str, minute:str = '00', second:str = '00') -> None:
    if type(hour) != str or type(minute) != str or type(second) != str:
        raise TypeError('Function takes string but integer given')

    hour_n = 0
    minute_n = 0
    second_n = 0

    while hour != hour_n or minute != minute_n or second != second_n:
        time_now = ctime().split(' ')
        clock_now = time_now[3].split(':')

        hour_n = clock_now[0]
        minute_n = clock_now[1]
        second_n = clock_now[2]

        sleep(1)
