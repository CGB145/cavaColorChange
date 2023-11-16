from PIL import ImageGrab,ImageColor
from Xlib import display,X
from screeninfo import get_monitors
import webcolors
import os
import time
import keyboard
import subprocess
import sys



def getUpperMonitorScreenShot():
    monitorList = get_monitors()
    firstMonitor = monitorList[0]
    secondMonitor = monitorList[1]

    bbox = (firstMonitor.x, firstMonitor.y, firstMonitor.x + firstMonitor.width, firstMonitor.y + firstMonitor.height)


    
    screenshot = ImageGrab.grab(bbox=bbox)
    return  screenshot

def upperMonitorHeight():
    monitorList = get_monitors()
    firstMonitor = monitorList[0]
    return firstMonitor.height

def upperMonitorWidth():
    monitorList = get_monitors()
    firstMonitor = monitorList[0]
    return firstMonitor.width 

def getLowerMonitorScreenShot():
    monitorList = get_monitors()
    secondMonitor = monitorList[1]
    bbox = (secondMonitor.x, secondMonitor.y, secondMonitor.x + secondMonitor.width, secondMonitor.y + secondMonitor.height)

    screenshot = ImageGrab.grab(bbox=bbox)
    
    return screenshot


def rgb_to_hex(r, g, b):
    # Ensure RGB values are within the range 0-255
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))

    # Convert to hexadecimal and return the formatted string
    return "#{:02x}{:02x}{:02x}".format(r, g, b)




def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]


def getAverageColorOfScreen(displayScreenshot,displayWidht,displayHeight):

    xPixelCount = 0
    yPixelCount = 0
    red = []
    green =[]
    blue = []
    while xPixelCount != displayWidht - 1:
        
        xPixelCount += 1
        yPixelCount = 0
        pixel = displayScreenshot.getpixel((xPixelCount,yPixelCount))
        red.append(pixel[0])
        green.append(pixel[1])
        blue.append(pixel[2])

        if xPixelCount != displayWidht:
            while yPixelCount != displayHeight - 1:

                yPixelCount += 1
                pixel = displayScreenshot.getpixel((xPixelCount,yPixelCount))
                red.append(pixel[0])
                green.append(pixel[1])
                blue.append(pixel[2])


    
    avgBlue = round(sum(blue)/len(blue))
    avgRed = round(sum(red)/len(red))
    avgGreen = round(sum(green)/len(green))
    avgColor = (avgRed, avgGreen, avgBlue)
    print(avgColor)
    # colorName = find_closest_color_name(avgRed, avgGreen, avgBlue)
    # hexColor = closest_color(avgColor)

    return avgColor



def writeToFile(hexColor):
    filename = os.path.expanduser('~/.config/cava/config')
    line_to_change = 177  
    new_content = f"foreground = '{hexColor}' "

    with open(filename, 'r') as file:
        lines = file.readlines()

    lines[line_to_change] = new_content + '\n'

    with open(filename, 'w') as file:
        file.writelines(lines)


def open_terminal_with_cava():
    if sys.platform == "linux" or sys.platform == "linux2":
        return subprocess.Popen(["kitty", "--title", "Kitty", "-e", "cava"])

def get_window_id(window_name):
    try:
        window_id = subprocess.check_output(['xdotool', 'search', '--name', window_name]).decode().strip()
        return window_id
    except subprocess.CalledProcessError:
        return None

def send_keystroke_to_window(window_id, key):
    # Save the currently focused window ID
    original_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()

    # Focus the target window, send the key, then refocus the original window
    subprocess.call(['xdotool', 'windowfocus', window_id])
    subprocess.call(['xdotool', 'key', '--window', window_id, key])
    subprocess.call(['xdotool', 'windowfocus', original_window_id])

# Example usage
# send_keystroke_to_window('window_id', 'r')


if __name__ == "__main__":
    
    opened = False
    while True:

        if opened == False:
            opened = True
            terminal = open_terminal_with_cava()
            time.sleep(1)
            windowID = get_window_id("Kitty")
        color = getAverageColorOfScreen(getUpperMonitorScreenShot(),upperMonitorWidth(),upperMonitorHeight())
        print(color)
        red = color[0]
        green = color[1]
        blue = color[2]

        x = rgb_to_hex(red,green,blue)
        print(x)

        writeToFile(x)
        send_keystroke_to_window(str(windowID),"r")
      

        time.sleep(20)


