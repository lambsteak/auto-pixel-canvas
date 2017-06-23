'''
Created on 19-Jun-2017

@author: thepenguin
'''

import pyautogui
from PIL import Image
import threading
import time
import logging
import os
import sys
import random
import pickle
#import commcon
import datetime


logging.basicConfig(filename='notebook.logs.notebook',level=logging.DEBUG, filemode='w', \
                    format='%(asctime)s %(message)s', datefmt='%m/%d %I:%M:%S %p')

logging.info('Program started running.')
'''
there are three ways: either add 50 to window_edge, or increase pixel_range to 50
or the third way is to find all possible colors in the canvas and remove
the target and exception colors from the clickables list
'''

#f=open("error",'a')
#sys.stderr=f

class Colors(object):
    
    def _get_color_meanings(self):
        color_meanings = dict()
        for color, value in self.colors.items():
            color_meanings[value]=color
        return color_meanings

    def __init__(self):
        self.colors={'white':(255,255,255),
                'light grey':(228,228,228),
                'dark grey':(136,136,136),
                'black':(34,34,34),
                'pink':(255,167,209),
                'red':(229,0,0),
                'orange':(229,149,0),
                'brown':(160,106,66),
                'yellow':(229,217,0),
                'light green':(148,224,68),
                'dark green':(2,190,1),
                'turquoise':(0,211,221),
                'dark turquoise':(0,131,99),
                'blue':(0,0,234),
                'light purple':(207,110,228),
                'dark purple':(130,0,128)
                }
        self.color_meanings=self._get_color_meanings()
    


def pause():
    logging.info("the pause/resume thread loop started running")
    logging.debug("configure database in file: configure")
    
    dbfile=open('configure', 'rb')
    db=pickle.load(dbfile)
    dbfile.close()
    logging.debug('pause thread: pause status just after start of pause(): %s'%db['pause'])
    print('pause status:', db['pause'])
    db['pause']='FALSE'
    logging.debug('pause thread: "configure" db dictionary is as follows:')
    for key, value in db.items():
        logging.debug('pause thread: ' + key + ' : ' + str(value))
    dbfile=open('configure','wb')
    pickle.dump(db,dbfile)
    dbfile.close()
    
    print("Program is running")
    #have two separate [in/out/err) streams for the pause thread's inf loop and the main thread
    while True:
        option=input('Enter "pause" to pause, "quit" to quit: ')
        if option.lower()=="pause":
            '''
            cfile=open('configure.conf','r')
            logging.debug("opened conf file (rmode) @line 23")
            older=cfile.readlines()
            cfile.close()
            cfile=open('configure.conf','w')
            cfile.write('pause=TRUE\n')
            for i in range(1,len(older)):
                cfile.write(older[i])
            cfile.close()
            '''
            logging.debug("pause thread: user selected 'pause'")
            dbfile=open('configure','rb')
            db=pickle.load(dbfile)
            dbfile.close()
            db['pause']='TRUE'
            dbfile=open('configure','wb')
            pickle.dump(db,dbfile)
            dbfile.close()
            logging.debug("pause thread: Program status: %s"%db['pause'])
            logging.info("Program paused.")
       
        elif option.lower()=='quit':
            print('Quitting the application..')
            logging.info("pause thread: user selected 'quit'")
            dbfile=open('configure','rb')
            db=pickle.load(dbfile)
            logging.debug("Initial status: %s"%db['pause'])
            dbfile.close()
            db['pause']='QUIT'
            dbfile=open('configure','wb')
            pickle.dump(db,dbfile)
            dbfile.close()
            logging.debug("pause thread: program status: %s"%db['pause'])
            logging.info('pause thread: calling sys.exit()')
            sys.exit()
            
        option=input('Enter "resume" to resume or "quit" to quit:')
        if option.lower()=='resume' or option.lower()=='r':
            '''cfile=open('configure.conf','r')
            older=cfile.readlines()
            cfile.close()'''
            logging.debug("pause thread: user selected 'resume'")
            dbfile=open('configure', 'rb')
            db=pickle.load(dbfile)
            logging.debug("pause thread: initial pause status: %s"%db['pause'])
            dbfile.close()
            
            '''
            cfile=open('configure.conf','w')
            cfile.write('pause=FALSE\n')
            for i in range(1,len(older)):
                cfile.write(older[i])
            cfile.close()
            '''
            db['pause']='FALSE'
            dbfile=open('configure','wb')
            pickle.dump(db, dbfile)
            dbfile.close()
            logging.debug("pause thread: program status: %s"%db['pause'])
            logging.info("Program resumed.")
        else:
            logging.info("pause thread: user selected 'quit' *after pausing*")
            dbfile=open('configure','rb')
            db=pickle.load(dbfile)
            logging.log("Initial status: %s"%db['pause'])
            dbfile.close()
            db['pause']='QUIT'
            dbfile=open('configure','wb')
            pickle.dump(db,dbfile)
            dbfile.close()
            logging.debug("pause thread: program status: %s"%db['pause'])
            logging.info('pause thread: calling sys.exit()')
            sys.exit()

