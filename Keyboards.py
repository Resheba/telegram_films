import asyncio
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from dbAPI import getFilmsIds, db_start, getMultFilmsIds, getSerialSeries, getSeriesIds


async def channelsLinks(channels:dict):
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True)
    for channel in channels:
        Keyboard.add(InlineKeyboardButton(text = channel.get('name'), url=channel.get('link')))

    Keyboard.add(InlineKeyboardButton(text = 'Проверить', callback_data='checkChannels'))

    return Keyboard

async def echoMark(*args):
    Keyboard = ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    for i in args:
        Keyboard.insert(KeyboardButton(str(i)))
    return Keyboard

class AfterCheck:
    button_create = KeyboardButton('/start')
    button_channels = KeyboardButton('/channels')

    Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True).add(button_create, button_channels)

class AdminMenu:
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=1)

    button_channels = InlineKeyboardButton(text = 'Управление каналами', callback_data='ChannelsMenu')
    button_films = InlineKeyboardButton(text = 'Управление фильмами/мульт', callback_data='FilmsMenu')
    button_serials = InlineKeyboardButton(text = 'Управление сериалами', callback_data='SerialsMenu')
    button_static = InlineKeyboardButton(text = 'Статистика', callback_data='StaticMenu')
    button_mail = InlineKeyboardButton(text='Рассылка', callback_data='mailMenu')

    Keyboard.add(button_channels, button_films, button_serials, button_static,button_mail)

class MailMenu:
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True)

    button_new = InlineKeyboardButton(text = 'Новая рассылка', callback_data='newMail')
    Keyboard.add(button_new)
    Keyboard.add(InlineKeyboardButton(text = 'Назад', callback_data='adminMenu'))

class ChannelsMenu:
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True)

    button_add = InlineKeyboardButton(text = 'Новый канал', callback_data='addNewChannnel')
    button_list = InlineKeyboardButton(text = 'Список каналов', callback_data='channelsList')
    button_delete = InlineKeyboardButton(text = 'Удалить канал', callback_data='channelDelete')

    Keyboard.add(button_list, button_add, button_delete)
    Keyboard.add(InlineKeyboardButton(text = 'Назад', callback_data='adminMenu'))

FilmMultCreate = CallbackData('Mtype', 'typeid')

class FilmsMenu:
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=1)

    button_add = InlineKeyboardButton(text = 'Новый фильм', callback_data='Mtype:0')
    button_addMult = InlineKeyboardButton(text = 'Новый мультфильм', callback_data='Mtype:2')
    button_list = InlineKeyboardButton(text = 'Список фильмов', callback_data='filmsList')
    button_listMult = InlineKeyboardButton(text = 'Список мультфильмов', callback_data='multfilmsList')
    button_delete = InlineKeyboardButton(text = 'Удалить фильм', callback_data='filmDelete')

    Keyboard.add(button_list, button_listMult, button_add, button_addMult, button_delete)
    Keyboard.add(InlineKeyboardButton(text = 'Назад', callback_data='adminMenu'))

class SeriesMenu:
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=1)

    button_add_content = InlineKeyboardButton(text = 'Новый сериал', callback_data='addNewSerial')
    button_add_seria = InlineKeyboardButton(text = 'Новая серия', callback_data='addNewSeria')
    button_list = InlineKeyboardButton(text = 'Список сериалов', callback_data='serialsList')
    button_delete = InlineKeyboardButton(text = 'Удалить сериал', callback_data='serialDelete')
    button_delete_seria = InlineKeyboardButton(text = 'Удалить серию', callback_data='seriaDelete')

    Keyboard.add(button_list, button_add_content, button_delete, button_add_seria, button_delete_seria)
    Keyboard.add(InlineKeyboardButton(text = 'Назад', callback_data='adminMenu'))

class StatisticMenu:
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True)

    button_add = InlineKeyboardButton(text = 'Прибавить/Убавить', callback_data='changeStatic')

    Keyboard.add(button_add)
    Keyboard.add(InlineKeyboardButton(text = 'Назад', callback_data='adminMenu'))

