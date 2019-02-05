from twitter import Twitter
from textblob import TextBlob
from mlinc.notifier import notification, file_robert, file_christof, file_jelle, file_vincent


twitter_api = Twitter()

tweets = twitter_api.get_tweets('1085519375224983552')

for i in tweets:
    text = i['full_text']
    time = i['created_at']

    text_blob = TextBlob(text)
    polarity, subjectivity = text_blob.sentiment

    nouns = text_blob.noun_phrases

    message = f'Date = {time} \n {text} \n Nouns: {nouns} \n Polarity = {polarity}, Subjectivity = {subjectivity}'

    print(message)

    # notification(fileID=file_christof, message=message)
    # notification(fileID=file_vincent, message=message)



    #
    # text = TextBlob(tweet)
    # newsentiment = text.sentiment
    #
    # print tweet
    # print text.tags
    # print text.noun_phrases
    # print newsentiment




