# import dependancies
from flask import Flask, request
from flask_restful import Resource, Api
from secretKeys import *
import tweepy

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
        # get basic user statistics: tweets, likes, retweets

        # return {
        #     "login": 'bchiang7',
        #     "name": 'Brittany Chiang',
        #     "id": 6599979,
        #     "avatar_url": 'https://avatars2.githubusercontent.com/u/6599979?v=4',
        #     "url": 'https://api.github.com/users/bchiang7',
        #     "html_url": 'https://github.com/bchiang7',
        #     "public_repos": 53,
        #     "public_gists": 4,
        #     "followers": 248,
        #     "following": 12,
        #     "created_at": '2014-02-05T23:22:59Z',
        #     "updated_at": '2019-04-17T03:18:31Z',
        #     }, 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Add classes/methods to api at the appropriate url extension
api.add_resource(HelloWorld, '/')
api.add_resource(UserData, '/user-data/<string:username>')

    

if __name__ == "__main__":
    # run the server
    app.run(debug=True)
    