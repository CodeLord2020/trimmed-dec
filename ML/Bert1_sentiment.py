#BERT Model= "nlptown/bert-base-multilingual-uncased-sentiment"

import os
from environs import Env
import praw
from io import BytesIO
import base64
from .models import Query_data
from transformers import pipeline
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud


# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline(model="nlptown/bert-base-multilingual-uncased-sentiment")

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('Marvel_Client_ID'),
    client_secret=os.getenv('Marvel_Client_Secret'),
    user_agent=os.getenv('Marvel_user_agent'),
)

# def analyze_sentiment_with_bert(comments):
#     sentiments = []
#     scores = []

#     for comment in comments:
#         # Analyze sentiment for each comment
#         result = sentiment_pipeline(comment)
#         sentiment_label = result[0]['label']
#         sentiments.append(sentiment_label)
#         scores.append(result[0]['score'])

#     return sentiments, scores

def analyze_sentiment_with_bert(comments):
    sentiments = []
    scores = []
    five_star_comments = []  # List to store 5-star comments
    one_star_comments = []   # List to store 1-star comments

    for comment in comments:
        # Analyze sentiment for each comment
        result = sentiment_pipeline(comment)
        sentiment_label = result[0]['label']
        sentiments.append(sentiment_label)
        scores.append(result[0]['score'])

        if sentiment_label == '5 stars' and len(five_star_comments) < 10:
            five_star_comments.append(comment)
        elif sentiment_label == '1 star' and len(one_star_comments) < 10:
            one_star_comments.append(comment)

        if len(five_star_comments) >= 10 and len(one_star_comments) >= 10:
            break

    return sentiments, scores, five_star_comments, one_star_comments


# Calculate the total average sentiment score
def calculate_total_average(scores_bert):
    total_score = sum(scores_bert)
    total_count = len(scores_bert)

    if total_count > 0:
        total_average = total_score / total_count
        return total_average

    return None  # Handle the case when there are no scores

def plot_sentiments(sentiments_data_bert):
    # Count the occurrences of each sentiment label
    sentiment_counts = Counter(sentiments_data_bert)

    # Define color mapping for sentiment labels
    color_mapping = {

        '1 star': 'red',
        '2 stars': 'orange',
        '3 stars': 'yellow',
        '4 stars': 'blue',
        '5 stars': 'green',

    }

    # Extract labels and counts
    labels = sentiment_counts.keys()
    counts = sentiment_counts.values()

    # Assign colors based on sentiment labels
    colors = [color_mapping.get(label, 'green') for label in labels]

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color=colors)
    plt.xlabel('Sentiment Labels')
    plt.ylabel('Count')
    plt.title('Sentiment Analysis of Comments')
    plt.ylim(0, max(counts) + 1)  # Set the y-axis range based on the maximum count

    # Convert the plot image to a base64-encoded string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    return img_str

import matplotlib.pyplot as plt

def plot_pie_chart(sentiments_data_bert):
    # Count the occurrences of each sentiment label
    sentiment_counts = Counter(sentiments_data_bert)

    # Define colors for each sentiment label
    colors = ['yellow', 'green', 'red', 'lightgreen', 'orange']

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(sentiment_counts.values(), labels=sentiment_counts.keys(), autopct='%1.1f%%', colors=colors, startangle=140)
    plt.title('Sentiment Distribution')

    # Convert the plot image to a base64-encoded string
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    return img_str


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




def start_sentiment_analysis_BERT1(query):
    try:
        comments_max = 50
        limit = 5
        comments = []

        # Check if there are existing comments related to 'query' in the database.
        existing_query = Query_data.objects.filter(query_name=query).first()

        if existing_query and existing_query.get_comments():
            # Use existing comments from the database.
            comments = existing_query.get_comments()
            print(query + ' data fetched from the database')
        else:
            for submission in reddit.subreddit("all").search(query, limit=limit):
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                    max_comment_length = 120  # Adjust as needed
                    if len(comment.body) > max_comment_length:
                        # Skip this comment
                        continue
                    comments.append(comment.body)
                    if len(comments) >= comments_max:
                        break

            # Save the newly fetched comments to the database.
            if not existing_query:
                # If the query doesn't exist in the database, create a new instance and save comments.
                query_instance = Query_data(query_name=query)
                query_instance.save_comments(comments)
                print(query + ' data saved to database')
        
        sentiments_data_bert, scores_bert, five_star_comments, one_star_comments = analyze_sentiment_with_bert(comments)
        average_score = calculate_total_average(scores_bert)
        piechart = plot_pie_chart(sentiments_data_bert)
        sentiments_bert_plot = plot_sentiments(sentiments_data_bert)
        comments_wordcloud = generate_wordcloud(comments)
    except praw.exceptions.PRAWException as reddit_exception:
        print('Reddit API error:', str(reddit_exception))
        return None, None, None

    except Exception as e:
        print('Error:', str(e))
        return None, None, None

    return average_score, five_star_comments, one_star_comments, sentiments_bert_plot, piechart, comments_wordcloud

