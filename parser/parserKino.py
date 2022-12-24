import requests, json
API_TOKEN = ''


async def getMovieById(id):
    response = requests.get(f'https://api.kinopoisk.dev/movie?token={API_TOKEN}&search={id}&field=id')
    filmDict = json.loads(response.text)
    if response.status_code != 200: return None
    name = filmDict.get('name')
    description = filmDict.get('description').replace(u'\xa0', ' ')
    photo = filmDict.get('poster').get('url')
    genres = [gerne.get('name') for gerne in filmDict.get('genres')]
    

    return dict(name=name, description=description, photo=photo, genres=genres)
