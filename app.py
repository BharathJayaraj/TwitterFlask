from config import Config
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from datetime import datetime
from db_utils import (
    search_tweets,
    get_tweets_of_user,
    get_column_for_row,
    filter_tweets,
    update_last_pulled_time_for_user,
    initialize_user,
    update_tweets_pulled_for_user,
    write_tweets_to_db,
    update_is_completed_status
)
from forms import FilterForm, SearchForm
from twitter_utils import get_timeline_for_user
from logger import exc


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.config.from_object(Config)
twitter_bp = make_twitter_blueprint()
app.register_blueprint(twitter_bp, url_prefix="/login")
OAUTHLIB_INSECURE_TRANSPORT = True


@app.route("/", methods=['GET', 'POST'])
def login():
    try:
        if not twitter.authorized:
            return redirect(url_for("twitter.login"))
        resp = twitter.get("account/verify_credentials.json")
        assert resp.ok
        twitter_username = resp.json()["screen_name"]
        pull_tweets_of_user(twitter_username)
        form = SearchForm()
        if form.validate_on_submit():
            search_terms = form.search.data
            tweets = search_tweets(search_terms, twitter_username)
        else:
            tweets = get_tweets_of_user(twitter_username)

        context = {
            "username": twitter_username,
            "tweets_pulled": get_column_for_row("tweets_pulled", "users", "username", twitter_username),
            "last_updated_at": get_column_for_row("last_pulled_at", "users", "username", twitter_username)
        }
        return render_template('index.html', context=context, form=form, tweets=tweets)
    except Exception as err:
        exc.exception("Exception occurred in app login function. Error:{}".format(err))
        print("Exception occurred in app login function.", err)


@app.route("/filter", methods=['GET', 'POST'])
def filter():
    try:
        if not twitter.authorized:
            return redirect(url_for("twitter.login"))
        resp = twitter.get("account/verify_credentials.json")
        assert resp.ok
        twitter_username = resp.json()["screen_name"]

        form = FilterForm()
        if form.validate_on_submit():
            start_date = form.startdate.data
            end_date = form.enddate.data
            chronological = form.chronological.data
            tweets = filter_tweets(
                start_date, end_date, chronological, twitter_username
            )
        else:
            tweets = get_tweets_of_user(twitter_username)

        context = {
            "username": twitter_username
        }
        return render_template('filter.html', context=context, form=form, tweets=tweets)
    except Exception as err:
        exc.exception("Exception occurred in app filter function.. Error:{}".format(err))
        print("Exception occurred in app filter function.", err)


def pull_tweets_of_user(username):
    try:
        user_id = get_column_for_row("id", "users", "username", username)
        last_pulled_at = get_column_for_row("last_pulled_at", "users", "username", username)
        if user_id:
            update_last_pulled_time_for_user(username, datetime.now())
        else:
            initialize_user(username, datetime.now())
        timeline, count = get_timeline_for_user(username, last_pulled_at)
        write_tweets_to_db(timeline, username)
        update_tweets_pulled_for_user(username, count)
        update_is_completed_status(username)
    except Exception as err:
        exc.exception("Exception occurred in app pull tweets function. Error:{}".format(err))
        print("Exception occurred in app pull tweets function.", err)


def pull_new_tweets_of_users():
    try:
        users = []
        for user in users:
            pull_tweets_of_user(user)
    except Exception as err:
        exc.exception("Exception occurred in app pull new tweets function. Error:{}".format(err))
        print("Exception occurred in app pull new tweets function.", err)


if __name__ == "__main__":
    try:
        app.run(debug=False)
    except Exception as e:
        exc.exception("Exception occurred in app execution. Error:{}".format(e))
        print("Exception occurred in app run.", e)
