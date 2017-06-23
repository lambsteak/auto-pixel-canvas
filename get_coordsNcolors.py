'''
Created on 21-Jun-2017

@author: thepenguin
'''

import pyautogui

try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'Coordinate: (' + str(x).rjust(4) + ', ' + str(y).rjust(4) + ')  '
        
        pixelColor = pyautogui.screenshot().getpixel((x, y))
        positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        positionStr += ', ' + str(pixelColor[1]).rjust(3)
        positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
except KeyboardInterrupt:
    print('\nDone.')