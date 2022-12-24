from asyncio import sleep
from aiogram import Bot, Dispatcher, executor, types
from Keyboards import *
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from aiogram.dispatcher import FSMContext
from aiogram.types.input_media import InputMedia
from parser.parserKino import getMovieById
from states import ChannelGroup, FilmGroup, MailGroup, SeriesGroup, StaticGroup
from filters import IsAdminFilter
from dbAPI import *
from aiogram.utils.markdown import hlink
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging, random


async def adminStatic():
    global ADD_USER_COUNT, ADD_MOVIE_PRESSED_COUNT
    realUserCount = await getUserCount()
    addUserCount = ADD_USER_COUNT

    realmoviesPressedCount = await getMoviesCheckedCount()
    addgetMoviesCheckedCount = ADD_MOVIE_PRESSED_COUNT

    caption = f'Количество пользователей: <b>{realUserCount}</b> + <em>{addUserCount}</em> (добавочные)\nКоличество просмотров movie: <b>{realmoviesPressedCount}</b> + <em>{addgetMoviesCheckedCount}</em> (добавочные)\n'
    return caption

#_____________Config_______________
from config import API_TOKEN, ADMINS, INLINE_RESULT_LIMIT, filmCaption, filmListCaption, filmVideoCaption, serialInfoCaption, serisCaption, INSTRUCTION

ADD_USER_COUNT = 0
ADD_MOVIE_PRESSED_COUNT = 0

logging.basicConfig(level = logging.INFO)
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
dispatcher.filters_factory.bind(IsAdminFilter)

async def on_startup(_):
    await db_start()

async def checkMemberTF(message: types.Message):
    for channel in await getChannels():
        chat_member = await bot.get_chat_member(chat_id=channel.get('telegram_id'), user_id=message.from_user.id)
        if chat_member['status'] == 'left':
            return False
    return True

async def checkMemberList(user_id):
    subList = []
    for channel in await getChannels():
        try:
            chat_member = await bot.get_chat_member(chat_id=channel.get('telegram_id'), user_id=user_id)
            if chat_member['status'] == 'left':
                subList.append(channel)
        except: continue
    return subList

#---------------------

@dispatcher.callback_query_handler(text='checkChannels')
async def subPostCheck(message: types.Message):
    if isinstance(message, types.CallbackQuery): message = message.message
    await message.delete()
    missedChannels = await checkMemberList(message.chat.id)
    if missedChannels:
        return await message.answer('Чтобы получить доступ к фильмам, Вам нужно подписаться👇', reply_markup=await channelsLinks(missedChannels))
    await start(message)

@dispatcher.message_handler(commands=['start'])
@dispatcher.callback_query_handler(text='start')
async def start(message: types.Message):
    if isinstance(message, types.CallbackQuery): message = message.message
    #if not await checkMemberTF(message): return await subPostCheck(message)
    if not await getUser(message.from_id):
            await createUser(message.from_id)
            resultUserCount = await getUserCount() + ADD_USER_COUNT
            resiltMoviesPressed = await getMoviesCheckedCount() + ADD_MOVIE_PRESSED_COUNT
            await message.answer(f'Здравствуйте, {message.from_user.first_name}!\n\nСмотрите с комфортом самые популярные фильмы, мультфильмы и сериалы прямо в телеграм абсолютно бесплатно и в хорошем качестве!☺️\n\nКинолама ждëт тебя🤗', parse_mode='HTML')
            await message.answer(f'🔴📢Нас уже <b>{resultUserCount}</b>! Через бот просмотрено более <b>{resiltMoviesPressed}</b> 📺фильмов и 🎬сериалов, а также мультфильмов!', parse_mode='HTML', reply_markup=await echoMark('Инструкция'))
    try:
        await message.delete()

        await message.answer('Главное меню', reply_markup=AfterCheckMenu.Keyboard)

    except Exception as ex:
        print(ex)

#--------------------- Films

@dispatcher.message_handler(commands=['film'])
async def film(message: types.Message):
    try:
        await message.delete()

        id = message.get_args()
        film = await getFilm(id)

        await message.answer_photo(photo=film.get('photo'), caption=await filmVideoCaption(film), reply_markup=await filmRedirectKeyboard(id), parse_mode='HTML')
    except Exception as ex:
        print(ex)

