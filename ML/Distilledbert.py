from environs import Env
env = Env()
env.read_env()

import os

import praw
from io import BytesIO
import base64
from .models import Query_data
from transformers import pipeline
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('Marvel_Client_ID'),
    client_secret=os.getenv('Marvel_Client_Secret'),
    user_agent=os.getenv('Marvel_user_agent'),
)

def analyze_sentiment(comments):
    sentiments = []
    scores = []
    positive_comments = []
    negative_comments = []
    neutral_comments = []

    for comment in comments:
        # Analyze sentiment for each comment
        result = sentiment_pipeline(comment)
        sentiment_label = result[0]['label']
        sentiments.append(sentiment_label)
        scores.append(result[0]['score'])

        if sentiment_label == 'positive' and len(positive_comments) < 10:
            positive_comments.append(comment)
        elif sentiment_label == 'negative' and len(negative_comments) < 10:
            negative_comments.append(comment)
        elif sentiment_label == 'neutral' and len(neutral_comments) < 10:
            neutral_comments.append(comment)

        if len(positive_comments) >= 10 and len(negative_comments) >= 10 and len(neutral_comments) >= 10:
            break

    return sentiments, scores, positive_comments, negative_comments, neutral_comments

def calculate_total_average(scores):
    total_score = sum(scores)
    total_count = len(scores)

    if total_count > 0:
        total_average = total_score / total_count
        return total_average

    return None

def plot_sentiments(sentiments_data):
    sentiment_counts = Counter(sentiments_data)

    color_mapping = {
        'positive': 'green',
        'negative': 'red',
        'neutral': 'yellow',
    }

    labels = sentiment_counts.keys()
    counts = sentiment_counts.values()

    colors = [color_mapping.get(label, 'green') for label in labels]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color=colors)
    plt.xlabel('Sentiment Labels')
    plt.ylabel('Count')
    plt.title('Sentiment Analysis of Comments')
    plt.ylim(0, max(counts) + 1)

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    return img_str

def plot_pie_chart(sentiments_data):
    sentiment_counts = Counter(sentiments_data)

    colors = ['red', 'green', 'yellow']

    labels = sentiment_counts.keys()
    counts = sentiment_counts.values()

    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title('Sentiment Distribution')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    return img_str

def generate_wordcloud(comments):
    comments_text = ' '.join(comments)

    wordcloud = WordCloud(width=800, height=400).generate(comments_text)

    img_buffer = BytesIO()
    wordcloud.to_image().save(img_buffer, format="PNG")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
    return img_str

def start_sentiment_analysis_distilbert(query):
    try:
        comments_max = 750
        limit = 15
        comments = []

        existing_query = Query_data.objects.filter(query_name=query).first()

        if existing_query and existing_query.get_comments():
            comments = existing_query.get_comments()
            print(query + ' data fetched from the database')
        else:
            for submission in reddit.subreddit("all").search(query, limit=limit):
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    max_comment_length = 120
                    if len(comment.body) > max_comment_length:
                        continue
                    comments.append(comment.body)
                    if len(comments) >= comments_max:
                        break

            if not existing_query:
                query_instance = Query_data(query_name=query)
                query_instance.save_comments(comments)
                print(query + ' data saved to the database')
        
        sentiments, scores, positive_comments, negative_comments, neutral_comments = analyze_sentiment(comments)
        average_score = calculate_total_average(scores)
        sentiments_plot = plot_sentiments(sentiments)
        piechart = plot_pie_chart(sentiments)
        comments_wordcloud = generate_wordcloud(comments)
        
    except praw.exceptions.PRAWException as reddit_exception:
        print('Reddit API error:', str(reddit_exception))
        return None, None, None, None, None, None

    except Exception as e:
        print('Error:', str(e))
        return None, None, None, None, None, None

    return average_score, positive_comments, negative_comments, sentiments_plot, piechart, comments_wordcloud

