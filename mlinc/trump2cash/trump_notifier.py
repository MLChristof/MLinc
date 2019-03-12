from mlinc.trump2cash.core.twitter import Twitter
from textblob import TextBlob
from mlinc.notifier import notification, file_robert, file_christof, file_jelle, file_vincent


twitter_api = Twitter()

# test_id = '1085519375224983552'

with open('last_id.txt', 'r') as f:
    last_tweet_id = f.read()

tweets = twitter_api.get_tweets(last_tweet_id)
# tweets = twitter_api.get_tweets(test_id)

for i in tweets:
    text = i['full_text']
    time = i['created_at']

    text_blob = TextBlob(text)
    polarity, subjectivity = text_blob.sentiment

    nouns = text_blob.noun_phrases

    message = f'Date = {time} \n {text} \n Nouns: {nouns} \n Polarity = {polarity}, Subjectivity = {subjectivity}'

    if abs(polarity) > 0.8:
        notification(fileID=file_christof, message=message)
        notification(fileID=file_jelle, message=message)
        notification(fileID=file_robert, message=message)
        notification(fileID=file_vincent, message=message)

with open('last_id.txt', 'w') as f:
    f.write(str(tweets[0]['id']))