'''
def build_colors_list(target_color, exception_colors):
    pixel_range=20
    target_colors=list()
    c=-pixel_range
    r=target_color[0]
    g=target_color[1]
    b=target_color[2]
    l=[r,g,b]
    cols=0
    while cols<3:
        c=0
        x=l[cols]
        while c<pixel_range:
            x+=c
            pix=(l[0],l[1],l[2])
            target_colors.append(pix)
            c+=1
        cols+=1
        
    exceptions_set=list()
    for color in exception_colors:
        c=-pixel_range
        r=color[0]
        g=color[1]
        b=color[2]
        l=[r,g,b]
        cols=0
        while cols<3:
            c=0
            x=l[cols]
            while c<pixel_range:
                x+=c
                pix=(l[0],l[1],l[2])
                exceptions_set.append(pix)
                c+=1
            cols+=1
            
    return target_colors, exceptions_set
    '''
'''
def build_colors_list(target_color, exception_colors):
    pixel_range=20
    target_set=list()
    print("target_color:",target_color)
    print("type: ",type(target_color))
    r=target_color[0]
    g=target_color[1]
    b=target_color[2]
    
    i=b-pixel_range
    while i<(b+pixel_range):
        j=g-pixel_range
        while j<(g+pixel_range):
            k=r-pixel_range
            while k<(r+pixel_range):
                target_set.append((k,j,i))
                k+=1
            j+=1
        i+=1
    
    q=0
    exception_set=list()
    while q<len(exception_colors):
        r=exception_colors[q][0]
        g=exception_colors[q][1]
        b=exception_colors[q][2]
        
        i=b-pixel_range
        while i<(b+pixel_range):
            j=g-pixel_range
            while j<(g+pixel_range):
                k=r-pixel_range
                while k<(r+pixel_range):
                    exception_set.append((k,j,i))
                    k+=1
                j+=1
            i+=1
        q+=1
    return (target_set, exception_set)
'''

def clickable_colors(color_tuple):
    logging.debug('clickable_colors() called')
    logging.debug('calling Colors() constructor')
    colors=Colors().colors
    logging.info('Clickable colors:')
    clickables=list()
    target_color=color_tuple[0]
    exception_colors=color_tuple[1]
    for key, value in colors.items():
        if value!=target_color and value not in exception_colors:
            logging.info(key+'\t'+str(value))
            clickables.append(value)
    logging.debug('No. of clickable colors:%d'%len(clickables))
    return clickables

def no_pixels_handler():
    print('NO PIXELS TO PAINT')
    pass

def print_intro():
    logging.debug('print_info() called..displaying "fig.png" file')
    Image.open('fig.png').show()
    logging.debug('"fig.png" file displayed')
    print('\n==Auto Pixelgrad==')
    print('author:lambsteak\nEmail : free.fries@yandex.com\n\n')
    
    print('Set up your screen: open a web browser window,')
    print('Resize your browser to split the screen vertically (see figure)')
    print('so that you have sufficient screen space to do your work etc')
    print('Enter the pixel canvas url, go to the image to be worked on')
    print('and zoom in, such that the browser\'s screen shows the specific')
    print('target area where you have: a target color, and a list of exception')
    print('colors..this program will paint all pixels which aren\'t in')
    print('exception list into the target color')
    print('Make sure that you have selected the target color in the canvas palette')
    print('cursor is at the left edge of window when you press Enter key')
    print('That\'s it!')
    print('NOTE: You can also set the configuration values through the')
    print('configuration.conf file. Run the get_coordsNcolors.py program to')
    print('get the coordinates and the RGB color of any pixel on screen')
    print('\nOnce done setting up the browser window, follow these steps:\n')
    logging.debug('print_intro() exited')
    

