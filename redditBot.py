import praw 
import re
import time
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("config.ini")
config = config_object["CONFIG"]

reddit = praw.Reddit(client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            username=config['username'], 
            password=config['password']) 


reddit.validate_on_submit=True

subreddits = config['subreddits'].split(',')
pos=0
errors = 0
 
title = config['title']
text = config['text']
text = text.replace('\\n', '\n\n')

def post():
    global subreddits
    global pos
    global errors
    try:      
        subreddit = reddit.subreddit(subreddits[pos])
        subreddit.submit(title,selftext=text)
        print("Posted to " + subreddits[pos])

        pos = pos+1

        if(pos <= len(subreddits) - 1):
            post() 
        else:
            print("Done")
    except praw.exceptions.APIException as e: 
        if(e.error_type == "RATELIMIT"):
            delay = re.search("minutes?", e.message)

            if delay:
                delay_seconds = float(int(delay.group(1))*60)
                time.sleep(delay_seconds)
                post()
            else:
                delay = re.search("seconds",e.message)
                delay_seconds = float(delay.group(1))
                time.sleep(delay_seconds)
                post()

    except:
        errors = errors + 1
        if(errors > 5):
            print("Crashed")
            exit(1)                            


post()
