import sys
import os
import datetime


import numpy as np
import pandas as pd
import serial
from tqdm import tqdm


port_path = '/dev/cu.usbserial-AC008NHR'
#port_path = '/dev/cu.usbserial-A107KQV7'
#port_path = '/dev/cu.usbserial-AI045SW1'
bps = 115200
timeout = 1


def get_now():
    '''
    It gets current time.
    
    Returns
    -------
    now : str
        current time
    
    Examples
    --------
    >>> get_now()
    "2020/11/10-16:05:43"
    '''
    now = datetime.datetime.now()
    yy = f'{now.year}'
    mm = f'{now.month}'.zfill(2)
    dd = f'{now.day}'.zfill(2)
    h = f'{now.hour}'.zfill(2)
    m = f'{now.minute}'.zfill(2)
    s = f'{now.second}'.zfill(2)
    now =  yy + '/' + mm + '/' + dd + '-' + h + ':'  + m + ':'  + s
    return now


def get_impedance(ser):
    '''
    It returns a list of impedances at each frequency acquired, 
    varying in frequency from 1 kHz to 1 MHz.
    
    Parameters
    ----------
    ser : object
        ser = serial.Serial(port_path, bps, timeout=timeout)
    
    Returns
    -------
    line : list
        A list of impedances at each frequency acquired.
        len(list) == 271
    
    Examples
    --------
    >>> ser = serial.Serial(port_path, bps, timeout=timeout)
    >>> get_impedance(ser)
    [0.0, 0.0, ..., 108.0, 110.0, ..., 0.0, 0.0]
        
    '''
    line = []
    for i in range(271):
        data = ser.readline().strip()
        amp = data.decode()
        line.append(float(amp))
    return line    


def get_vals(pid, n):
    '''
    Obtain data multiple times.
    
    Parameters
    ----------
    pid : int
        user id
    n : int
        Number of times to retrieve data
        
    Returns
    -------
    vals : list
        [val, val, ..., val]
        -->val : [pid, get_now()] + get_impedance()
        len(list) == n
        
    Exapmles
    --------
    >>> get_vals(2, 3)
    [
    [2, "2020/11/10-16:05:43", 0.0, 0.0, ..., 0.0],
    [2, "2020/11/10-16:05:45", 0.0, 0.0, ..., 0.0],
    [2, "2020/11/10-16:05:47", 0.0, 0.0, ..., 0.0],
    ]
    '''
    ser = serial.Serial(port_path, bps, timeout=timeout)
    vals = []
    for i in tqdm(range(n)):
        data = ser.readline().strip()
        start = data.decode()
        while start != 'S':
            data = ser.readline().strip()
            start = data.decode()
    
        line = get_impedance(ser)
        if line.count(0) > 150:
            print(f'''\n
            Interrupts because the data could not be retrieved successfully.
            \n
            {i} / {n} completed.''')
            break
        val = [pid, get_now()]+line[::-1]
        vals.append(val)
    return vals    


def main():
    pid = int(input('Your ID: ...?\n'))
    yn = input(f"Your ID is {pid}, right? [Y/n]")
    if yn != 'y' and yn != 'Y':
        exit()
    times = int(input('How many times do you want to take the data?: ...'))
    vals = get_vals(pid, times)
    cols = [f'{i}' for i in range(10**3, 10**4, 10**2)] + \
           [f'{i}' for i in range(10**4, 10**5, 10**3)] + \
           [f'{i}' for i in range(10**5, 10**6+1, 10**4)]
    use_cols = ['ID', 'date/time'] + cols
    tmp = pd.DataFrame(vals, columns=use_cols)
    
    if os.path.isfile('./testdata.csv'):
        df = pd.read_csv('./testdata.csv')
        df = pd.concat([df, tmp]).reset_index(drop=True)
    else:
        df = tmp
    df.to_csv('./testdata.csv', index=False)    
    

if __name__ == '__main__':
    main()
    print('success!\n')
