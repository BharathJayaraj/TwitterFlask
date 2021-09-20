from sqlalchemy import create_engine
from sqlalchemy.sql import text
from logger import exc
import config

engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)


def get_column_for_row(column_name, table_name, filter_column, value):
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT {} FROM {} WHERE {} = '{}'".format(
                    column_name, table_name, filter_column, value
                )))
            row = result.fetchone()
        return row[column_name] if row else None
    except Exception as err:
        exc.exception("Exception occurred in db utils get column for row function. Error:{}".format(err))
        print("Exception occurred in db utils get column for row function.", err)


def update_last_pulled_time_for_user(username, timestamp):
    try:
        data = {"timestamp": timestamp, "username": username}
        query = text("UPDATE users SET last_pulled_at=:timestamp WHERE username = :username")
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as err:
        exc.exception("Exception occurred in db utils last update pulled time function. Error:{}".format(err))
        print("Exception occurred in db utils last update pulled time function.", err)


def write_tweets_to_db(tweets, username):
    try:
        user_id = get_column_for_row("id", "users", "username", username)
        query = text("INSERT IGNORE INTO tweets (tweet_id, tweet_text, created_at, twitter_user)"
                     " VALUES (:id, :tweet, :created_at, :twitter_user)")
        with engine.connect() as connection:
            for tweet in tweets:
                tweet.update({"twitter_user": user_id})
                connection.execute(query, **tweet)
    except Exception as err:
        exc.exception(
            "Exception occurred in db utils fetch tweets from twitter to database function. Error:{}".format(err))
        print("Exception occurred in db utils fetch tweets from twitter to database function.", err)


def initialize_user(username, timestamp):
    try:
        query = text("INSERT INTO users (username, last_pulled_at) VALUES (:username, :now)")
        data = {"username": username, "now": timestamp}
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as err:
        exc.exception("Exception occurred in db utils user initialize row function. Error:{}".format(err))
        print("Exception occurred in db utils user initialize row function.", err)


def update_tweets_pulled_for_user(username, count):
    try:
        current_tweets_pulled = get_column_for_row("tweets_pulled", "users", "username", username)
        data = {
            "count": current_tweets_pulled + count,
            "username": username,
        }
        query = text("UPDATE users SET tweets_pulled=:count WHERE username = :username")
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as err:
        exc.exception("Exception occurred in db utils pulled update tweets function. Error:{}".format(err))
        print("Exception occurred in db utils pulled update tweets function.", err)


def update_is_completed_status(username, status=True):
    try:
        data = {
            "status": status,
            "username": username,
        }
        query = text("UPDATE users SET is_completed=:status WHERE username = :username")
        with engine.connect() as connection:
            connection.execute(query, **data)
    except Exception as err:
        exc.exception("Exception occurred in db utils update completion function. Error:{}".format(err))
        print("Exception occurred in db utils update completion function.", err)


def search_tweets(search_term, username):
    try:
        if not search_term:
            return []
        user_id = get_column_for_row("id", "users", "username", username)
        results = []
        search_term = ' & '.join(search_term.split())
        try:
            query = """
            WITH user_tweets AS (SELECT tweet_text, tweet_tsv, created_at FROM tweets WHERE twitter_user = {})
            SELECT tweet_text, created_at FROM user_tweets
            WHERE tweet_text LIKE %s""".format(user_id)

            value = f'%{search_term}%'
            with engine.connect() as connection:
                rows = connection.execute(query, value)
        except Exception as err:
            exc.exception("Exception occurred in search tweets query function. Error:{}".format(err))
        for row in rows:
            results.append({
                "tweet": row["tweet_text"],
                "created_at": row["created_at"]
            })
        return results
    except Exception as err:
        exc.exception("Exception occurred in db utils search tweets from database function. Error:{}".format(err))
        print("Exception occurred in db utils search tweets from database function.", err)


def get_tweets_of_user(username):
    try:
        user_id = get_column_for_row("id", "users", "username", username)
        results = []
        try:
            query = "SELECT tweet_id, tweet_text, created_at FROM tweets WHERE twitter_user = {}".format(user_id)
            with engine.connect() as connection:
                rows = connection.execute(query)
        except Exception as err:
            exc.exception("Exception occurred in get user tweets query function. Error:{}".format(err))
        for row in rows:
            results.append({
                "id": row["tweet_id"],
                "tweet": row["tweet_text"],
                "created_at": row["created_at"]
            })
        return results
    except Exception as err:
        exc.exception("Exception occurred in db utils get user tweets function. Error:{}".format(err))
        print("Exception occurred in db utils get user tweets function.", err)


def filter_tweets(start_date, end_date, chronological, username):
    results = []
    try:
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "user_id": get_column_for_row("id", "users", "username", username)
        }
        try:
            query = """WITH user_tweets AS (SELECT tweet_text, created_at FROM tweets WHERE twitter_user = :user_id)
            SELECT tweet_text, created_at FROM user_tweets
            WHERE created_at BETWEEN :start_date and DATE_ADD(:end_date,INTERVAL 1 DAY) ORDER BY tweet_text {}
            """.format("ASC" if chronological else "DESC")

            with engine.connect() as connection:
                rows = connection.execute(text(query), data)
        except Exception as err:
            exc.exception("Exception occurred in filter tweets query function. Error:{}".format(err))
        for row in rows:
            results.append({
                "tweet": row["tweet_text"],
                "created_at": row["created_at"]
            })
        return results

    except Exception as err:
        exc.exception("Exception occurred in db utils tweets filter function. Error:{}".format(err))
        print("Exception occurred in db utils tweets filter function.", err)
