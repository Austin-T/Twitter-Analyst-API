import tweepy



def genAPI():
    # This function creates an instance of the tweepy.API object, and returns the
    # object. This object can then be used to read from and write to twitter.
    CONSUMER_KEY = '###'
    CONSUMER_SECRET = '###'
    ACCESS_KEY = '###'
    ACCESS_SECRET = '###'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api


def main():
    
    # Generate a new tweepy.API object
    api = genAPI()

main()