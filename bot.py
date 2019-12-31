import os
import time
import logging
import json
from logging.config import fileConfig

import praw

from utils.util import get_env, is_keyword_mentioned, get_random_quote, get_username

fileConfig('log.ini')
logger = logging.getLogger('reddit-bots')
logger.info("Started Reddit bot")

try:
    environment = get_env('ENV', __file__)
    if environment == 'STAGE':
        subreddits = get_env('SUBS', __file__)
    elif environment == 'PROD':
        with open('config/subreddits.json', 'r') as subs:
            raw = json.load(subs)
            subreddits = '+'.join(raw)
    logger.info("Environment detected - {}".format(environment))
    logger.info("Active subreddits - {}".format(subreddits))
except Exception as e:
    logger.exception("Could not get environment variables: {}".format(str(vars(e))))

if not os.path.isfile('posts_replied_to.dat'):
    open("posts_replied_to.dat", 'w+')

if __name__ == '__main__':

    reddit = praw.Reddit('geraltOfReddit')
    logger.info("Instantiated client for Geralt of Reddit")
    while True:
        try:
            with open('posts_replied_to.dat', 'r') as f:
                posts_replied_to = f.read()
                posts_replied_to = posts_replied_to.split('\n')
                posts_replied_to = list(filter(None, posts_replied_to))
                logger.info("Got posts that were already replied to")

            subreddit = reddit.subreddit(subreddits)
            for comment in subreddit.stream.comments():
                if comment.id not in posts_replied_to:
                    username = get_username(comment.author)
                    replied = False
                    if username == 'jaskier-bot':
                        logger.info("Jaskier said - {}".format(comment.body))
                        comment.reply(get_random_quote('jaskier'))
                        replied = True
                    elif is_keyword_mentioned(comment.body):
                        logger.info("Matching comment found - {}".format(comment.body))
                        comment.reply(get_random_quote())
                        replied = True                    
                    if replied:
                        logger.info("Replied to comment on subreddit - {}".format(comment.subreddit))
                        posts_replied_to.append(comment.id)
                        logger.info("Appended to posts_replied_to list")
                        with open("posts_replied_to.dat", 'a') as f:
                            f.write(comment.id + "\n")
                            logger.info("Updated posts_replied_to list on file")

        except APIException as e:
            logger.exception("Error !!: {}".format(str(vars(e))))
            logger.error("Error occured, retrying after 3 mins")
            time.sleep(180)
