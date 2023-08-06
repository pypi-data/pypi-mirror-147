from typing import Dict, Any
import yaml


def get_data() -> Dict[str,Any]:
    with open('config.yaml') as f:
        data:Dict[str,Any] = yaml.load(f,Loader=yaml.FullLoader)
    return data







