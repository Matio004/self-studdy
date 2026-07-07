import requests

from model import Episodes, Show, Seasons


def get_show(name):
    response = requests.get('https://api.tvmaze.com/singlesearch/shows', params={'q': name})
    
    response.raise_for_status()  # todo proper error handling

    return Show.model_validate(response.json())

def get_seasons(id):
    response = requests.get(f'https://api.tvmaze.com/shows/{id}/seasons')
    
    response.raise_for_status()  # todo proper error handling

    return Seasons.validate_python(response.json())

def get_episodes(id):
    response = requests.get(f'https://api.tvmaze.com/seasons/{id}/episodes')
    
    response.raise_for_status()  # todo proper error handling

    return Episodes.validate_python(response.json())