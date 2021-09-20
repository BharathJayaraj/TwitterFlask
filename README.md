# TwitterFlask
 
## App to fetch, search, filter tweets from twitter

Built using
- flask
- mysql
- sqlalchemy

## Create Application and Generate Access keys and Tokens from Developer page.

    Create Twitter account with developer access.
            https://twitter.com

    Create an App in developer page and this will generate a key for your key.
            https://developer.twitter.com/en/apply-for-access

    If need you have access to regenerate your keys and token.
    
    Enable 3-legged OAuth and give a callback url for Twitter login.
            Example for callback url : http://localhost:5001/login/twitter/authorized

In localhost give your machine IP address with your port address otherwise use it with localhost with default port address.

### How to run this app

Make sure that you've docker and docker-compose in your machine
```bash
git clone https://github.com/BharathJayaraj/Twitter-Flask.git
```
```bash
cd Twitter-Flask
```
```bash
python app.py
```
Go to ```http://127.0.0.1/```

### Running in Docker
```
 docker-compose up
 docker run {build_image}
 ```

### Working

- Twitter oAuth authentication is done using flask dance, first user is directed to twitter for auth and when the user is authenticated by twitter the user is redirected to the app.
- If the user is visiting the app for the first time, we will fetch all the tweets of user, when the same user is logged into the app next time, all the tweets from his timeline is not fetched only new tweets of the user is fetched from twitter.
- Mysql text search: For searching the tweets of the user I've used keyword search capability of mysql.