def get_confs(outer=True):
    #return all the vars to the global
    #cfile=open('configure.conf','w')
    #cfile.write('pause=FALSE\n')
    logging.debug('get_confs() called')
    print('Take your mouse cursor to the left edge of the browser window')
    print('and  press Enter in the terminal')
    input('>>>')    
    window_edge=pyautogui.position()[0]
    window_edge+=50
    #cfile.write('window_edge='+str(window_edge)+'\n')
    logging.debug('window_edge(50 added later for use)=%d'%(window_edge-50))
    print('Now take the mouse cursor to the top edge of browser web display')
    print('below the menu bar where the pixel canvas starts, and then press Enter')
    input('>>>')
    top_edge=pyautogui.position()[1]
    #cfile.write('top_edge='+str(top_edge)+'\n')
    logging.debug('top_edge=%d'%top_edge)
    
    print('Now move the mouse cursor to the lower edge above the color palette')
    print('and "no. of people online" widget and press Enter')
    input('>>>')
    bottom_edge=pyautogui.position()[1]
    #cfile.write('bottom_edge='+str(bottom_edge)+'\n')
    logging.debug('bottom_edge=%d'%bottom_edge)
    #could periodically scan for browser notification on screen
    #but that might be interruptive
    
    freeze_time=int(input('Freeze time after painting pixel (in seconds):'))
    #cfile.write('freeze_time='+str(freeze_time)+'\n')
    logging.debug('freeze time (in seconds) = %d'%freeze_time)
    '''
    print('Enter target color from the available colors.. ')
    print('with row no. and column no., eg "1 4" for black and "2 6" for blue')
    target_color=build_colors(input('>>>'))
    
    print('Enter exception colors (space-separated)')
    print('row# col# row# col# ...row# col#')
    print('Example: "1 6 2 8" for red and purple')
    '''
    print('You can either select the target and exception colors by pointing')
    print('at the color in canvas\'s palette or entering the name')
    colors=Colors().colors
    color_meanings=Colors().color_meanings
    col_c=0
    for color in colors.keys():
        col_c+=1
        print(col_c,'\t',color)
    target_obtained=False
    while not target_obtained:
        print('Either take the cursor to the target color in color palette and press Enter')
        print('Or enter the color name')
        a_input=input().lower()
        if not a_input:
            cur_pos=pyautogui.position()
            target_color=pyautogui.screenshot().getpixel(cur_pos)
            if target_color not in colors.values():
                logging.debug('target color doesn\'t match any predefined color')
                print('Target color didn\'t match any canvas color')
                continue
            target_obtained=True
        else:
            try:
                target_color=colors[a_input]
            except KeyError:
                print('Invalid color name given')
                continue
            target_obtained=True
    logging.debug('target color = %s, value = %s'\
                              %(color_meanings[target_color],str(target_color)))
    print('Target color obtained')
    #cfile.write('target_color='+str(target_color)+'\n')
    exception_colors=list()
    #exceptions_obtained=False
    #while not exceptions_obtained:
    print('Either take cursor to the exception color in palette and press Enter')
    print('Or enter the color names')
    print('When all exception colors are submitted, enter "done"')
    #cfile.write('exception_colors')

    a_input=input().lower()
    while a_input!="done":
        if not a_input:
            cur_pos=pyautogui.position()
            col=pyautogui.screenshot().getpixel(cur_pos)
            if not col in colors.values():
                print('Color value didn\'t match any canvas color, please retry')
            else:
                exception_colors.append(col)
                print('Color added to exception')
        else:
            if a_input in colors.keys():
                exception_colors.append(colors[a_input])
                print('Color added to exception')
            else:
                print('Given color didn\'t match any canvas value')
        a_input=input().lower()
        #cfile.write('='+str(col))
    #cfile.write('exception_colors='+str(exception_colors)+'\n')
    #cfile.write('\n')
    logging.debug('done taking exception colors')
    
    db = {}
    db['pause']='FALSE'
    db['window_edge']=window_edge
    db['top_edge']=top_edge
    db['bottom_edge']=bottom_edge
    db['freeze_time']=freeze_time
    db['target_color']=target_color
    db['exception_colors']=exception_colors
    dbfile=open('configure', 'wb')
    pickle.dump(db, dbfile)
    dbfile.close()

    colors=Colors().color_meanings
    print('The values given are:')
    for key in db.keys():
        if key=='pause':
            continue
        elif key=='target_color':
            print(key, ':', color_meanings[db[key]], db[key])
        elif key=='exception_colors':
            print('exception_colors :')
            for ele in db[key]:
                print('\t',color_meanings[ele], ele)
        else:
            print(key,' : ', db[key])
    a_input=input('Enter "y" to confirm or "n" to reinsert the values:').lower()
    if a_input=='n':
        logging.debug('reinserting the values')
        db=get_confs(outer=False)
    #return window_edge,top_edge,bottom_edge,freeze_time,target_color,exception_colors
    if outer:
        logging.debug('exiting get_confs()')
    return db

