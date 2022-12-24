from aiogram.utils.markdown import link, hlink, quote_html
from dbAPI import getFilms, getMoviesCheckedCount, getSerialSeries, getUserCount

API_TOKEN = ''
INLINE_RESULT_LIMIT = 20

ADMINS = [
    1391069512,
    526836949,
    866932903,
]

INSTRUCTION = '''<b>ЧТО ПОЗВОЛЯЕТ ДЕЛАТЬ БОТ?</b>

В нашем боте "Кинолама" Вы можете искать фильмы, сериалы и мультфильмы! Смотреть их, добавлять в избранное, скачивать и смотреть без интернета!


<b>КАК ПОЛЬЗОВАТЬСЯ БОТОМ?</b>

Введи <code>@KinolamaBot</code> и выбери фильм/сериал/мультфильм из списка😊 А также Вы можете просмотреть список нажав на соответствующие кнопки в меню бота.'''

async def filmCaption(film:dict):
    description = film.get('description')
    id = f"<u>#{film.get('id') or 'id'}</u>"
    name = f'<b>{film.get("name")}</b>'

    caption = f'{name}\n\n{id}\n\n{description}'
    return caption

async def filmListCaption():
    caption = ''
    films = await getFilms()
    for i, film in enumerate(films):
        name = film.get('name')
        #link = film.get('link')
        #caption += f'{i+1} <u>{hlink(name, link)}</u>\n'
        caption += f'{i+1} <u>{name}</u>\n'
    return caption

async def serisCaption(content, season, series):
    caption = ''
    name = content.get('name')
    caption += f'<b>{name}</b>\nСезон {season}, серия {series}'
    return caption

async def serialInfoCaption(serialId, name):
    caption = f'Для просмотра сериала <b>{name}</b>,\n<em>введите команду</em> <b>/movie {serialId} [сезон] [серия]</b>\nДоступные серии:\n'
    series = await getSerialSeries(serialId)
    series.sort()
    for season, seria in series:
        caption += f'Сезон {season} серия {seria}\n'
    return caption

async def filmVideoCaption(film:dict):
    name = film.get('name')
    description = film.get('description')
    caption = f'<b>{name}</b>\n\n{description}\n'
    return caption