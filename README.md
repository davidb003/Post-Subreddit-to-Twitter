# Post-Subreddit-to-Twitter
Allows you to repost all the new posts of a specified subreddit to a Twitter profile

# Requirements
- Tweepy 3.8.0
- Praw 6.5.1

### Installation
```
pip3 install tweepy==3.8.0
pip3 install praw==6.5.1
```

# Getting Started
1. Paste your Twitter API credentials below "Twitter API Credentials". You can get those from the [Twitter Developers page](https://developer.twitter.com/en/apps)
2. Paste your Reddit Client ID, Client Secret, Username and Password below "Reddit API Credentials". If you don't have the Client ID and Secret, you can get them from the [Reddit Settings](https://www.reddit.com/prefs/apps)
3. Edit below config as you like
**PLEASE NOTE: Remember to set your Tweet suffix in line 110!**
4. If you don't need the sleep function, delete the lines 146 and 17 and **INDENT EVERYTHING BACK**

# What's different from the original version?
- Tweet suffix fixed
- Added Reddit authentication
- Added the sleep function (Useful if the mods wanna check (and remove) the posts before the bot publishes them on Twitter)

> You can find the original version of this code [here](https://github.com/rhiever/reddit-twitter-bot)

> I'm a Python Beginner, so don't get mad if I wrote the code badly :)

# Support
I'm not planning to spend time on this code anymore, however you can create issues and answer them.
Feel free to update the code if you want! Just create an issue and paste your code. Credits will be added.