@dispatcher.callback_query_handler(ListFilmsCallback.filter())
async def listFilms(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get('num'))
    try:
        await query.message.edit_text('Список фильмов\n\nЧем выше в списке, тем раньше появился в боте', reply_markup=await filmsListKeyboard(page))
    except Exception as ex:
        print(ex)

@dispatcher.callback_query_handler(FContentCallback.filter())
async def preShowFCallback(query: types.CallbackQuery, callback_data: dict):
    await query.message.delete()
    id = callback_data.get('id')
    content = await getContent(id)
    await query.message.answer_photo(photo=content.get('photo'), caption=await filmCaption(content), parse_mode='HTML', reply_markup=await filmRedirectKeyboard(id))

@dispatcher.callback_query_handler(FilmRedirectCallBack.filter())
async def ShowFilmCallback(query: types.CallbackQuery, callback_data: dict):
    if not await checkMemberTF(query): return await subPostCheck(query)
    id = callback_data.get('movieId')
    film = await getFilm(id)
    video = InputMedia(type='video', media=film.get('video'))
    await query.message.edit_media(media=video)
    await query.message.edit_caption(caption=await filmCaption(film), parse_mode='HTML', reply_markup=Search.Keyboard)

@dispatcher.callback_query_handler(text = 'RandFilm')
async def randFilm(query: types.CallbackQuery):
    await query.message.delete()
    film = random.choice(await getFilms())
    await query.message.answer_photo(photo=film.get('photo'), caption=await filmCaption(film), parse_mode="HTML", reply_markup=await filmRedirectKeyboard(film.get('id')), protect_content=True)
    #return await menu(query.message)

#--------------------- Multfilms

@dispatcher.callback_query_handler(ListMultFilmsCallback.filter())
async def listFilms(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get('num'))
    try:
        await query.message.edit_text('Список мультфильмов\n\nЧем выше в списке, тем раньше появился в боте', reply_markup=await multFilmsListKeyboard(page))
    except Exception as ex:
        print(ex)

#--------------------- Series

@dispatcher.message_handler(commands=['series'])
async def series(message: types.Message):
    try:
        await message.delete()

        id = message.get_args()
        content = await getContent(id)

        await message.answer_photo(caption=await filmCaption(content), photo=content.get('photo'), reply_markup=await seriesSeasonsKeyboard(id), parse_mode='HTML')
    except Exception as ex:
        print(ex)

@dispatcher.callback_query_handler(ListSeriesCallback.filter())
async def listSeries(query: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get('num'))
    try:
        await query.message.edit_text('Список сериалов\n\nЧем выше в списке, тем раньше появился в боте', reply_markup=await SeriesListKeyboard(page))
    except Exception as ex:
        print(ex)

@dispatcher.callback_query_handler(SContentCallback.filter())
async def preShowSCallback(query: types.CallbackQuery, callback_data: dict):
    id = callback_data.get('id')
    page = int(callback_data.get('page'))
    season = callback_data.get('season')
    content = await getContent(id)
    if not season:
        if not query.message.photo: 
            await query.message.delete()
            await query.message.answer_photo(photo=content.get('photo'), caption=await filmCaption(content), parse_mode='HTML', reply_markup=await seriesSeasonsKeyboard(id, page))
        else: await query.message.edit_reply_markup(reply_markup=await seriesSeasonsKeyboard(id, page))
    else:
        season = int(season)
        await query.message.edit_reply_markup(reply_markup=await seriesSeriasKeyboard(id, season,page))

@dispatcher.callback_query_handler(SeriesRedirectCallback.filter())
async def ShowSeriaCallback(query: types.CallbackQuery, callback_data: dict):
    if not await checkMemberTF(query): return await subPostCheck(query)
    id = callback_data.get('movieId')
    seria = callback_data.get('seria')
    season = callback_data.get('season')
    content = await getContent(id)
    videoCont = await getSerialSeria(id,season, seria)
    video = InputMedia(type='video', media=videoCont.get('video'))
    await query.message.edit_media(media=video)
    await query.message.edit_caption(caption=await serisCaption(content, season, seria), parse_mode='HTML', reply_markup=Search.Keyboard)

