import config
import tweepy
import datetime


def create_tweepy_client():
    try:
        auth = tweepy.OAuthHandler(
            consumer_key=config.Config.TWITTER_OAUTH_CLIENT_KEY,
            consumer_secret=config.Config.TWITTER_OAUTH_CLIENT_SECRET
        )
        auth.set_access_token(
            key=config.Config.TWITTER_OAUTH_ACCESS_KEY,
            secret=config.Config.TWITTER_OAUTH_ACCESS_SECRET
        )
        client = tweepy.API(auth)
        return client
    except Exception as err:
        print("Exception occurred in twitter authentication function.", err)


def get_timeline(client, screen_name, last_pulled_at=None):
    timeline = []
    try:
        for status in tweepy.Cursor(client.user_timeline, id=screen_name).items():
            time_change = datetime.timedelta(hours=5, minutes=30, seconds=50)
            status.created_at = status.created_at + time_change
            if last_pulled_at and status.created_at < last_pulled_at:
                break

            timeline.append({
                "id": status.id,
                "tweet": status.text,
                "created_at": status.created_at
            })
        return timeline, len(timeline)
    except Exception as err:
        print("Exception occurred in twitter timeline function.", err)


def get_timeline_for_user(screen_name, last_pulled_at=None):
    try:
        client = create_tweepy_client()
        timeline = get_timeline(client, screen_name, last_pulled_at)
        return timeline
    except Exception as err:
        print("Exception occurred in twitter user timeline function.", err)