class Back2MailMenuMark:
    button_back = KeyboardButton(text = 'Отмена', callback_data='mailMenu')

    Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_back)

class Back2StatickMenuMark:
    button_back = KeyboardButton(text = 'Отмена', callback_data='StaticMenu')

    Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_back)

class Back2ChannelsMenuMark:
    button_back = KeyboardButton(text = 'Отмена', callback_data='ChannelsMenu')

    Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_back)

class Back2ChannelsMenu:
    button_back = InlineKeyboardButton(text = 'Отмена', callback_data='ChannelsMenu')

    Keyboard = InlineKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_back)

class Back2FilmsMenuMark:
    button_back = KeyboardButton(text = 'Отмена', callback_data='FilmsMenu')

    Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_back)

class Back2FilmsMenu:
    button_back = InlineKeyboardButton(text = 'Отмена', callback_data='FilmsMenu')

    Keyboard = InlineKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_back)

class Back2SerialsMenuMark:
    button_back = KeyboardButton(text = 'Отмена', callback_data='SerialsMenu')

    Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_back)

class Back2SerialsMenu:
    button_back = InlineKeyboardButton(text = 'Отмена', callback_data='SerialsMenu')

    Keyboard = InlineKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_back)

FilmRedirectCallBack = CallbackData('film', 'movieId')
SeriesRedirectCallback = CallbackData('series', 'movieId', 'seria', 'season')

async def filmRedirectKeyboard(movieId):
    button_video = InlineKeyboardButton(text='Смотреть', callback_data=f'film:{movieId}')
    #button_show = InlineKeyboardButton(text = 'Смотреть на канале', url=filmLink)
    Keyboard = InlineKeyboardMarkup().add(button_video)

    return Keyboard

async def seriesSeasonsKeyboard(movieId, page: int = 1):
    series = await getSerialSeries(movieId)
    seasons = list(set(t[0] for t in series))
    seasons.sort()
    Keyboard = InlineKeyboardMarkup()

    pageContent = seasons[5*(page-1):5*page]
    for season in pageContent:
        Keyboard.add(InlineKeyboardButton(f'{season} Сезон', callback_data=f'Scontent:{movieId}:1:{season}'))
    serv_buttons = []

    if page != 1:
        serv_buttons.append(InlineKeyboardButton('Пред.', callback_data=f'Scontent:{movieId}:{page-1}:'))
    if len(seasons) > 5*page:
        serv_buttons.append(InlineKeyboardButton('След.', callback_data=f'Scontent:{movieId}:{page+1}:'))
    
    Keyboard.add(*serv_buttons)    
    return Keyboard

async def seriesSeriasKeyboard(movieId, season: int, page: int = 1):
    series = await getSerialSeries(movieId)
    series = list(set(t[1] for t in series if t[0] == season))
    series.sort()
    Keyboard = InlineKeyboardMarkup()

    pageContent = series[5*(page-1):5*page]
    for seria in pageContent:
        Keyboard.add(InlineKeyboardButton(f'{seria} серия', callback_data=f'series:{movieId}:{seria}:{season}'))
    serv_buttons = []

    if page != 1:
        serv_buttons.append(InlineKeyboardButton('Пред.', callback_data=f'Scontent:{movieId}:{page-1}:{season}'))
    if len(series) > 5*page:
        serv_buttons.append(InlineKeyboardButton('След.', callback_data=f'Scontent:{movieId}:{page+1}:{season}'))
    
    Keyboard.add(*serv_buttons) 
    Keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'Scontent:{movieId}:1:'))  
    return Keyboard

