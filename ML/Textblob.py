import os
from environs import Env
env = Env()
env.read_env()
import praw
from io import BytesIO
import base64
from .models import Query_data
import seaborn as sns

from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO


# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id = os.getenv('Client_ID'),
    client_secret = os.getenv('Client_Secret'),
    user_agent =  os.getenv('user_agent'),

    )
#############################################             Data Collection          ###########################################################################
def collect_data(query):
    try:
        reddit = praw.Reddit(client_id='your_client_id',
                             client_secret='your_client_secret',
                             user_agent='your_user_agent')

        comments_max = 750
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

        return comments

    except praw.exceptions.RedditAPIException as reddit_error:
        # Handle Reddit API-specific errors
        print(f"Reddit API Error for query {query}: {reddit_error}")
        return []

    except Exception as e:
        # Handle other general exceptions
        print(f"Error in collecting data for query {query}: {str(e)}")
        return []

def avgPolarity_topComments_wordclouds(comments):
    # Create a list to store tuples of (comment, polarity)
    comment_polarity_list = []

    # Calculate polarity for each comment
    for comment in comments:
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity
        comment_polarity_list.append((comment, polarity))

    # Sort comments based on polarity
    sorted_comments = sorted(comment_polarity_list, key=lambda x: x[1], reverse=True)

    # Extract top 10 positive and negative comments
    top_positive = [comment for comment, polarity in sorted_comments[:10]]
    top_negative = [comment for comment, polarity in sorted_comments[-10:]]

    wc_top_positive = [comment for comment, polarity in sorted_comments[:50]]
    wc_top_negative = [comment for comment, polarity in sorted_comments[-50:]]


    # Generate WordCloud for positive comments
    wordcloud_positive = WordCloud(width=800, height=400, background_color='black').generate(' '.join(wc_top_positive))

    # Generate WordCloud for negative comments
    wordcloud_negative = WordCloud(width=800, height=400, background_color='black').generate(' '.join(wc_top_negative))

    # Calculate average polarity score
    avg_polarity = sum(polarity for _, polarity in comment_polarity_list) / len(comment_polarity_list)

    # Display the word clouds
    # plt.figure(figsize=(12, 6))

    # plt.subplot(1, 2, 1)
    # plt.imshow(wordcloud_positive, interpolation='bilinear')
    # plt.axis('off')
    # plt.title('Word Cloud for Positive Comments')

    # plt.subplot(1, 2, 2)
    # plt.imshow(wordcloud_negative, interpolation='bilinear')
    # plt.axis('off')
    # plt.title('Word Cloud for Negative Comments')

    # Save images to base64 strings
    img_buffer_positive = BytesIO()
    wordcloud_positive.to_image().save(img_buffer_positive, format="PNG")
    # plt.savefig(img_buffer_positive, format="png")
    img_str_positive = base64.b64encode(img_buffer_positive.getvalue()).decode("utf-8")

    img_buffer_negative = BytesIO()
    wordcloud_negative.to_image().save(img_buffer_negative, format="PNG")
    # plt.savefig(img_buffer_negative, format="png")
    img_str_negative = base64.b64encode(img_buffer_negative.getvalue()).decode("utf-8")

    return avg_polarity, top_positive, top_negative, img_str_positive, img_str_negative

# def avgPolarity_topComments(comments):
#     try:
#         # Create a list to store tuples of (comment, polarity)
#         comment_polarity_list = []

#         # Calculate polarity for each comment
#         for comment in comments:
#             blob = TextBlob(comment)
#             polarity = blob.sentiment.polarity
#             comment_polarity_list.append((comment, polarity))

#         # Sort comments based on polarity
#         sorted_comments = sorted(comment_polarity_list, key=lambda x: x[1], reverse=True)

#         # Extract top 10 positive and negative comments
#         top_positive = sorted_comments[:10]
#         top_negative = sorted_comments[-10:]

#         # Calculate average polarity score
#         avg_polarity = sum(polarity for _, polarity in comment_polarity_list) / len(comment_polarity_list)

#         return top_positive, top_negative, avg_polarity

#     except Exception as e:
#         # Handle any exception that might occur
#         print(f"An error occurred: {e}")
#         return None

def visualize_polarity_distribution(comments):
    # Calculate polarity for each comment
    polarities = [TextBlob(comment).sentiment.polarity for comment in comments]

    # Create a histogram
    plt.hist(polarities, bins=20, edgecolor='black')
    plt.title('Polarity Distribution')
    plt.xlabel('Polarity')
    plt.ylabel('Frequency')

    # Save the plot to a BytesIO buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    # Close the plot to free up resources
    plt.close()
    return img_str

def start_sentiment_analysis_TB(comments):
    avg_topComments_wordclouds = avgPolarity_topComments_wordclouds(comments)
    dist_img = visualize_polarity_distribution(comments)
    return dist_img, avg_topComments_wordclouds

