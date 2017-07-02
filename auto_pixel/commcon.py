"""The module for communicating with the task group and acting on the messages
recieved."""
import requests
import json

class Commcon:
    url = 'https://lambsteaklab.herokuapp.com/pixelcanvas'
    def __init__(self, username, password, token):
        self.username = username
        self.password = password
        self.token = token
        self.params = {'username': self.username, 'password': self.password,
                       'token': self.token}

    def get_cycles_per_shot():
        r = requests.get(url, params=self.params)
        r = r.json()
        return r.get('cycles_per_shot')  # does it work this way?

    def send_to_cc(file, categ):
        r = requests.post(url)
        pass


    def _recieve_from_cc(file_with_address):
        # download the required file or wait until the required file is created
        # open the file and parse it:
        # the file will be a json file
        pass


    def send_to_dev():
        pass
