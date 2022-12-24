import sqlite3 as sq
import asyncio, os, datetime

async def db_start():
    global db, cur
    db = sq.connect('data.db')
    db.row_factory = sq.Row
    cur = db.cursor()
    cur.execute('PRAGMA foreign_keys = ON')
    # try:
    #     cur.execute("CREATE TABLE film(id INTEGER PRIMARY KEY, name NOT NULL, description NOT NULL, photo NOT NULL, video NOT NULL)")
    #     cur.execute("CREATE TABLE channel(telegram_id INTEGER PRIMARY KEY, link NOT NULL, name NOT NULL)")
    # except: pass

async def getFilms():
    try:
        FILMS = cur.execute("SELECT content.id, name, description, photo, video FROM content INNER JOIN film ON content.id = content_id WHERE type = 0;").fetchall()
        FILMS = [dict(film) for film in FILMS]
        return FILMS
    except Exception as ex:
        print('getFilms', ex)

async def getMultFilms():
    try:
        FILMS = cur.execute("SELECT content.id, name, description, photo, video FROM content INNER JOIN film ON content.id = content_id WHERE type = 2;").fetchall()
        FILMS = [dict(film) for film in FILMS]
        return FILMS
    except Exception as ex:
        print('getMultFilms', ex)

async def getFilm(id):
    try:
        FILM = cur.execute("SELECT content.id, name, description, photo, video FROM content INNER JOIN film ON content.id = content_id WHERE content.id = {content_id};".format(content_id=id)).fetchone()
        FILM = dict(FILM)
        return FILM
    except Exception as ex:
        print('getFilm', ex)

async def getFilmsIds():
    try:
        FILMS = cur.execute("SELECT id, name FROM content WHERE type = 0;").fetchall()
        FILMS = [tuple(film) for film in FILMS]
        return FILMS
    except Exception as ex:
        print('getFilmsIds', ex)

async def getSeriesIds():
    try:
        SERIES = cur.execute("SELECT id, name FROM content WHERE type = 1;").fetchall()
        SERIES = [tuple(series) for series in SERIES]
        return SERIES
    except Exception as ex:
        print('getSeriesIds', ex)

async def getMultFilmsIds():
    try:
        FILMS = cur.execute("SELECT id, name FROM content WHERE type = 2;").fetchall()
        FILMS = [tuple(film) for film in FILMS]
        return FILMS
    except Exception as ex:
        print('getMultFilmsIds', ex)

async def getContent(id):
    try:
        CONTENT = cur.execute("SELECT id, name, description, photo, type FROM content WHERE id = {id}".format(id=id)).fetchone()
        CONTENT = dict(CONTENT)
        return CONTENT
    except Exception as ex:
        print('getContent', ex)

async def getChannels():
    try:
        CHANNELS = cur.execute("SELECT * FROM channel").fetchall()
        CHANNELS = [dict(film) for film in CHANNELS]
        return CHANNELS
    except Exception as ex:
        print('getChannels', ex)

async def getSerialSeries(id):
    try:
        SERIAS = cur.execute("SELECT season, series FROM serial WHERE content_id = {id};".format(id=id)).fetchall()
        SERIAS = [tuple(SERIA) for SERIA in SERIAS]
        return SERIAS
    except Exception as ex:
        print('getSerialSeries', ex)
        return 0

async def getSerialSeria(id, season, series):
    try:
        SERIAL = cur.execute("SELECT * FROM serial WHERE content_id = {id} and season = {season} and series = {series};".format(id=id, season=season, series=series)).fetchone()
        SERIAL = dict(SERIAL)
        return SERIAL
    except Exception as ex:
        #print('getSerialSeria', ex)
        return 0

async def deleteSeria(content_id, season, series):
    try:
        cur.execute("DELETE FROM serial WHERE content_id = {content_id} and season = {season} and series = {series};".format(content_id=content_id, season=season, series=series)).fetchone()
        db.commit()
        return 1
    except Exception as ex:
        print('deleteSeria', ex)
        return 0

async def getSerials():
    try:
        SERIALS = cur.execute("SELECT id, name, description, photo FROM content WHERE type = 1;").fetchall()
        SERIALS = [dict(serial) for serial in SERIALS]
        return SERIALS
    except Exception as ex:
        print('getSerials', ex)

