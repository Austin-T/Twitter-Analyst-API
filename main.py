# import dependancies
from flask import Flask, request
from flask_restful import Resource, Api
from secretKeys import *
import tweepy
import random
from datetime import datetime
from textblob import TextBlob


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

def percentage(part, whole):
    # This function calculates a percentage given the 'part' (numerator) and the
    # 'whole' (denominator)
    percentage = 100 * float(part) / float(whole)
    return percentage

def getPolarity(tweets):
    # This function calculates the positive, neutral, and negative polarity of a set of 
    # tweets recieved from the twitter API. The total percentage of positive, negative,
    # and neutral tweets are returned as integers in a tuple.

    positive = 0
    neutral = 0
    negative = 0

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        polarity = analysis.sentiment.polarity

        if polarity > 0:
            positive += 1
        elif polarity < 0:
            negative += 1
        else:
            neutral += 1

    return (positive, neutral, negative)

# def getAllResponses(tweetID, username):
#     # This function returnes ever tweet which has been issued to a user in response
#     # to one of their messages

def getReplyPolarity(tweetID, responses):
    # This function calculates the positive, neutral, and negative polarity of a set of 
    # tweets that have been posted in reponse to the given 'tweet'. The percentage of 
    # positive polarities is returned

    # # Find all tweets which have been posted in response to any tweet of the user
    # toString = "to:" + username
    # responses = tweepy.Cursor(twitterAPI.search, q=toString, since_id=tweetID).items(100)

    # Create a subset of all responses which were directed at the specific tweet we are looking at
    replies = []
    for response in responses:
        if response.in_reply_to_status_id == tweetID:
            replies.append(response)

    # print(replies)
    if replies == []:
        # There are no replies to the given tweet so we return 999
        return 999
    else:
        # Find the total amount of positive replies, and the total amount of positive and negative
        # replies combined
        polarity = getPolarity(replies)
        total = 2 * (polarity[0] + polarity[1] + polarity[2])
        positive = 2 * polarity[0] + polarity[1]

        # return the total percentage of positive replies
        return percentage(positive, total)

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
        #try:
            # # rawData = twitterAPI.user_timeline(username)
            # rawData = tweepy.Cursor(twitterAPI.user_timeline).items(100)
            # # Find all tweets which have been posted in response to any tweet of the user
            # i = 0
            # for status in rawData:
            #     dictionary = status.__dict__
            #     i += 1
            #     if i == 99:
            #         tweetID = dictionary['id']
            #         break
            # print(tweetID)
            # toString = "to:@" + username
            # responses = tweepy.Cursor(twitterAPI.search, q=toString, since_id=tweetID).items()
            # print(responses)
            # print(tweetID)

        username = "@" + username
        toString = "to:" + username
        tweets = tweepy.Cursor(twitterAPI.user_timeline, screen_name=username).items(50)
        # tweetID = tweets[49].id
        # print(tweetID)
        # i = 0
        # for oneTweet in tweets:
        #     tweetID = oneTweet.id
        #     lastTweet = oneTweet.created_at
        #     i += 1
        # print(tweetID, i)
        # print(lastTweet)
        responses = tweepy.Cursor(twitterAPI.search, q=toString).items()
        # print(len(responses))
        # i = 0
        # for response in responses:
        # #     print(response, "\n\n", i, "\n\n\n")
        #     i += 1
        # print(i)




        #except:
            # user not found. return null
            #return

        allTweets = []

        for status in tweets:
            dictionary = status.__dict__

            # feedback = getReplyPolarity(dictionary["id"], responses)
            feedback = random.randint(0, 100)
            feedbackStr = "% Positive"
            if feedback == 999:
                feedback = 0
                feedbackStr = " Comments"
            
            tempDict = {
                "body": dictionary["text"],
                "retweets": dictionary["retweet_count"],
                "likes": dictionary["favorite_count"],
                "date": getDateString(dictionary['created_at']),
                "id": dictionary["id"],
                "feedback": feedback,
                "feedbackStr": feedbackStr,
                "hashtag": getHashtag(dictionary['text'])
            }
            allTweets.append(tempDict)
            # if len(allTweets) > 100:
            #     break

        return allTweets

class UserStats(Resource):
    def get(self, username):
        # Query the twitter API to get a result set containing the users 100 most recent mentions

        searchTerm = username
        numberOfSearches = 100

        # get the tweets from the twitter API
        tweets = tweepy.Cursor(twitterAPI.search, q=searchTerm).items(numberOfSearches)

        polarity = getPolarity(tweets)

        return [
            { "label": 'Positive', "value": polarity[0], "color": '#89e051' },
            { "label": 'Neutral', "value": polarity[1], "color": '#f1e05a' },
            { "label": 'Negative', "value": polarity[2], "color": '#e34c26' },
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
    