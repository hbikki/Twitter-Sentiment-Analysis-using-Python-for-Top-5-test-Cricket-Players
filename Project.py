import tweepy
import matplotlib.pyplot as plt
import numpy as np
import time
from textblob import TextBlob
from gmplot import gmplot
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
geolocator = Nominatim(user_agent="dev")
exec(open("TwitterTokens.py").read())

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

good_tweets=[]
good_tweets_latitude=[]
good_tweets_longitude=[]
bad_tweets_latitude=[]
bad_tweets_longitude=[]
neutral_tweet=[]
bad_tweets=[]
now = time.strftime("%c")
names_full = np.array(['Kohli(IND)', 'Smith(AUS)', 'Williamson(NZ)', 'Root(ENG)', 'Warner(AUS)'])
names_twitter = np.array(['@imVkohli', '@stevesmith49', '@NotNossy', '@root66', '@davidwarner31'])
def getLocation_goodtweets():
      geolocator = Nominatim(user_agent="dev_good")
      try:
        for good_tweet in good_tweets:
            location=geolocator.geocode(good_tweet.user.location, timeout=10)
            if(location is not None):
                good_tweets_latitude.append(location.latitude)
                good_tweets_longitude.append(location.longitude)     
      except GeocoderTimedOut:
          return
    
def getLocation_badtweets():
    geolocator = Nominatim(user_agent="dev_bad")
    for bad_tweet in bad_tweets:
      try:
        for bad_tweet in bad_tweets:
            location=geolocator.geocode(bad_tweet.user.location, timeout=10)
            if(location is not None):
                bad_tweets_latitude.append(location.latitude)
                bad_tweets_longitude.append(location.longitude)     
      except GeocoderTimedOut:
          return
    
def plotMap_goodtweets():
    getLocation_goodtweets();
    gmap = gmplot.GoogleMapPlotter(41.8719, 12.5674,3)
    gmap.opacity = 0.2 #
    gmap.scatter(good_tweets_latitude, good_tweets_longitude, '#1A70ff', size=100000, marker=False)
    gmap.draw("goodtweets.html")
    
def plotMap_badtweets():
    getLocation_badtweets();
    gmap = gmplot.GoogleMapPlotter(41.8719, 12.5674,3)
    gmap.opacity = 0.2 #
    gmap.scatter(good_tweets_latitude, good_tweets_longitude, '#FF0000', size=100000, marker=False)
    gmap.draw("badtweets.html")
    
def getScores(str):
     tweets=getTweets(str)
     polarity_sum = 0	
     good_tweets_count=0;
     bad_tweets_count=0;
     netural_tweets_count=0;
     for tweet in tweets:
       tweet_text = TextBlob(tweet.text)
       polarity_sum += tweet_text.sentiment.polarity 
       if(tweet_text.sentiment.polarity >0):
           good_tweets_count=good_tweets_count+1;
           good_tweets.append(tweet);
       elif tweet_text.sentiment.polarity ==0:
           netural_tweets_count=netural_tweets_count+1;
           neutral_tweet.append(tweet);
       else:
           bad_tweets_count=bad_tweets_count+1;
           bad_tweets.append(tweet);
     return [polarity_sum/len(tweets),good_tweets_count,netural_tweets_count,bad_tweets_count];
 
def getTweets(str):
    tweets = api.search(str,count=100)
    return tweets;

def getPolarity():
    scores = []
    for player in names_twitter:
       player_score = getScores(player)[0]
       scores.append(player_score)
       print(player_score)
    return scores;

def plotGraph():
    scores=getPolarity();
    n_groups = len(names_twitter)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.5
    opacity = 0.8
    
    rects1 = plt.bar(index, scores, bar_width,
                     alpha=opacity,
                     color='b',                 
                     label='Polarity [-1, 1]')
    
    for x in range(0, n_groups):
    	scl = scores[x]	
    	if scl<0:
    		rects1[x].set_color((0.9,0,0))
    	else: rects1[x].set_color((0,0,0.9))
    
    rects = ax.patches
    for rect,scl in zip(rects,scores):
    	height = rect.get_height()
    	ax.text(rect.get_x() + rect.get_width()/2, height , round(scl,2), ha='center', va='bottom')
    
    
    plt.xticks(index , names_full)
    plt.ylim((-0.25,1))
    plt.hlines(0, 0-bar_width, n_groups, colors='k', linestyles='solid', label='')
    plt.ylabel(now)
    plt.legend()
    plt.tight_layout()
    plt.show()
  
    
def plotPieChart(name,good,neutraql,bad):
    labels = 'Good', 'Neutral', 'Bad'
    sizes = [good, neutraql, bad]
    explode = (0.1, 0, 0)
    fig1, ax1 = plt.subplots()
    ax1.set_title(name)
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
def getSentiments():
    inc=0
    for player in names_twitter:
        scores=getScores(player)
        plotPieChart(names_full[inc],scores[1],scores[2],scores[3])
        inc=inc+1
    
    
    
plotGraph()   
getSentiments()
plotMap_goodtweets()
#plotMap_badtweets()