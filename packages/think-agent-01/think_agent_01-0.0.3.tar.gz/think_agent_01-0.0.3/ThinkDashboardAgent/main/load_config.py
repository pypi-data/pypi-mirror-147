from ThinkDashboardAgent.main.base import Config, get_data
from ThinkDashboardAgent.helpers.put_data import put_data
from ThinkDashboardAgent.main.settings import PROVIDERS


def config_list()->list:
    l:list = []
    for i, j in get_data().items():
        l.append(Config(key=i))
    l.pop(0)

    return l


def get_provider(config):
    try:
        return PROVIDERS.get(config.type)(config=config).check()
    except Exception as e:
        return e


def run():
    list:dict ={}
    for config in config_list():
        list[config.key] = get_provider(config)
    put_data(data=list,token=get_data().get('token').get('token'))
    print(list)