class AfterCheckMenu:
    button_rand = InlineKeyboardButton(text = 'Рандомный фильм', callback_data='RandFilm')
    button_list = InlineKeyboardButton(text = 'Список фильмов', callback_data='Fpage:1')
    button_serials = InlineKeyboardButton(text = 'Список сериалов', callback_data='Spage:1')
    button_search = InlineKeyboardButton(text='🔍Поиск', switch_inline_query_current_chat='')
    button_listMult = InlineKeyboardButton(text = 'Список мультфильмов', callback_data='Mpage:1')
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=1).add(button_rand, button_list, button_serials, button_listMult, button_search)

class YesNoMark:
    button_yes = KeyboardButton(text = 'Да')
    button_no = KeyboardButton(text = 'Нет')

    Keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).add(button_yes, button_no)

class SwitchToBot:
    button_search = InlineKeyboardButton(text='🔍Найти', switch_inline_query_current_chat='')

    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_search)

class FilmList:
    button_search = InlineKeyboardButton(text='🔍Найти', switch_inline_query_current_chat='')
    button_back = InlineKeyboardButton(text='Назад', callback_data='start')

    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_search, button_back)

class Search:
    button_search = InlineKeyboardButton(text='🔍Поиск', switch_inline_query_current_chat='')

    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True).add(button_search)

FContentCallback = CallbackData('Fcontent', 'id')
SContentCallback = CallbackData('Scontent', 'id', 'page', 'season')
ListFilmsCallback = CallbackData('Fpage', 'num')
ListSeriesCallback = CallbackData('Spage', 'num')
ListMultFilmsCallback = CallbackData('Mpage','num')

async def multFilmsListKeyboard(page: int = 1):
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=2)
    films = await getMultFilmsIds()
    films.reverse()
    pageContent = films[5*(page-1):5*page]
    for id, name in pageContent:
        Keyboard.add(InlineKeyboardButton('🪷'+name, callback_data=f'Fcontent:{id}'))
    serv_buttons = []

    if page != 1:
        serv_buttons.append(InlineKeyboardButton('Пред.', callback_data=f'Mpage:{page-1}'))
    if len(films) > 5*page:
        serv_buttons.append(InlineKeyboardButton('След.', callback_data=f'Mpage:{page+1}'))
    
    Keyboard.add(*serv_buttons)
    Keyboard.add(InlineKeyboardButton('🔙Глав. меню', callback_data='start'))
    return Keyboard

async def filmsListKeyboard(page: int = 1):
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=2)
    films = await getFilmsIds()
    films.reverse()
    pageContent = films[5*(page-1):5*page]
    for id, name in pageContent:
        Keyboard.add(InlineKeyboardButton('📽'+name, callback_data=f'Fcontent:{id}'))
    serv_buttons = []

    if page != 1:
        serv_buttons.append(InlineKeyboardButton('Пред.', callback_data=f'Fpage:{page-1}'))
    if len(films) > 5*page:
        serv_buttons.append(InlineKeyboardButton('След.', callback_data=f'Fpage:{page+1}'))
    
    Keyboard.add(*serv_buttons)
    Keyboard.add(InlineKeyboardButton('🔙Глав. меню', callback_data='start'))  
    return Keyboard

async def SeriesListKeyboard(page: int = 1):
    Keyboard = InlineKeyboardMarkup(one_time_keyboard=True, row_width=2)
    films = await getSeriesIds()
    films.reverse()
    pageContent = films[5*(page-1):5*page]
    for id, name in pageContent:
        Keyboard.add(InlineKeyboardButton('🪐'+name, callback_data=f'Scontent:{id}:1:'))
    serv_buttons = []

    if page != 1:
        serv_buttons.append(InlineKeyboardButton('Пред.', callback_data=f'Spage:{page-1}'))
    if len(films) > 5*page:
        serv_buttons.append(InlineKeyboardButton('След.', callback_data=f'Spage:{page+1}'))
    
    Keyboard.add(*serv_buttons)
    Keyboard.add(InlineKeyboardButton('🔙Глав. меню', callback_data='start'))
    return Keyboard

# asyncio.run(db_start())
# asyncio.run(filmsListKeyboard())