from ThinkDashboardAgent.helpers.get_data import get_data


class Config:

    def __init__(self,key):
        self.key = key
        self.data = get_data().get(f'{self.key}')
        self.ip = self.data.get('ip',None)
        self.port = self.data.get('port',None)
        self.dbname = self.data.get('dbname',None)
        self.username = self.data.get('username',None)
        self.password = self.data.get('password',None)
        self.site_url = self.data.get('site_url',None)
        self.type = self.data.get('type', None)
        self.token = get_data().get('token')


class BaseProveder:
    def __init__(self,config:Config):
        self.config:Config = config


    def check(self):
        return False


