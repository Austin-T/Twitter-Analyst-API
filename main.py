# import dependancies
from flask import Flask, request
from flask_restful import Resource, Api
from secretKeys import *
import tweepy
import random
from datetime import datetime

# Connect to the twitter API using consumer/access keys/secrets
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitterAPI = tweepy.API(auth)

# create Flask & Api objects
app = Flask(__name__)
api = Api(app)

# create helper functions for handling client requests
def getHashtag(text):
    # This function takes in a string and searches that string for a hashtag.
    # hashtags are denoted by a # (pound), followed by one or more characters,
    # and ending with a space. The function returns the first found hashtag as
    # a string.

    # isolate the indicies of the first hashtag to appear in the text
    index1 = -1
    index2 = -1
    for i in range(0, len(text)):
        if text[i] == '#':
            index1 = i
        elif text[i] == ' ':
            if index1 != -1:
                index2 = i + 1
                break

    # if no hashtag was found, return an empty string
    if index1 == -1:
        return ''
    else:
        return text[index1:index2]

def getDate(date):
    # This function takes in a datetime.datetime obejct and converts it to a 
    # serializable string which can be sent to the client.
    dateString = date.strftime("%FT%H:%M:%SZ")
    return dateString

def getDateString(date):
    # This funciton takes in a datetime.datetime object and converts it to a
    # human readable string, including the month and day only.
    dateString = date.strftime("%B %d")
    return dateString

# Define classes/methods for handling client requests
class HelloWorld(Resource):
    def get(self):
        return {"about": "Hello World"}, 200

class UserData(Resource):
    def get(self, username):
        # Query the twitter API to get a result set containing information about the user
        try:
            rawData = twitterAPI.get_user(username)
        except:
            # user not found. return null
            return

        rawData = rawData.__dict__

        # get user information
        # avatarURL = rawData['profile_image_url_https']
        # name = rawData['name']
        # screenName = rawData['screen_name']
        # location = rawData['location']
        # url = rawData['url']    
        # createdAt = rawData['created_at']
        # createdAt = "2014-02-05T23:22:59Z"
        # followersCount = rawData['followers_count']
        # followingCount = rawData['friends_count']
        # tweetsCount = rawData['statuses_count']
        

        # return the user information
        return {
            "avatarURL": rawData['profile_image_url_https'],
            "name": rawData['name'],
            "screenName": rawData['screen_name'],
            "location": rawData['location'],
            "url": rawData['url'],
            "createdAt": getDate(rawData['created_at']),
            "followersCount": rawData['followers_count'],
            "followingCount": rawData['friends_count'],
            "tweetsCount": rawData['statuses_count'],
        }

class UserTweets(Resource):
    def get(self, username):
        # Query the twitter API to get a result set containing the users 20 most recent tweets
        try:
            rawData = twitterAPI.user_timeline(username)

        except:
            # user not found. return null
            return

        allTweets = []

        for status in rawData:
            # print(status.__dict__.keys())
            dictionary = status.__dict__

            # # isolate the first hashtag which appears in the text
            # index1 = -1
            # index2 = -1
            # for i in range(0, len(dictionary['text'])):
            #     if dictionary['text'][i] == '#':
            #         index1 = i
            #     elif dictionary['text'][i] == ' ':
            #         if index1 != -1:
            #             index2 = i + 1
            #             break

            # if index1 == -1:
            #     hashtag = ''
            # else:
            #     hashtag = dictionary['text'][index1:index2]

            tempDict = {
                "body": dictionary["text"],
                "retweets": dictionary["retweet_count"],
                "likes": dictionary["favorite_count"],
                # "createdAt": dictionary["created_at"],
                "date": getDateString(dictionary['created_at']),
                "id": dictionary["id"],
                "feedback": random.randint(0, 100),
                "hashtag": getHashtag(dictionary['text'])
            }
            allTweets.append(tempDict)
            # print(dictionary["created_at"], ",", type(dictionary["created_at"]))

        # print(allTweets)
        return allTweets
        # rawData = rawData.__dict__

        # # get tweet information
        # avatarURL = rawData['profile_image_url_https']
        # name = rawData['name']
        # screenName = rawData['screen_name']
        # location = rawData['location']
        # url = rawData['url']    
        # createdAt = rawData['created_at']
        # createdAt = "2014-02-05T23:22:59Z"
        # followersCount = rawData['followers_count']
        # followingCount = rawData['friends_count']
        # tweetsCount = rawData['statuses_count']

        # # return the user information
        # return {
        #     "avatarURL": avatarURL,
        #     "name": name,
        #     "screenName": screenName,
        #     "location": location,
        #     "url": url,
        #     "createdAt": createdAt,
        #     "followersCount": followersCount,
        #     "followingCount": followingCount,
        #     "tweetsCount": tweetsCount,
        # }

class UserStats(Resource):
    def get(self, username):
        # Query the twitter API to get a result set containing the users 20 most recent tweets
        # try:
        #     rawData = twitterAPI.user_timeline(username)

        # except:
        #     # user not found. return null
        #     return

        return [
            { "label": 'Positive', "value": 24, "color": '#89e051' },
            { "label": 'Neutral', "value": 16, "color": '#f1e05a' },
            { "label": 'Negative', "value": 7, "color": '#e34c26' },
        ]


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Add classes/methods to api at the appropriate url extension
api.add_resource(HelloWorld, '/')
api.add_resource(UserData, '/user-data/<string:username>')
api.add_resource(UserTweets, '/user-tweets/<string:username>')
api.add_resource(UserStats, '/user-stats/<string:username>')

    

if __name__ == "__main__":
    # run the server
    app.run(debug=True)
    