#--------------------- Admin

@dispatcher.message_handler(isAdminFilter=True, commands=['admin'])
@dispatcher.callback_query_handler(text='adminMenu')
async def adminMenu(message: types.Message):
    try:
        await message.answer('Админ панель', reply_markup=AdminMenu.Keyboard)
    except:
        await message.message.edit_text('Админ панель', reply_markup=AdminMenu.Keyboard)

#--------------------- Admin / Channels

@dispatcher.callback_query_handler(text='ChannelsMenu')
async def ChannelsMenuF(query: types.CallbackQuery):
    try:
        await query.message.edit_text('Админ панель / Управление каналами', reply_markup=ChannelsMenu.Keyboard)
    except: await default(query.message)

@dispatcher.callback_query_handler(text='addNewChannnel')
async def addNewChannnel(query: types.CallbackQuery):
    try: await query.message.delete()
    except: pass
    await query.message.answer('Админ панель / Управление каналами / Добавить новый канал\n\nВведите через запятые:\nНазвание, id, Ссылка', reply_markup=Back2ChannelsMenuMark.Keyboard)

    await ChannelGroup.channel.set()
    #print(query.text)

@dispatcher.message_handler(state = ChannelGroup.channel)
async def addNewChannnelState(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        #await message.delete()
        return await adminMenu(message)
    try:
        addList = message.text.split(',')
        name, id, link = addList[0].strip(), addList[1].strip(), addList[2].strip()
        if await createChannel(telegram_id=id, link=link, name=name): raise Exception
        await message.answer('Успешно')
    except:
        await message.answer('Неверный формат')
    await state.finish()
    return await adminMenu(message)

@dispatcher.callback_query_handler(text='channelsList')
async def channelsList(query: types.CallbackQuery):
    #await query.message.delete()
    links = [hlink(can.get('name'), can.get('link')) for can in await getChannels()]
    links = [f'({i+1}) '+link for i, link in enumerate(links)]
    try:
        await query.message.edit_text('Админ панель / Управление каналами / Список каналов\n\n'+'\n'.join(links), parse_mode="HTML", reply_markup=Back2ChannelsMenu.Keyboard, disable_web_page_preview=True)
    except: await default(query.message)

@dispatcher.callback_query_handler(text='channelDelete')
async def channelDelete(query: types.CallbackQuery):
    await query.message.delete()
    links = [hlink(f"{can.get('telegram_id')} {can.get('name')}", can.get('link')) for can in await getChannels()]
    try:
        await query.message.answer('Админ панель / Управление каналами / Удалить канал\n\nНомер канала:\n'+'\n'.join(links), parse_mode="HTML", reply_markup=Back2ChannelsMenuMark.Keyboard)
    except Exception as ex: 
        print(ex)
        return await default(query.message)

    await ChannelGroup.channelDelete.set()

@dispatcher.message_handler(state = ChannelGroup.channelDelete)
async def channelDeleteState(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        return await adminMenu(message)
    try:
        channelId = int(message.text)
        await deleteChannel(channelId)
        await message.answer('Успешно')
    except:
        await message.answer('Неверный формат')

    await state.finish()
    return await adminMenu(message)

#--------------------- Admin / Films

@dispatcher.callback_query_handler(text='FilmsMenu')
async def FilmsMenuF(query: types.CallbackQuery):
    try:
        await query.message.edit_text('Админ панель / Управление фильмами', reply_markup=FilmsMenu.Keyboard)
    except: await default(query.message)

@dispatcher.callback_query_handler(text='filmsList')
async def filmsList(query: types.CallbackQuery):
    links = [film.get('name') for film in await getFilms()]
    links = [f'({i+1}) '+link for i, link in enumerate(links)]
    try:
        await query.message.edit_text('Админ панель / Управление фильмами / Список фильмов\n\n'+'\n'.join(links), parse_mode="HTML", reply_markup=Back2FilmsMenu.Keyboard)
    except: await default(query.message)

@dispatcher.callback_query_handler(text='multfilmsList')
async def multfilmsList(query: types.CallbackQuery):
    links = [film.get('name') for film in await getMultFilms()]
    links = [f'({i+1}) '+link for i, link in enumerate(links)]
    try:
        await query.message.edit_text('Админ панель / Управление фильмами / Список мультфильмов\n\n'+'\n'.join(links), parse_mode="HTML", reply_markup=Back2FilmsMenu.Keyboard)
    except: await default(query.message)

@dispatcher.callback_query_handler(text='filmDelete')
async def filmsDelete(query: types.CallbackQuery):
    await query.message.delete()
    links = [hlink(f"{can.get('id')} {can.get('name')}", can.get('link')) for can in await getFilms()]
    try:
        await query.message.answer('Админ панель / Управление фильмами / Удалить фильм\n\nНомер фильма:\n'+'\n'.join(links), parse_mode="HTML", reply_markup=Back2FilmsMenuMark.Keyboard)
    except Exception as ex: 
        print(ex)
        return await default(query.message)

    await FilmGroup.filmDelete.set()

@dispatcher.message_handler(state = FilmGroup.filmDelete)
async def filmDeleteState(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        return await adminMenu(message)
    try:
        filmlId = int(message.text)
        await deleteContent(filmlId)
        await message.answer('Успешно')
    except:
        await message.answer('Неверный формат')

    await state.finish()
    return await adminMenu(message)

@dispatcher.callback_query_handler(FilmMultCreate.filter())
async def addNewFilm(query: types.CallbackQuery, callback_data: dict):
    typeId = callback_data.get('typeid')
    try: await query.message.delete()
    except: pass
    addTypeName = 'фильм'
    if typeId == '2': 
        addTypeName = 'мультфильм'
    await query.message.answer(f'Админ панель / Управление фильмами / Добавить новый {addTypeName}\n\nПришлите id фильма на КиноПоиске или \nВведите, разделяя знаком "#" атрибуты:\n\nНазвание \n# Описание \n# Ссылка на фото', reply_markup=Back2FilmsMenuMark.Keyboard)
    state = dispatcher.get_current().current_state()
    await state.update_data(typeId=typeId)
    await FilmGroup.film.set()
    #print(query.text)

@dispatcher.message_handler(state = FilmGroup.film, content_types=['text', 'photo'])
async def addNewFilmState(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        #await message.delete()
        return await adminMenu(message)
    try:
        if '#' in message.text:
            addList = message.text.split('#')
            name,description, photo = addList[0].strip(), addList[1].strip(), addList[2].strip()
            #video = message.video.file_id
            film = dict(name=name, description=description, photo=photo)
        else:
            id = int(message.text)
            film = await getMovieById(id)
            if not film:
                await message.answer('Ошибка КиноПоиска.')
                await state.finish()
                return await adminMenu(message)
        await state.update_data(film=film)
        await message.answer('Загрузите или перешлите видео', reply_markup=Back2FilmsMenuMark.Keyboard)

        await FilmGroup.filmVideo.set()

    except:
        await message.answer('Неверный формат')
        await state.finish()
        return await adminMenu(message)

@dispatcher.message_handler(state = FilmGroup.filmVideo, content_types=['text', 'video'])
async def filmVideoState(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        #await message.delete()
        return await adminMenu(message)
    try:
        cur_state = await state.get_data()
        film = cur_state.get('film')
        film.update({'video' : message.video.file_id})
        await state.update_data(film=film)
    except:
        await message.answer('Неверный формат')
        await state.finish()
        return await adminMenu(message)

    await message.answer_photo(caption=('Всё верно?\n'+await filmCaption(film)), photo=film.get('photo'), parse_mode='HTML', reply_markup=YesNoMark.Keyboard)
    await FilmGroup.filmConfirm.set()
        
@dispatcher.message_handler(state = FilmGroup.filmConfirm)
async def confirmNewFilmState(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Да':
            cur_state = await state.get_data()
            film = cur_state.get('film')
            await createFilm(type=cur_state.get('typeId'), **film)
            await message.answer('Успешно')
    except Exception as ex:
        await message.answer('Неверный формат')
        print(ex)
    await state.finish()
    return await adminMenu(message)

#--------------------- Admin / Serials

@dispatcher.callback_query_handler(text='SerialsMenu')
async def SerialsMenuF(query: types.CallbackQuery):
    try:
        await query.message.edit_text('Админ панель / Управление сериалами', reply_markup=SeriesMenu.Keyboard)
    except: await default(query.message)

@dispatcher.callback_query_handler(text='addNewSerial')
async def SerialsMenuF(query: types.CallbackQuery):
    try: await query.message.delete()
    except: pass
    await query.message.answer('Админ панель / Управление сериалами / Добавить новый сериал\n\nПришлите id сериала на КиноПоиске или \nВведите, разделяя знаком "#" атрибуты:\n\nНазвание \n# Описание \n# Ссылка на фото', reply_markup=Back2SerialsMenuMark.Keyboard)

    await SeriesGroup.series.set()

@dispatcher.message_handler(state = SeriesGroup.series, content_types=['text', 'photo'])
async def addNewSeriesState(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        #await message.delete()
        return await adminMenu(message)
    try:
        if '#' in message.text:
            addList = message.text.split('#')
            name,description, photo = addList[0].strip(), addList[1].strip(), addList[2].strip()
            #video = message.video.file_id
            series = dict(name=name, description=description, photo=photo)
        else:
            id = int(message.text)
            series = await getMovieById(id)
            if not series:
                await message.answer('Ошибка КиноПоиска.')
                await state.finish()
                return await adminMenu(message)
        await state.update_data(series=series)
        await message.answer_photo(caption=('Всё верно?\n'+await filmCaption(series)), photo=series.get('photo'), parse_mode='HTML', reply_markup=YesNoMark.Keyboard)

        await SeriesGroup.seriesConfirm.set()

    except Exception as ex:
        print(ex)
        await message.answer('Неверный формат')
        await state.finish()
        return await adminMenu(message)

@dispatcher.message_handler(state = SeriesGroup.seriesConfirm)
async def confirmNewSeriesState(message: types.Message, state: FSMContext):
    try:
        if message.text == 'Да':
            cur_state = await state.get_data()
            series = cur_state.get('series')
            result = await createSerial(**series)
            if not result:
                await message.answer('Успешно')
            else:
                await message.answer('Произошла какая-то проблема')
    except:
        await message.answer('Неверный формат')
    await state.finish()
    return await adminMenu(message)

@dispatcher.callback_query_handler(text='serialsList')
async def serialsList(query: types.CallbackQuery):
    links = [series.get('name') for series in await getSerials()]
    links = [f'({i+1}) '+link for i, link in enumerate(links)]
    try:
        await query.message.edit_text('Админ панель / Управление сериалами / Список сериалов\n\n'+'\n'.join(links), parse_mode="HTML", reply_markup=Back2SerialsMenu.Keyboard)
    except: await default(query.message)

@dispatcher.callback_query_handler(text='serialDelete')
async def serialDelete(query: types.CallbackQuery):
    await query.message.delete()
    links = [f"{series.get('id')} {series.get('name')}" for series in await getSerials()]
    try:
        await query.message.answer('Админ панель / Управление сериалами / Удалить сериал\n\nНомер сериала:\n'+'\n'.join(links), parse_mode="HTML", reply_markup=Back2SerialsMenuMark.Keyboard)
    except Exception as ex: 
        print(ex)
        return await default(query.message)

    await SeriesGroup.seriesDelete.set()

@dispatcher.message_handler(state = SeriesGroup.seriesDelete)
async def serialDeleteS(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        return await adminMenu(message)
    try:
        serieslId = int(message.text)
        await deleteContent(serieslId)
        await message.answer('Успешно')
    except:
        await message.answer('Неверный формат')

    await state.finish()
    return await adminMenu(message)

@dispatcher.callback_query_handler(text='addNewSeria')
async def addNewSeria(query: types.CallbackQuery):
    await query.message.delete()
    await query.message.answer('Введите следующие атрибуты через пробелы:\n{id сериала} {Номер сезона} {Номер серии}', reply_markup=Back2SerialsMenuMark.Keyboard)
    await SeriesGroup.newSeria.set()

@dispatcher.message_handler(state = SeriesGroup.newSeria)
async def addNewSeriaS(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        return await adminMenu(message)
    try:
        content_id, season, series = message.text.split()
        serial = await getContent(content_id)
        if serial.get('type') != 1 or await getSerialSeria(content_id, season, series):
            await message.answer('Неверный id сериала или такая серия уже существует')
            await state.finish()
            return await adminMenu(message)
        name = serial.get('name')
        await state.update_data(seria=dict(season=season,series=series,content_id=content_id))
        await message.answer(f'Отправте видео или перешлите сообщение с видео\nСериал: {name}\nСезон: {season}\nСерия: {series}', reply_markup=Back2SerialsMenuMark.Keyboard)
    except:
        await message.answer('Неверный формат')
        await state.finish()
        return await adminMenu(message)
    await SeriesGroup.newSeriaVideo.set()

@dispatcher.message_handler(state = SeriesGroup.newSeriaVideo, content_types=['text', 'video'])
async def newSeriaVideoS(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        return await adminMenu(message)
    try:
        state_ = await state.get_data()
        seria = state_.get('seria')
        seria.update({'video' : message.video.file_id})
        result = await addSeries(**seria)
        if not result:
            await message.answer('Успешно')
    except:
        await message.answer('Неверный формат')
    await state.finish()
    return await adminMenu(message)

@dispatcher.callback_query_handler(text='seriaDelete')
async def seriaDelete(query: types.CallbackQuery):
    await query.message.delete()
    await query.message.answer('Удаление серии\nВведите следующие атрибуты через пробелы:\n{id сериала} {Номер сезона} {Номер серии}', reply_markup=Back2SerialsMenuMark.Keyboard)
    await SeriesGroup.deleteSeria.set()

@dispatcher.message_handler(state = SeriesGroup.deleteSeria)
async def newSeriaVideoS(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        return await adminMenu(message)
    try:
        content_id, season, series = message.text.split()
        if await deleteSeria(content_id, season, series):
            await message.answer('Успешно')
        else:
            raise Exception
    except:
        await message.answer('Что-то пошло не так...')
    await state.finish()
    return await adminMenu(message)

#--------------------- Admin / Statistic

@dispatcher.callback_query_handler(text='StaticMenu')
async def StaticMenu(query: types.CallbackQuery):
    try:
        await query.message.edit_text('Админ панель / Статистика\n\n'+ await adminStatic(), reply_markup=StatisticMenu.Keyboard, parse_mode='HTML')
    except Exception as ex: 
        print(ex)
        await default(query.message)

@dispatcher.callback_query_handler(text='changeStatic')
async def changeStatic(query: types.CallbackQuery):
    try:
        await query.message.delete()
        await query.message.answer('Админ панель / Статистика\n\nВведите через пробел добавочные КП и КПМ\n\n'+ await adminStatic(), reply_markup=Back2StatickMenuMark.Keyboard, parse_mode='HTML')
        await StaticGroup.fakeStatic.set()
    except Exception as ex: 
        print(ex)
        await default(query.message)

@dispatcher.message_handler(state = StaticGroup.fakeStatic)
async def newSeriaVideoS(message: types.Message, state: FSMContext):
    global ADD_USER_COUNT, ADD_MOVIE_PRESSED_COUNT
    if message.text == 'Отмена': 
        await state.finish()
        return await adminMenu(message)
    try:
        fakeUserCount, fakeMoviePressedCount = message.text.split()

        ADD_USER_COUNT = int(fakeUserCount)
        ADD_MOVIE_PRESSED_COUNT = int(fakeMoviePressedCount)
    except:
        await message.answer('Что-то пошло не так...')
    await message.answer('Успешно')
    await state.finish()
    return await adminMenu(message)

#--------------------- Admin / Publish

@dispatcher.callback_query_handler(text='mailMenu')
async def mailMenu(query: types.CallbackQuery):
    try:
        await query.message.edit_text('Админ панель / Рассылка', reply_markup=MailMenu.Keyboard)
    except Exception as ex: 
        print(ex)
        await default(query.message)

@dispatcher.callback_query_handler(text='newMail')
async def mailNew(query: types.CallbackQuery):
    try:
        await query.message.delete()
        await query.message.answer('Админ панель / Рассылка\n\nВведите текст рассылки. Можете прикреплять фотографию.', reply_markup=Back2MailMenuMark.Keyboard)
        await MailGroup.mail.set()
    except Exception as ex: 
        print(ex)
        await default(query.message)

@dispatcher.message_handler(state = MailGroup.mail, content_types=['photo','text'])
async def newMailS(message: types.Message, state: FSMContext):
    if message.text == 'Отмена': 
        await state.finish()
        return await adminMenu(message)
    try:
        if message.photo:
            await state.update_data(text=message.caption, photo=message.photo[0].file_id)
            await message.answer_photo(caption='Всё верно?\n\n'+message.caption, photo=message.photo[0].file_id, reply_markup=YesNoMark.Keyboard)
        else:
            await state.update_data(text=message.text)
            await message.answer(text='Всё верно?\n\n'+message.text, reply_markup=YesNoMark.Keyboard)
    except Exception as ex:
        #print('newMailS', ex)
        await message.answer('Что-то пошло не так...')
        await state.finish()
        return await adminMenu(message)
    await MailGroup.mailConfirm.set()

@dispatcher.message_handler(state = MailGroup.mailConfirm)
async def confirmMailS(message: types.Message, state: FSMContext):
    if message.text == 'Да':      
        try:
            cur_state = await state.get_data()
            await sendMail(cur_state)
            await message.answer('Успешно')
        except:
            await message.answer('Что-то пошло не так...')
    else:
        await message.answer('Отмена')
    await state.finish()
    await adminMenu(message)
    

#---------------------

@dispatcher.message_handler(content_types=['photo','text','sticker', 'video'])
async def default(message: types.Message):
    #if not message.from_user.is_bot and not message.via_bot:
    if message.text == 'Инструкция':
        await message.answer(INSTRUCTION, parse_mode='HTML', reply_markup=Search.Keyboard)
    else:
        await message.answer('🔌⚙️ Попробуйте: /start')
        #print(bot.get_me)
        #await message.answer_video('BAACAgIAAxkBAAIB-GObRrIAAX1gg2GiF-HLP78823H1jwACWSAAAoue4UjhL6TRsitj0SwE', caption='Видео')

#---------------------

@dispatcher.inline_handler()
async def inlineFilmSearch(query: InlineQuery):
    text = query.query or None
    items = []
    content = await getContentInlineQuery()
    if not text:
        for id, name, description, photo, type in content:
            if len(items) > INLINE_RESULT_LIMIT: break
            command = '/series '
            type_text = 'Сериал |'
            if type in (0,2):
                command = '/film '
                type_text = 'Фильм |'
                if type == 2: type_text = 'Мультфильм |'

            items.append(InlineQueryResultArticle(
                    id = id,
                    input_message_content = InputTextMessageContent(command+str(id)),
                    title = name,
                    description = type_text + description,
                    thumb_url = photo,
                    #reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Введите /movie {id}', url='https://t.me/KinolamaBot'))
                ))
    else:
        for id, name, description, photo, type in content:
            if len(items) > INLINE_RESULT_LIMIT: break
            if text.lower().strip() in name.lower():
                command = '/series '
                type_text = 'Сериал |'
                if type in (0,2):
                    command = '/film '
                    type_text = 'Фильм |'
                    if type == 2: type_text = 'Мультфильм |'
                items.append(InlineQueryResultArticle(
                        id = id,
                        input_message_content = InputTextMessageContent(command+str(id)),
                        title = name,
                        description = type_text + description,
                        thumb_url = photo,
                        #reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Введите /movie {id}', url='https://t.me/KinolamaBot'))
                    ))
    
    if not items:
        items = [InlineQueryResultArticle(
                        id = 'None',
                        input_message_content = InputTextMessageContent('Инструкция'),
                        title = 'Не смогли ничего найти(',
                        description = 'Попроверьте правильность ввода.',
                    )]

    return await query.answer(items, switch_pm_text='Меню', switch_pm_parameter='search')

async def sendMail(mail: dict):
    maxUserCount = await getMaxUsersId()
    text = mail.get('text')
    photo = mail.get('photo')
    for id in range(1, maxUserCount+1):
        telegram_id = (await getUserById(id)).get('telegram_id')
        try:
            if photo: await bot.send_photo(chat_id=telegram_id, photo=photo, caption=text, parse_mode='HTML')
            else: await bot.send_message(chat_id=telegram_id, text=text, parse_mode='HTML')
        except Exception as ex: pass #print(ex)
        await sleep(0.5)

if __name__ == '__main__':
	executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)