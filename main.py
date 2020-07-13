# import dependancies
from flask import Flask, request
from flask_restful import Resource, Api
from secretKeys import *
import tweepy
import random

# Connect to the twitter API using consumer/access keys/secrets
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitterAPI = tweepy.API(auth)

# create Flask & Api objects
app = Flask(__name__)
api = Api(app)

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
        avatarURL = rawData['profile_image_url_https']
        name = rawData['name']
        screenName = rawData['screen_name']
        location = rawData['location']
        url = rawData['url']    
        createdAt = rawData['created_at']
        createdAt = "2014-02-05T23:22:59Z"
        followersCount = rawData['followers_count']
        followingCount = rawData['friends_count']
        tweetsCount = rawData['statuses_count']

        # return the user information
        return {
            "avatarURL": avatarURL,
            "name": name,
            "screenName": screenName,
            "location": location,
            "url": url,
            "createdAt": createdAt,
            "followersCount": followersCount,
            "followingCount": followingCount,
            "tweetsCount": tweetsCount,
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

            # isolate the first hashtag which appears in the text
            index1 = -1
            index2 = -1
            for i in range(0, len(dictionary['text'])):
                if dictionary['text'][i] == '#':
                    index1 = i
                elif dictionary['text'][i] == ' ':
                    if index1 != -1:
                        index2 = i + 1
                        break

            if index1 == -1:
                hashtag = ''
            else:
                hashtag = dictionary['text'][index1:index2]

            tempDict = {
                "body": dictionary["text"],
                "retweets": dictionary["retweet_count"],
                "likes": dictionary["favorite_count"],
                # "createdAt": dictionary["created_at"],
                "date": "June 9 2020",
                "id": dictionary["id"],
                "feedback": random.randint(0, 100),
                "hashtag": hashtag
            }
            allTweets.append(tempDict)

        print(allTweets)
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
    