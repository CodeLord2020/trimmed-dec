import os
from environs import Env
env = Env()
env.read_env()


import praw
import json
from io import BytesIO
import base64
import requests
import nltk
import seaborn as sns


# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id = os.getenv('Client_ID'),
    client_secret = os.getenv('Client_Secret'),
    user_agent =  os.getenv('user_agent'),
    # password =  os.getenv('password'),
    # username =  os.getenv('username'),
    )



#############################################             Data Collection          ############################################################################
def start_sentiment_analysis_VADER(query):
    try:    
        comments_max = 300
        limit = 5
        comments = []
        for submission in reddit.subreddit("all").search(query, limit=limit):
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                comments.append(comment.body)
                if len(comments) >= comments_max:
                    break
            setiments_data = calculate_sentiment(comments)
            comments_wordcloud = generate_wordcloud(comments)

    except praw.exceptions.PRAWException as reddit_exception:
        # Handle Reddit API exceptions (e.g., rate limiting)
        print('Reddit API error:', str(reddit_exception))
        return None, None  # You can return None or handle the error as needed

    except Exception as e:
        # Handle other exceptions
        print('Error:', str(e))
        return None, None  # You can return None or handle the error as needed
    return setiments_data, comments_wordcloud

# comments_text = ' '.join(comments)

#################################################            VADER TEST          ############################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

analyser = SentimentIntensityAnalyzer()
nltk.download('punkt')
def calculate_sentiment(comments):
    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()
    vader_scores = []  # Initialize a list to store VADER sentiment scores
    textblob_scores = []  # Initialize a list to store TextBlob sentiment scores

    for comment in comments:
        vader_scores.append(analyzer.polarity_scores(comment)["compound"])
        textblob_scores.append(TextBlob(comment).sentiment.polarity)

    # Calculate the average compound sentiment score using VADER
    avg_vader_score = sum(vader_scores) / len(vader_scores)

    # Calculate the average sentiment score using TextBlob
    avg_textblob_score = sum(textblob_scores) / len(textblob_scores)

    # Create line charts for VADER and TextBlob scores
    plt.figure(figsize=(8, 4))
    sns.histplot(vader_scores, bins=10, kde=True)
    plt.title("VADER Sentiment Analysis")
    plt.xlabel("Compound Sentiment Score")
    plt.ylabel("Frequency")
    # Convert the chart image to a base64-encoded string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str1 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    # Create line charts for VADER and TextBlob scores
    plt.figure(figsize=(8, 4))
    sns.histplot(textblob_scores, bins=10, kde=True)
    plt.title("VADER Sentiment Analysis")
    plt.xlabel("Compound Sentiment Score")
    plt.ylabel("Frequency")
    # Convert the chart image to a base64-encoded string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str2 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    return avg_vader_score, avg_textblob_score, img_str1, img_str2



# compound_score = 0


# for comment in comments:
#     sentiment = analyzer.polarity_scores(comment)
#     compound_score += sentiment['compound']

# num_comments = len(comments)
# avg_compound_score = compound_score / num_comments


# return avg_compound_score


from wordcloud import WordCloud
def generate_wordcloud(comments):
    # Combine comments into a single text string
    comments_text = ' '.join(comments)

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400).generate(comments_text)

    # Convert the word cloud image to a base64-encoded string
    img_buffer = BytesIO()
    wordcloud.to_image().save(img_buffer, format="PNG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    return img_str

