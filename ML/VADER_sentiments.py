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

from .models import Query_data

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id = os.getenv('Muhammadinho_Client_ID'),
    client_secret = os.getenv('Muhammadinho_Client_Secret'),
    user_agent =  os.getenv('Muhammadinho_user_agent'),
    )

def start_sentiment_analysis_VADER(query):
    try:
        comments_max =  750
        limit = 15
        comments = []

        # Check if there are existing comments related to 'query' in the database.
        existing_query = Query_data.objects.filter(query_name=query).first()

        if existing_query and existing_query.get_comments():
            # Use existing comments from the database.
            comments = existing_query.get_comments()
            print(query + ' data fetch to database')
        else:
            for submission in reddit.subreddit("all").search(query, limit=limit):
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    comments.append(comment.body)
                    if len(comments) >= comments_max:
                        break

            # Save the newly fetched comments to the database.
            if not existing_query:
                # If the query doesn't exist in the database, create a new instance and save comments.
                query_instance = Query_data(query_name=query)
                query_instance.save_comments(comments)

        sentiments_data = calculate_sentiment(comments)
        comments_wordcloud = generate_wordcloud(comments)

    except praw.exceptions.PRAWException as reddit_exception:
        print('Reddit API error:', str(reddit_exception))
        return None, None

    except Exception as e:
        print('Error:', str(e))
        return None, None

    return sentiments_data, comments_wordcloud


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# nltk.download('punkt')
def calculate_sentiment(comments):
    # Initialize the VADER sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()
    vader_scores = []  # Initialize a list to store VADER sentiment scores

    for comment in comments:
        vader_scores.append(analyzer.polarity_scores(comment)["compound"])

    # top_comments = get_top_comments(comments, vader_scores, textblob_scores)
    top_pos_vader, top_neg_vader = get_top_comments(comments, vader_scores)

    # Calculate the average compound sentiment score using VADER
    avg_vader_score = sum(vader_scores) / len(vader_scores)


    # Create line charts and Heatmap for VADER scores
    plt.figure(figsize=(8, 4))
    sns.histplot(vader_scores, bins=10, kde=True)
    plt.title("VADER Sentiment Analysis")
    plt.xlabel("Compound Sentiment Score")
    plt.ylabel("Frequency")
    # Convert the chart image to a base64-encoded string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str1 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    plt.figure(figsize=(8, 6))
    vader_scores_array = np.array(vader_scores).reshape(len(vader_scores), 1)
    sns.heatmap(vader_scores_array, cmap="coolwarm", annot=True, fmt=".2f", cbar=True)
    plt.title("VADER Sentiment Analysis Heatmap")
    plt.xlabel("Comments")
    plt.ylabel("Samples")
    # Convert the heatmap image to a base64-encoded string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str2 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")


    return avg_vader_score, img_str1, img_str2, top_pos_vader, top_neg_vader

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

def get_top_comments(comments, vader_scores):
    # Combine comments, TextBlob scores, and VADER scores into a list of dictionaries
    comment_data = [{'comment': comment, 'vader_score': vader_score}
                    for comment, vader_score in zip(comments, vader_scores)]

    # Sort comments by VADER sentiment score (positive to negative)
    sorted_comments_positive_vader = sorted(comment_data, key=lambda x: x['vader_score'], reverse=True)
    top_positive_comments_vader = [comment['comment'] for comment in sorted_comments_positive_vader[:10]]

    # Sort comments by VADER sentiment score (negative to positive)
    sorted_comments_negative_vader = sorted(comment_data, key=lambda x: x['vader_score'])
    top_negative_comments_vader = [comment['comment'] for comment in sorted_comments_negative_vader[:10]]

    return (top_positive_comments_vader, top_negative_comments_vader)
