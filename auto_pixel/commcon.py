"""The module for communicating with the task group and acting on the messages
recieved."""
import requests
import time
import json
import threading
import pyautogui
from string import ascii_letters


class Commcon:
    """
    The communication is based on web-based HTTP requests instead of the easier
    to implement raw sockets for this case, thus making the external
    communication very easily implementable on a wide range of systems
    without bothering about firewalls. JSON format is used to transfer
    information given its support for the universal data structures of
    dictionaries and lists.
    The url here will need to be replace with the domain name that the
    user group will be using for this purpose.
    **The server side program is not running at the moment.**
    """
    url = 'https://lambsteaklab.herokuapp.com/pixelcanvas'

    def __init__(self, username, password, token,
                 logfile='notebook.logs.notebook'):
        self.username = username
        self.password = password
        self.token = token
        self.logfile = logfile
        self.db = None
        self.config = self.get_configs()
        self.start_time = time.time()
        self.params = {'username': self.username, 'password': self.password,
                       'token': self.token, 'state': self.get_state}

        listen_thread = threading.Thread(target=self.listen_to_cc)
        listen_thread.start()

    def get_state(self):
        running_time = time.time()-self.start_time
        f = open(self.logfile, 'rb')
        logs = [i.rstrip() for i in f.readlines()[-(self.config['loglines']):]]
        f.close()
        return {'running_time': running_time, 'logs': '\n'.join(logs)}

    def get_configs(self, config=None):
        params = self.params
        params['state'] = self.get_state()
        if config:
            params['task_desc'] = config
        r = requests.post(self.url, json=params).json()
        r = json.loads(r)
        if not config:
            return r
        return r.get(config)

    def set_client_confs(db):
        self.db = db

    def listen_to_cc(self):
        params = self.params
        params['task_desc'] = 'polling'
        polling_id = None
        while True:
            params['state'] = self.get_state()
            if polling_id:
                params['polling_id'] = polling_id
            r = requests.post(self.url, json=params)
            if r.text:
                if len(r.text) < 2048:
                    r = json.loads(r)
                    if r.get('polling_id'):
                        polling_id = r.get('polling_id')
                    self.parse_commands(r)
                else:
                    txt_part = r.content[:2048].rstrip()
                    txt_part = json.dumps(txt_part)
                    with open('file_from_cc', 'wb') as bfile:
                        bfile.write(r.content[2048:])
                        self.parse_commands(txt_part, bfile)
                    # do whatever is needed with that file
                    # eg first n bytes of file contain info about
                    # what to do and thus parse it
            else:
                time.sleep(20)
            time.sleep(5)

    def send_to_cc(self, file, categ):
        params = self.params
        params['state'] = self.get_state()
        params['task_desc'] = categ
        files = {'file': open(file, 'rb')}
        req_token = requests.post(self.url, files=files, json=params).json()
        resp = requests.post(self.url, data=req_token).json()
        while not resp:
            time.sleep(10)
            resp = requests.post(self.url, data=req_token).json()
        return self.parse_commands(resp)

    def send_text(self, message):
        params = self.params
        params['message'] = message
        r = requests.post(self.url, json=params).json()
        return r

    def send_file(self, file):
        params = self.params
        files = {'file': open(file, 'rb')}
        r = requests.post(self.url, files=files, json=params).json()
        return r

    def parse_commands(self, command, file=None):
        """By parsing the dictionaries and arrays, determine the actions
        to be performed."""
        if not self.db:
            return
        if file:
            # act accordingly
            pass
        action_table = {'moveTo': pyautogui.moveTo,
                        'moveRel': pyautogui.moveRel,
                        'position': pyautogui.position,
                        'click': pyautogui.click,
                        'rightClick': pyautogui.rightClick,
                        'scroll': pyautogui.scroll,
                        'screenshot': pyautogui.screenshot,
                        'press': pyautogui.press,
                        'keyDown': pyautogui.keyDown,
                        'keyUp': pyautogui.keyUp
                        }
        if command['kind'] == 'special case':
            for action, obj in command['action sequence']:
                if action == 'click':
                    if (obj[0] > self.db['window_edge']) and\
                            (obj[1] < self.db['bottom_edge']) and\
                            (obj[1] > self.db['top_edge']):
                        pyautogui.click(*obj)
                elif action == 'screenshot' or action == 'scroll':
                    if action == 'scroll':
                        pyautogui.scroll(*obj)
                    scr = pyautogui.screenshot()
                    scr = scr.crop((self.db['window_edge'], 0, self.db['width'],
                                    self.db['height']))
                    scr.save('tmp_screenshot.png')
                    self.send_file('tmp_screenshot.png')
                    return
                elif action in ['press', 'keyDown', 'keyUp']:
                    if obj[0] not in ascii_letters and obj[0] not in\
                            ['shift', 'ctrl']:
                        return
                    else:
                        action_table[action](*obj)
                else:
                    action_table.get(action)(*obj)
