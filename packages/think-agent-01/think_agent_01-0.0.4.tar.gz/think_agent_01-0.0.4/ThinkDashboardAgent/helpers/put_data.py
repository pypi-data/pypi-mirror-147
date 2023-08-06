import requests

from ThinkDashboardAgent.main.settings import DASHBOARD_URL


def put_data(data,token):
    url = DASHBOARD_URL
    print(token)
    res = requests.put(
        url=url,
        headers={
            'Authorization': f'Token {token}'
        },
        data=data)
    return res.status_code