'''cfile=open('configure.conf','a')
cfile.close()
cfile=open('configure.conf','r')
lines=cfile.readlines()
cfile.close()'''

if os.path.isfile('configure'):
    logging.debug('at the start of main thread: configure file found')
    print('--Auto Pixelgrad--\nAuthor: lambsteak\nEmail: free.fries@yandex.com\n')
    user=input('Enter "y" to run program by previous configurations, else "n": ')
    if user.lower()=='y':
        logging.debug('user selected to run with previous configuration')
        dbfile=open('configure','rb')
        db=pickle.load(dbfile)
        dbfile.close()
    else:
        logging.debug('user selected to *not* run with previous configuration')
        print_intro()
        db=get_confs()
        logging.debug('at main thread: value obtained from user -- configure file overwritten')
else:
    logging.debug('printing intro and getting values from user')
    print_intro()
    db=get_confs()
    logging.debug('at main thread: value obtained from user -- new configure file created')

db['pause']='FALSE'
dbfile=open('configure', 'wb')
pickle.dump(db, dbfile)
dbfile.close()

logging.debug('stored configure file values in db dictionary')
window_edge=db['window_edge']
top_edge=db['top_edge']
bottom_edge=db['bottom_edge']
freeze_time=db['freeze_time']
target_color=db['target_color']
exception_colors=db['exception_colors']
logging.debug('(in main thread): values in db dictionary are as follows:')
for key, value in db.items():
    logging.debug(key+' : '+str(db[key]))
 
'''
try:
    dbfile=open('configure','rb')
    db=pickle.load(dbfile)
    dbfile.close()
    if db['pause']=='TRUE' or db['pause']=='QUIT':
        db['pause']='FALSE'
        dbfile=open('configure','wb')
        pickle.dump(db, dbfile)
        dbfile.close()
    user=input('Enter "y" to run program by previous configurations, else "n": ')
    if user.lower()=='y':
        window_edge=db['window_edge']
        top_edge=db['top_edge']
        bottom_edge=db['bottom_edge']
        freeze_time=db['freeze_time']
        target_color=db['target_color']
        exception_colors=db['exception_colors']
    else:
        print_intro()
        db=get_confs()
        window_edge=db['window_edge']
        top_edge=db['top_edge']
        bottom_edge=db['bottom_edge']
        freeze_time=db['freeze_time']
        target_color=db['target_color']
        exception_colors=db['exception_colors']
except:
    print('No configuration file available, creating now')
    print_intro()
    db=get_confs()
    window_edge=db['window_edge']
    top_edge=db['top_edge']
    bottom_edge=db['bottom_edge']
    freeze_time=db['freeze_time']
    target_color=db['target_color']
    exception_colors=db['exception_colors']

'''

