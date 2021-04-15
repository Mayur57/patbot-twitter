import tweepy
import time
import random

consumer_key = '<REPLACE-WITH-YOUR-OWN>'
consumer_secret = '<REPLACE-WITH-YOUR-OWN>'
access_token = '<REPLACE-WITH-YOUR-OWN>'
access_token_secret = '<REPLACE-WITH-YOUR-OWN>'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

FILE_NAME = 'last.txt'
GIF = 'pat-pat.gif'

api = tweepy.API(auth)

# This function will open the text file and return the ID of
# the latest tweet the bot has successfully replied to 
def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

# Overwrite the previous Tweet ID with latest
def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

appreciations = [
    "You're looking absolutely gorgeous today ;)",
    "Here's a bonus hug from me!",
    "Go drink some water!"
    "I love your tweets!",
    "You're awesome",
    "Should I be worried that my creator is a dumbass?",
    "You're are so smart, people had to increase range of the IQ scale",
    "I want to be as cool as you",
    "Do you want to go out on a coffee date maybe?",
]


# Pick appreciation randomly
def random_appreciation():
    return appreciations[random.randrange(0, 8)]

def reply():
    # The API will only send a response containing tweets with IDs that come after the ID
    # stored in the text file
    tweets = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode='extended')
    for tweet in reversed(tweets):
        if 'pat' in tweet.full_text.lower():
            print("Pattted!: " + str(tweet.id) + " - " + tweet.full_text.lower())
            api.update_with_media(GIF, "@"+ tweet.user.screen_name + " pat pat" + "\nPS: " + random_appreciation(), in_reply_to_status_id=tweet.id)
            api.create_favorite(tweet.id) # Like the tweet with mentions
            store_last_seen(FILE_NAME, tweet.id)


"""
The program needs to run continuously to fetch and reply to tweets. This loop
runs infinitely and executes the reply() functions checking for mentions and
has a timeout of 15 seconds between each poll so that rate limits imposed by
Twitter APIs are not tripped.
"""
while True:
    reply()
    time.sleep(15)