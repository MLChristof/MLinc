from twitter import Twitter
from textblob import TextBlob


twitter_api = Twitter()

tweets = twitter_api.get_tweets('1085519375224983552')

for i in tweets:
    text = i['full_text']
    text_blob = TextBlob(text)

    polarity, subjectivity = text_blob.sentiment

    print(polarity, subjectivity)


    #
    # text = TextBlob(tweet)
    # newsentiment = text.sentiment
    #
    # print tweet
    # print text.tags
    # print text.noun_phrases
    # print newsentiment




