from plexapi.server import PlexServer
from plexapi.playlist import Playlist
from neo4j_helper import Database
from dotenv import load_dotenv
import os, sys, requests

def connect_plex():
    baseurl = os.environ['PLEX_URL']
    token = os.environ['PLEX_TOKEN']

    plex = PlexServer(baseurl, token)

    return plex

def connect_db():
    db = Database(os.environ['DATABASE_URL'], os.environ['DATABASE_USERNAME'], os.environ['DATABASE_PASSWORD'])

    return db

def recommend():
    plex = connect_plex()
    db = connect_db()

    accounts = plex.systemAccounts()
    
    accounts[0].id = plex.myPlexAccount().id

    for user in accounts:
        print(f"Creating playlist for: {user.name}")

        results = db.get_movie_for_user(str(user.id))
        user_playlist = find_user_playlist(user, plex, results)

        if user_playlist == None:
            continue
    
        for data in results:
            user_playlist.addItems(plex.library.section("Movies").getGuid(data['m2']['guid']))

        print(f"Playlist successfully created for: {user.name}")
        if (user.name != plex.myPlexAccount().username):
            user_playlist.copyToUser(str(user.id))
            continue

def find_user_playlist(user, plex, results):
    user_playlist = None

    if any(playlist.title == f"Recommended Movies for {user.name}" for playlist in plex.playlists()):
        user_playlist = plex.playlist(f"Recommended Movies for {user.name}")

        user_playlist.removeItems(user_playlist.items())
    elif len(results) != 0:
        user_playlist = Playlist.create(plex, f"Recommended Movies for {user.name}", plex.library.section("Movies"), plex.library.section("Movies").getGuid(results[0]['m2']['guid']))

    return user_playlist

def add_users_watched():
    print("Adding User Watched")
    plex = connect_plex()
    db = connect_db()

    accounts = plex.systemAccounts()
    
    accounts[0].id = plex.myPlexAccount().id

    for user in accounts:
        id = str(user.id)

        db.create_new_user(id, user.name)

        user_history = get_history(id, 1000)

        for item in user_history["data"]:
            if (item["media_type"] == "movie"):
                db.connect_user_and_movie(id, item["title"], item['guid'])

def add_movies(num):
    print("Adding Movies")
    db = connect_db()

    for content in get_recently_added(num):
        if content["library_name"] == "Movies":
            rating = 0
            audience_rating = 0

            if (content["rating"] != ''):
                rating = float(content["rating"])
            if (content["audience_rating"] != ''):
                audience_rating = float(content["audience_rating"])
            db.create_new_movie(content["title"], rating, audience_rating, content['guid'])

            for genre in content["genres"]:
                db.create_new_genre(genre)
                db.connect_movie_and_genre(genre, content['title'], content['guid'])

            db.create_new_content_rating(content['content_rating'])
            db.connect_movie_and_content_rating(content['content_rating'], content['title'], content['guid'])

# Tautulli Functions
def get_history(id, length):
    response = requests.get(f"{os.environ['TAUTULLI_URL']}/api/v2?apikey={os.environ['TAUTULLI_API_KEY']}&cmd=get_history&length={str(length)}&user_id={id}")

    return response.json()["response"]["data"]

def get_recently_added(count):
    response = requests.get(f"{os.environ['TAUTULLI_URL']}/api/v2?apikey={os.environ['TAUTULLI_API_KEY']}&cmd=get_recently_added&count={str(count)}")

    return response.json()["response"]["data"]["recently_added"]


if __name__ == "__main__":
    load_dotenv()

    # none: add content and run recommend
    # -r: run recommendation
    # -a: add content to dbms

    if len(sys.argv) == 1:
        add_movies(1500)
        add_users_watched()
        recommend()
    elif (sys.argv[1] == "-r"):
        recommend()
    elif (sys.argv[1] == "-a"):
        add_movies(1500)
        add_users_watched()