'''
if not lines:
    print_intro()
    window_edge,top_edge,bottom_edge,freeze_time,target_color,exception_colors=get_confs()

else:
    if lines[0][:-1]=='pause=TRUE':
        cfile=open('configure.conf','w')
        cfile.write('pause=FALSE\n')
        for i in range(1,len(lines)):
            cfile.write(lines[i])
        cfile.close()
    user=input('Enter "y" to run program by previous configurations, else "n": ')
    if user.lower()=='y':
        #get values from conf file
        cfile=open('configure.conf','r')
        lines=cfile.readlines()
        cfile.close()
        window_edge=int(lines[1].split('=')[1].rstrip())
        top_edge=int(lines[2].split('=')[1].rstrip())
        bottom_edge=int(lines[3].split('=')[1].rstrip())
        freeze_time=int(lines[4].split('=')[1].rstrip())
        target_color=lines[5].split('=')[1].rstrip()
        exception_colors=lines[6].split('=')[1:]
        exception_colors[-1]=exception_colors[-1].rstrip()
        
    else:
        print_intro()
        window_edge,top_edge,bottom_edge,freeze_time,target_color,exception_colors=get_confs()
        print(type(target_color))
'''
    
print('program started..')
print('Press Enter to pause the program (always do that when any changes could')
print('occur in the screen area of the browser window')

logging.debug('in main thread: spawning pause thread')
interface_thread=threading.Thread(target=pause)
interface_thread.start()
logging.debug('in main thread: pause thread started')
logging.debug('main thread: sleeping for 0.2 seconds to allow pause thread to set up')
time.sleep(0.2)
                  
#file=open('pixeltable','w')
width,height=pyautogui.size()
logging.debug('screen size is (%d X %d), 65 subtracted for use',width,height)
width-=65
                  
captcha_fail=0

#target_set, exception_set = build_colors_list(target_color, exception_colors)
#print(target_set[:5])

colors=Colors().colors
color_meanings=Colors().color_meanings

if not os.path.isdir('notebook.logs.screenshots'):
    os.mkdir('notebook.logs.screenshots')
