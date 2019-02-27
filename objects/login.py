import requests
import yaml


class LoginSession:

    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False

    def load_cred(self, filename):

        with open(filename, 'r') as stream:
            try:
                self.secrets= yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def login(self):
        if not hasattr(self, 'secrets'):
            raise ValueError("'secrets' attribute has not been set.  Use 'load_cred' to load secrets")

        self.session.post(
            self.secrets['login_url'],
            data = self.secrets['cred_data'],
            allow_redirects=True
        )

        if self.session.cookies.get_dict():
            self.logged_in = True
