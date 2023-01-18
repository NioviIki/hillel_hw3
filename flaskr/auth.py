from . import db
from flask import Blueprint, render_template, request, current_app
import requests as requests
from faker import Faker

bp = Blueprint('auth', __name__)

@bp.route("/names/")
def names():
    count=db.con().execute("SELECT COUNT(DISTINCT(artist)) FROM tracks")
    artist=db.con().execute("SELECT DISTINCT(artist) FROM tracks")
    return render_template('auth/to_names.html', count=count, artist=artist)

@bp.route('/tracks/')
def tracks():
    count = db.con().execute("SELECT COUNT(DISTINCT(title)) FROM tracks")
    data = db.con().execute("SELECT DISTINCT(title) FROM tracks")
    return render_template('auth/to_tracks.html', data=data, count=count)

@bp.route("/tracks/<genres>/")
def genres(genres):
    output = "tracks.artist, tracks.title, tracks.length"
    count = db.con().execute(f"SELECT COUNT(*) FROM tracks JOIN all_genre ON tracks.genre_id = all_genre.id WHERE all_genre.genre='{genres}'")
    tracks = db.con().execute(f"SELECT {output} FROM tracks JOIN all_genre ON tracks.genre_id = all_genre.id WHERE all_genre.genre='{genres}'")
    return render_template('auth/to_genres.html', genre=genres, tracks=tracks, count=count)

@bp.route("/tracks-sec/")
def tracks_sec():
    name_length = db.con().execute("SELECT title, strftime('%H', length)* 3600 + strftime('%M', length)*60 + strftime('%S', length) FROM tracks")
    return render_template('auth/to_tracks-sec.html', name_length=name_length)

@bp.route('/tracks-sec/statistics/')
def tracks_sec_statistics():
    avg = db.con().execute("SELECT (SUM(strftime('%M', length))*60 + SUM(strftime('%S', length))) / MAX(id) FROM tracks")
    sum_of_tracks = db.con().execute("SELECT (SUM (strftime('%H', length))* 3600 + SUM(strftime('%M', length))*60 + SUM(strftime('%S', length))) FROM tracks")
    return render_template('auth/to_tracks_sec_statistics.html', avg=avg, sum=sum_of_tracks)

@bp.route('/space/')
def space():
    lsit_of_dict = requests.get('http://api.open-notify.org/astros.json').json()["people"]
    return render_template('auth/to_space.html', name_craft=lsit_of_dict, count=len(lsit_of_dict))

@bp.route("/mean/")
def mean():
    with current_app.open_resource("other/hw.csv", "r") as r:
        Weight, Height = 0, 0
        for count, lines in enumerate(r.readlines()):
            number = lines.splitlines()[0].split(",")
            if len(number) > 1 and "Index" not in lines:
                Height += float(number[1])
                Weight += float(number[2])
    return render_template('auth/to_mean.html',
                           Average_weight=round(Weight * 0.453592 / count),
                           Average_growth=round(Height * 2.54 / count)
                           )

@bp.route("/generate-users/", methods=["GET"])
def genetate():
    count = request.args.get('count', 100)
    fake = Faker()
    list_of_fake = [[fake.first_name(), fake.email()] for _ in range(int(count))]
    return render_template('auth/to_generate-users.html', list=list_of_fake)

@bp.route("/requirements/")
def requirements():
    with current_app.open_resource("other/requirements.txt", "r") as r:
        return render_template('auth/to_requirements.html', list_of_requirements=r.read().split())
