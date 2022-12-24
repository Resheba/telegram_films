from aiogram.dispatcher.filters.state import StatesGroup, State

class ChannelGroup(StatesGroup):
    channel = State()
    channelDelete = State()

class FilmGroup(StatesGroup):
    film = State()
    filmVideo = State()
    filmConfirm = State()
    filmDelete = State()

class SeriesGroup(StatesGroup):
    series = State()
    seriesConfirm = State()
    seriesDelete = State()

    newSeria = State()
    newSeriaVideo = State()

    deleteSeria = State()

class StaticGroup(StatesGroup):
    fakeStatic = State()

class MailGroup(StatesGroup):
    mail = State()
    mailConfirm = State()