async def deleteContent(id):
    try:
        cur.execute("DELETE FROM content WHERE id='{id}'".format(id=id))
        db.commit()
        return 0
    except Exception as ex:
        print('deleteFilm', ex)

async def deleteChannel(telegram_id):
    try:
        cur.execute("DELETE FROM channel WHERE telegram_id='{telegram_id}'".format(telegram_id=telegram_id))
        db.commit()
        return 0
    except Exception as ex:
        print('deleteChannel', ex)

async def createFilm(name, description, photo, video, id = None, genres = None, type = 0):
    try:
        cur.execute("INSERT INTO content VALUES(?,?,?,?,?)", (id, name, description, photo, type))
        content_id = cur.lastrowid
        cur.execute("INSERT INTO film VALUES(?,?,?)", (id, video, content_id))
        if genres:
            for genre in genres:
                cur.execute("INSERT INTO genres VALUES(?,?,?)", (id, genre, content_id))
        db.commit()
        return 0
    except Exception as ex:
        print('createFilm', ex)

async def createSerial(name, description, photo, id = None, genres = None):
    try:
        cur.execute("INSERT INTO content VALUES(?,?,?,?,?)", (id, name, description, photo, 1))
        content_id = cur.lastrowid
        if genres:
            for genre in genres:
                cur.execute("INSERT INTO genres VALUES(?,?,?)", (id, genre, content_id))
        db.commit()
        return 0
    except Exception as ex:
        print('createSerial', ex)
        return -1

async def addSeries(season, series, video, content_id, id = None):
    try:
        cur.execute("INSERT INTO serial VALUES(?,?,?,?,?)", (id, season, series, video, content_id))
        db.commit()
        return 0
    except Exception as ex:
        print('addSeries', ex)
        return -1

async def createChannel(telegram_id, link, name):
    try:
        cur.execute("INSERT INTO channel VALUES(?,?,?)", (telegram_id, link, name))
        db.commit()
        return 0
    except Exception as ex:
        print('createChannel', ex)
        return -1

async def getContentInlineQuery():
    try:
        FILMS = cur.execute("SELECT id, name, description, photo, type FROM content").fetchall()
        FILMS = [tuple(film) for film in FILMS]
        return FILMS
    except Exception as ex:
        print('getFilmInlineQuery', ex)

async def getGenresInlineQuery():
    try:
        Genres = cur.execute("SELECT genre, content_id FROM genres;").fetchall()
        Genres = [tuple(genre) for genre in Genres]
        return Genres
    except Exception as ex:
        print('getGenresInlineQuery', ex)

async def getMaxUsersId():
    try:
        MAX = cur.execute("SELECT MAX(id) FROM users;").fetchone()
        MAX = tuple(MAX)[0]
        return MAX
    except Exception as ex:
        print('getMaxUsersId', ex)

#---------------- Statistic

async def createUser(telegram_id):
    try:
        join_date = datetime.datetime.now()
        cur.execute("INSERT INTO users VALUES(?,?,?)", (telegram_id, join_date, None))
        db.commit()
    except Exception as ex:
        print('createUser', ex)

async def getUser(telegram_id):
    try:
        user = cur.execute("SELECT * FROM users WHERE telegram_id = {telegram_id};".format(telegram_id=telegram_id)).fetchone()
        if user: user = dict(user)
        return user
    except Exception as ex:
        print('getUser', ex)

async def getUserById(id):
    try:
        user = cur.execute("SELECT * FROM users WHERE id = {id};".format(id=id)).fetchone()
        if user: user = dict(user)
        return user
    except Exception as ex:
        print('getUserById', ex)

async def getUserCount():
    try:
        count = cur.execute("SELECT count() FROM users;").fetchone()
        count = tuple(count)[0]
        return count
    except Exception as ex:
        print('getUsersCount', ex)

async def getMoviesCheckedCount():
    try:
        count = cur.execute("SELECT count FROM statistic WHERE id = 1;").fetchone()
        count = tuple(count)[0]
        return count
    except Exception as ex:
        print('getMoviesCheckedCount', ex)

async def updateMoviesCheckedCount(plus = 1):
    try:
        count =  await getMoviesCheckedCount()
        cur.execute(f"UPDATE statistic SET count = {count + plus} WHERE id = 1;").fetchone()
        db.commit()
        return 0
    except Exception as ex:
        print('updateMoviesCheckedCount', ex)

# asyncio.run(db_start())
# asyncio.run(updateMoviesCheckedCount())