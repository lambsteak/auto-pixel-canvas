# auto-pixel-canvas
Automatically supply intelligent clicks to targeted kinds of pixel blocks in a dynamic canvas element.
It is inspired by the specific requirements for pixelcanvas.io and has been tested to work well on that canvas.

What it does:
Using auto-pixel-canvas, a user can open up a web browser with pixelcanvas.io (or other similar platforms) and pin the browser window to a specific subpart of the screen area, where the pixel canvas's area to be worked on is visible in the browser window on screen. As long as the browser window is available on screen the user can use the desktop for other tasks while the auto-pixel-canvas application will automatically supply clicks to the desired coordinates on the canvas without affecting the workflow of other programs running on the computer, and by extension, without disrupting the user's attention. It also means that the needed pixel coordinates on the canvas will keep getting clicked with the right color even when the user is away from computer or is engaged in some other activity.

Requirements:
auto-pixel-canvas requires pyautogui package. It can be installed using pip as: pip install pyautogui
Read http://pyautogui.readthedocs.io/en/latest/install.html for details.
Additionally for Linux systems scrot is required for screenshot facilities. scrot can be installed by running: sudo apt-get install scrot
