import pyautogui

try:
    while True:
        x, y = pyautogui.position()
        pos_str = 'Coordinate: (' + str(x).rjust(4) + ', ' + str(y).rjust(4) + ')  '
        
        pixelColor = pyautogui.screenshot().getpixel((x, y))
        pos_str += ' RGB: (' + str(pixelColor[0]).rjust(3)
        pos_str += ', ' + str(pixelColor[1]).rjust(3)
        pos_str += ', ' + str(pixelColor[2]).rjust(3) + ')'
        print(pos_str, end='')
        print('\b' * len(pos_str), end='', flush=True)
except KeyboardInterrupt:
    print('\nDone.')