logging.debug('in main thread: calling clickable_colors()')
clickables=clickable_colors((target_color, exception_colors))
captcha_sent=False
#loop_count=0
logging.info('Entering the infinite main logic loop')
loop_cycle=0
#per_shot=commcon.get_cycles_per_shot()             #####
per_shot=20
logging.info('no. of loop cycles per screenshot is set at %d'%per_shot)
while True:
    loop_cycle+=1
    logging.debug('inside main logic loop: loop cycle #%d'%loop_cycle)
    dbfile=open('configure','rb')
    db=pickle.load(dbfile)
    dbfile.close()
    logging.debug('db dict\'s pause value is: %s'%db['pause'])
    if db['pause']=='QUIT':
        logging.info('db\'s pause value equalled "QUIT", **exiting main thread**')
        sys.exit(0)
    #xybreak=False
    logging.debug('calling pyautogui.screenshot()')
    scrn=pyautogui.screenshot()
    logging.debug('(in main logic loop): pyautogui.screenshot() returned')
    
    if loop_cycle%per_shot:
        #give name to file based on formatted date and time
        logging.debug('loop_cycle%per_shot gave true, opening file to write screenshot')
        fname='shot-%s-%d.png'%(datetime.datetime.now().strftime('%y%m%d%H%M%S'),loop_cycle)
        try:
            fname=os.path.join(os.getcwd(), 'notebook.logs.screenshots', fname)
        except Exception as e:
            print('Could not open the file, make sure that the program\'s folder is not modified')
            print(str(e))
            logging.info('While opening screenshot file, error occured: %s'%str(e))
            logging.info('Exiting the main thread')
            print('Restart the program')
            sys.exit()
        im_data=scrn.crop((window_edge,0,width,height))
        #file should be inside notebook.logs.screenshot directory
        logging.debug('writing scrn.crop() object (of type: %s) to file'%str(type(im_data))) 
        im_data.save(fname)
        logging.debug('screenshot written to file')
    #checkig for captcha or error dialogue boxes
    #parted_scrn=scrn.crop(window_edge,0,width,height)
    im_element=pyautogui.locateOnScreen('ok.png')
    if im_element!=None:
        logging.debug('"ok.png" located on screen')
        clickpoint=pyautogui.center(im_element)
        if clickpoint[0]>window_edge:
            logging.debug('"ok.png" located in operated screen area')
            pyautogui.click(clickpoint)
            logging.info('Point clicked at coord: %s , sleeping for 4 seconds'%str(clickpoint))
            time.sleep(4)
    elif pyautogui.locateOnScreen('ok2.png'):
        logging.debug('"ok2.png located on screen')
        clickpoint=pyautogui.center(pyautogui.locateOnScreen('ok2.png'))
        if clickpoint[0]>window_edge:
            logging.debug('"ok2.png" is in operated screen area')
            pyautogui.click(clickpoint)
            logging.info('Point clicked at coord: %s , sleeping for 4 seconds'%str(clickpoint))
            time.sleep(4)
    elif pyautogui.locateOnScreen('captcha.png')!=None:
        logging.info('Captcha located on screen')
        clickpoint=pyautogui.center(pyautogui.locateOnScreen('captcha.png'))
        if clickpoint[0]>window_edge:
            logging.debut('captcha in operated screen area')
            if captcha_fail>3 and not captcha_sent:
                logging.info('Sending captcha to C&C, captcha_fail = %d'%captcha_fail)
                parted_scrn=scrn.crop((window_edge,0,width,height))
                #send captcha to other humans to solve it
                #commcon.send_to_cc(parted_scrn, categ='captcha')       #### 
                #the above function will return after dealing with the captcha
                #so no need to sleep etc
                #captcha_sent=True
                #time.sleep(300)
                continue
            elif captcha_fail>2:
                logging.debug('captcha_fail = %d, user being informed of captcha'%captcha_fail)
                print('CAPTCHA verification appeared')
                #show dialof=g box
                #captcha_fail=0
                time.sleep(60)
                captcha_fail+=1
                continue
            logging.debug('clicking coord: (%d, %d) to bring browser in focus'%(window_edge+10,top_edge+10))
            pyautogui.click(window_edge+10, top_edge+10, duration=0.2)
            logging.debug('pressing F5 key')
            pyautogui.press('f5')
            logging.debug('sleeping for 10 seconds')
            time.sleep(10)
            print('CAPTCHA appeared')
            captcha_fail+=1
            continue
    else:
        logging.debug('no captchas or dialog boxes detected on screen')
        captcha_fail=0
        captcha_sent=False
    if pyautogui.locateOnScreen('skipad.png'):
        logging.debug('skip ad located on screen')
        clickpoint=pyautogui.center(pyautogui.locateOnScreen('skipad.png'))
        if clickpoint[0]>window_edge:
            logging.debug('skip ad is in operated screen area, clicking "skip ad" at %s'%str(clickpoint))
            pyautogui.click(clickpoint, duration=0.1)
                
    #click_count=0
    xyloop_count=-1
    xybreak=False
    for x in range(window_edge,width, random.randint(5, 10)):
        #logging.debug('inside x nested loop: x=%d'%x)
        scrn=pyautogui.screenshot()
        for y in range(top_edge,bottom_edge, random.randint(5, 10)):
            xyloop_count+=1
            pixel_color=scrn.getpixel((x,y))
            if xyloop_count%200:
                if pixel_color in color_meanings.keys():
                    color_name=color_meanings[pixel_color]
                else:
                    color_name='Not in list'
                logging.debug('inside y nested loop: (x,y)=(%d, %d), RGB=%s , Color: %s'%(x,y,str(pixel_color),color_name))
            #if pixel_color not in exception_colors and pixel_color!=target_color:
            #if pixel_color not in exception_set and pixel_color not in target_set:
            if pixel_color in clickables:
                logging.debug('pixel of clickable color found: (x,y)= (%d, %d)...'%(x,y))
                logging.debug('...  RGB: %s, color: %s'%(str(pixel_color),color_meanings[pixel_color]))
                dbfile=open('configure','rb')
                #pause_line=cfile.readlines()[0].split('=')[1][:-1]
                db=pickle.load(dbfile)
                dbfile.close()
                logging.debug('(inside clickable pixel procedure): pause value: %s'%db['pause'])
                pause_value=db['pause']
                if pause_value=='QUIT':
                    logging.debug('(inside clickable pixel procedure): pause value is "QUIT", calling sys.exit()')
                    sys.exit()
                while pause_value=="TRUE":
                    time.sleep(2)
                    #pause_line=cfile.readlines()[0].split('=')[1][:-1]
                    dbfile=open('configure','rb')
                    db=pickle.load(dbfile)
                    dbfile.close()
                    pause_value=db['pause']
                logging.debug('taking screenshot before clicking')
                fname='pixel_shot-%s-%d-before.png'%(datetime.datetime.now().strftime('%y%m%d%H%M%S'),loop_cycle)
                try:
                    logging.debug('creating file path for pre-click screenshot')
                    fname=os.path.join(os.getcwd(), 'notebook.logs.screenshots', fname)
                    logging.debug('opening pre-click screenshot file')
                    
                except Exception as e:
                    logging.info('Error occured in opening pixel_screenshot file')
                    print('Could not open the file at required directory')
                    print('Make sure that the program\'s parent folder is not modified.')
                    logging.info('Exiting the main thread')
                    sys.exit()
                sff=pyautogui.screenshot().crop((window_edge,0,width,height))
                sff.save(fname)
                orig_pos=pyautogui.position()
                pyautogui.click(x+4,y+4, duration=0.3)
                logging.info('Point clicked at (%d, %d), taking screenshot again after clicking'%(x+4,y+4))
                #exactly same name as that of before clicking shot, except append "after"
                fname=fname[:-10]
                fname+='after.png'
                logging.debug('filename for post click screenshot: %s'%fname)
                try:
                    sff=open(fname, 'wb')
                    sff.close()
                except Exception as e:
                    print('Could not open the file at required folder')
                    print('Make sure that the program\'s parent folder is not modified.')
                    logging.info('Exiting the main thread')
                    sys.exit()
                sff=pyautogui.screenshot().crop((window_edge,0,width,height))
                sff.save(fname)
                logging.debug('screenshot written to file')
                #pyautogui.hotkey('alt','\t')
                
                #click_count+=1
                #if click_count>2:
                    #click_count=0
                xybreak=True
                break
        if xybreak==True:
            logging.debug('xy loop exiting with xybreak flag as True')
            break
    pyautogui.hotkey('alt','\t')
    logging.debug('taking curose to original position')
    pyautogui.moveTo(orig_pos)

    '''
    if loop_count%10==0:
        sdb=shelve.open('screenshots_log','ab')
        try:
            image_count=sdb['count']
        except KeyError:
            sdb['count']=0
        sdb['count']+=1
        filename='screenshot-%d'%sdb['count']
        sdb.close()
        im_content==pyautogui.screenshot().crop(window_edge,0,width,height)
        shh=open(filename,'wb')
        shh.write(im_content)
        shh.close()
        '''
    if xybreak==False:
        logging.debug('exited xy loop with xybreak flag as False (no pixel clicked(?))')
        pyautogui.press('Enter')
        nopix_scn=pyautogui.screenshot()
        nopix_scn=nopix_scn.crop((window_edge,0,width,height))
        fname='no_clicks_shots-%s-%d.png'%(datetime.datetime.now().strftime('%y%m%d%H%M%S'), loop_cycle)
        logging.debug('creating file path for post-no-clicks screenshot')
        fname=os.path.join(os.getcwd(), 'notebook.logs.screenshots', fname)
        logging.debug('opening post-no-clicks screenshot file')
        sff.save(fname)
        #the dev will send a multidimensional array instructing coords
        #and keypresses at specific coords
        #commcon.send_to_dev(nopix_scn, categ='no_pixels_scrn')             ######
        print('***NO PIXELS TO COLOR')
        logging.info("No pixels found to color")
        no_pixels_handler()
    else:
        no_pixels_count=0
    #click_count+=1
    #if click_count>(4+random.randint(0,5)):
    logging.debug('sleeping for freeze time = %d seconds'%freeze_time)
    time.sleep(freeze_time)
        #click_count=0
        
    
