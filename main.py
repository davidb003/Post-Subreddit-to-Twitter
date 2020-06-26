'''
Edited by https://github.com/davidb003
Original Code: https://github.com/rhiever/reddit-twitter-bot
LICENSE: GNU General Public License v3.0
'''

import praw
import json
import requests
import tweepy
import time
import os
import urllib.parse
from glob import glob
from time import sleep

while 3 > 2:

    # Twitter API Credentials
    ACCESS_TOKEN = ''
    ACCESS_TOKEN_SECRET = ''
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''

    # Reddit API Credentials
    # Documentation: https://github.com/reddit-archive/reddit/wiki/OAuth2
    reddit = praw.Reddit(client_id='',
                         client_secret="", password='',
                         user_agent='none', username='')

    #config
    SUBREDDIT_TO_MONITOR = ''
    IMAGE_DIR = 'img'
    POSTED_CACHE = 'posted.txt'
    TWEET_SUFFIX = '#yoursuffixhere' #go to line 110
    TWEET_MAX_LEN = 140
    DELAY_BETWEEN_TWEETS = 120 #seconds
    T_CO_LINKS_LEN = 24

    #code
    def setup_connection_reddit(subreddit):
        print('[...] Connecting to reddit...')
        reddit_api = praw.Reddit('reddit Twitter tool monitoring {}'.format(subreddit))
        return reddit_api.get_subreddit(subreddit)


    def tweet_creator(subreddit_info):
        post_dict = {}
        post_ids = []

        print('[OK] Connected to the Reddit servers. Checking for posts...')

        for submission in subreddit_info.get_new(limit=100):
            if not already_tweeted(submission.id):
                post_dict[submission.title] = {}
                post = post_dict[submission.title]
                post['link'] = submission.permalink
                post['img_path'] = get_image(submission.url)

                post_ids.append(submission.id)
            else:
                print('[i] Already tweeted: {}'.format(str(submission)))

        return post_dict, post_ids


    def already_tweeted(post_id):
        found = False
        with open(POSTED_CACHE, 'r') as in_file:
            for line in in_file:
                if post_id in line:
                    found = True
                    break
        return found


    def strip_title(title, num_characters):
        if len(title) <= num_characters:
            return title
        else:
            return title[:num_characters - 1] + '…'


    def get_image(img_url):
        if 'imgur.com' in img_url:
            file_name = os.path.basename(urllib.parse.urlsplit(img_url).path)
            img_path = IMAGE_DIR + '/' + file_name
            print('[...] Downloading image at URL ' + img_url + ' to ' + img_path)
            resp = requests.get(img_url, stream=True)
            if resp.status_code == 200:
                with open(img_path, 'wb') as image_file:
                    for chunk in resp:
                        image_file.write(chunk)
                return img_path
            else:
                print('[X] Image failed to download. Status code: ' + resp.status_code)
        else:
            print('[i] A link has been found in a post but it doesn\'t point to an i.imgur.com link')
        return ''


    def tweeter(post_dict, post_ids):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        for post, post_id in zip(post_dict, post_ids):
            img_path = post_dict[post]['img_path']

            extra_text = ' - #yoursuffixhere ' + post_dict[post]['link'] #suffix
            extra_text_len = 1 + T_CO_LINKS_LEN + len(TWEET_SUFFIX)
            if img_path:
                extra_text_len += T_CO_LINKS_LEN
            post_text = strip_title(post, TWEET_MAX_LEN - extra_text_len) + extra_text
            print('[OK] Posting this link on Twitter')
            print(post_text)
            if img_path:
                print('[OK] With image ' + img_path)
                api.update_with_media(filename=img_path, status=post_text)
            else:
                api.update_status(status=post_text)
            log_tweet(post_id)
            time.sleep(DELAY_BETWEEN_TWEETS)


    def log_tweet(post_id):
        with open(POSTED_CACHE, 'a') as out_file:
            out_file.write(str(post_id) + '\n')


    def main():
        if not os.path.exists(POSTED_CACHE):
            with open(POSTED_CACHE, 'w'):
                pass
        if not os.path.exists(IMAGE_DIR):
            os.makedirs(IMAGE_DIR)

        subreddit = setup_connection_reddit(SUBREDDIT_TO_MONITOR)
        post_dict, post_ids = tweet_creator(subreddit)
        tweeter(post_dict, post_ids)

        for filename in glob(IMAGE_DIR + '/*'):
            os.remove(filename)
        
    print('[...] Sleeping...')
    sleep(86400) #seconds

    #If you want to remove this sleep, be sure to remove the loop on line 17 and indent everything back


    if __name__ == '__main__':
        main()
