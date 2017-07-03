"""The module for communicating with the task group and acting on the messages
recieved."""
import requests
import time
import json
import threading


class Commcon:
    """
    The communication is based on web-based HTTP requests instead of the easier
    to implement raw sockets for this case, thus making the external
    communication very easily implementable on a wide range of systems
    without bothering about firewalls. JSON format is used to transfer
    information given its support for the universal data structures of
    dictionaries and arrays.
    """
    url = 'https://lambsteaklab.herokuapp.com/pixelcanvas'

    def __init__(self, username, password, token,
                 logfile='notebook.logs.notebook'):
        self.username = username
        self.password = password
        self.token = token
        self.logfile = logfile
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
        r = requests.post(url, json=params).json()
        r = json.loads(r)
        if not config:
            return r
        return r.get(config)

    def listen_to_cc(self):
        while True:
            params = self.params
            params['state'] = self.get_state()
            params['task_desc'] = 'polling'
            r = requests.post(url, json=params).json()
            if r:
                r = json.loads(r)
                self.parse_commands(r)
            else:
                time.sleep(20)
            time.sleep(5)

    def send_to_cc(self, file, categ):
        params = self.params
        params['state'] = self.get_state()
        params['task_desc'] = categ
        files = {'file': open(file, 'rb')}
        req_token = requests.post(url, files=files, json=params).json()
        resp = requests.post(url, data=req_token)
        while not resp:
            time.sleep(10)
            resp = requests.post(url, data=req_token)
        return self.parse_commands(resp)

    def parse_commands(self, command):
        """By parsing the dictionaries and arrays, determine the actions
        to be performed."""
        pass
