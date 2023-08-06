import enum
from ThinkDashboardAgent.providers.database_provider import DatabaseProvider
from ThinkDashboardAgent.providers.elasticsearch_provider import ElasticsearchProvider
from ThinkDashboardAgent.providers.redis_provider import RedisProvider
from ThinkDashboardAgent.providers.site_provider import SiteProvider
from ThinkDashboardAgent.providers.ssl_provider import SSLProvider

DASHBOARD_URL = 'http://192.168.1.106:8000/api/'

class SERVICE_TYPE(enum.Enum):
    ELASTICSEARCH:str = 'ELASTICSEARCH'
    DATABASE:str = 'DATABASE'
    SSL:str = 'SSL'
    SITE:str = 'SITE'
    REDIS:str = 'REDIS'

PROVIDERS={
        'site':SiteProvider,
        'redis': RedisProvider,
        'ssl' : SSLProvider,
        'database': DatabaseProvider,
        'elasticsearch' : ElasticsearchProvider
    }