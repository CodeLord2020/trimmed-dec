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

from .models import Query_data
import seaborn as sns

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id = os.getenv('Client_ID'),
    client_secret = os.getenv('Client_Secret'),
    user_agent =  os.getenv('user_agent'),

    )

#############################################             Data Collection          ############################################################################

def start_sentiment_analysis_TextBlob(query):
    try:
        comments_max =  750
        limit = 15
        comments = []

        # Check if there are existing comments related to 'query' in the database.
        existing_query = Query_data.objects.filter(query_name=query).first()

        if existing_query and existing_query.get_comments():
            # Use existing comments from the database.
            comments = existing_query.get_comments()
            print(query + ' data fetch from database')
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
                print(query + ' data saved to database')

        sentiments_data = calculate_sentiment(comments)
        comments_wordcloud = generate_wordcloud(comments)

    except praw.exceptions.PRAWException as reddit_exception:
        print('Reddit API error:', str(reddit_exception))
        return None, None

    except Exception as e:
        print('Error:', str(e))
        return None, None

    return sentiments_data, comments_wordcloud


#################################################            VADER/TextBlob  Scores and Visuals        ############################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob


# nltk.download('punkt')
def calculate_sentiment(comments):
    textblob_scores = []  # Initialize a list to store TextBlob sentiment scores

    for comment in comments:
        textblob_scores.append(TextBlob(comment).sentiment.polarity)

    # top_comments = get_top_comments(comments, vader_scores, textblob_scores)
    top_pos_textblob, top_neg_textblob = get_top_comments(comments, textblob_scores)

    # Calculate the average sentiment score using TextBlob
    avg_textblob_score = sum(textblob_scores) / len(textblob_scores)


    # Create line charts and Heatmap TextBlob scores
    plt.figure(figsize=(8, 4))
    sns.histplot(textblob_scores, bins=10, kde=True)
    plt.title("VADER Sentiment Analysis")
    plt.xlabel("Compound Sentiment Score")
    plt.ylabel("Frequency")
    # Convert the chart image to a base64-encoded string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str1 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    plt.figure(figsize=(8, 6))
    textblob_scores_array = np.array(textblob_scores).reshape(len(textblob_scores), 1)
    sns.heatmap(textblob_scores_array, cmap="coolwarm", annot=True, fmt=".2f", cbar=True)
    plt.title("VADER Sentiment Analysis Heatmap")
    plt.xlabel("Comments")
    plt.ylabel("Samples")
    # Convert the heatmap image to a base64-encoded string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str2 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    return avg_textblob_score, img_str1, img_str2, top_pos_textblob, top_neg_textblob 

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

def get_top_comments(comments, textblob_scores):
    # Combine comments, TextBlob scores, and VADER scores into a list of dictionaries
    comment_data = [{'comment': comment, 'textblob_score': textblob_score}
                    for comment, textblob_score in zip(comments, textblob_scores)]

    # Sort comments by TextBlob sentiment score (positive to negative)
    sorted_comments_positive_textblob = sorted(comment_data, key=lambda x: x['textblob_score'], reverse=True)
    top_positive_comments_textblob = [comment['comment'] for comment in sorted_comments_positive_textblob[:10]]


    # Sort comments by TextBlob sentiment score (negative to positive)
    sorted_comments_negative_textblob = sorted(comment_data, key=lambda x: x['textblob_score'])
    top_negative_comments_textblob = [comment['comment'] for comment in sorted_comments_negative_textblob[:10]]

    return (top_positive_comments_textblob, top_negative_comments_textblob)
