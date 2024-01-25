import os
import praw
from io import BytesIO
import base64
from .models import Query_data
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Download VADER lexicon
# import nltk
# nltk.download('vader_lexicon')

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id=os.getenv('Client_ID'),
    client_secret=os.getenv('Client_Secret'),
    user_agent=os.getenv('user_agent'),
)

def avgPolarity_topComments_wordclouds(comments):
    # Create a list to store tuples of (comment, compound score)
    comment_scores_list = []

    # Initialize the VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Calculate compound scores for each comment
    for comment in comments:
        scores = sia.polarity_scores(comment)
        compound_score = scores['compound']
        comment_scores_list.append((comment, compound_score))

    # Sort comments based on compound scores
    sorted_comments = sorted(comment_scores_list, key=lambda x: x[1], reverse=True)

    # Extract top 10 positive and negative comments
    top_positive = [comment for comment, _ in sorted_comments[:10]]
    top_negative = [comment for comment, _ in sorted_comments[-10:]]

    wc_top_positive = [comment for comment, _ in sorted_comments[:50]]
    wc_top_negative = [comment for comment, _ in sorted_comments[-50:]]

    # Generate WordCloud for positive comments
    wordcloud_positive = WordCloud(width=800, height=400, background_color='black').generate(' '.join(wc_top_positive))

    # Generate WordCloud for negative comments
    wordcloud_negative = WordCloud(width=800, height=400, background_color='black').generate(' '.join(wc_top_negative))

    # Calculate average compound score
    avg_score = sum(score for _, score in comment_scores_list) / len(comment_scores_list)

    # Save images to base64 strings
    img_buffer_positive = BytesIO()
    wordcloud_positive.to_image().save(img_buffer_positive, format="PNG")
    img_str_positive = base64.b64encode(img_buffer_positive.getvalue()).decode("utf-8")

    img_buffer_negative = BytesIO()
    wordcloud_negative.to_image().save(img_buffer_negative, format="PNG")
    img_str_negative = base64.b64encode(img_buffer_negative.getvalue()).decode("utf-8")

    return avg_score, top_positive, top_negative, img_str_positive, img_str_negative

def visualize_compoundScore_distribution(comments):
    # Calculate compound scores for each comment
    compound_scores = [SentimentIntensityAnalyzer().polarity_scores(comment)['compound'] for comment in comments]

    # Create a histogram
    plt.hist(compound_scores, bins=20, edgecolor='black')
    plt.title('Compound Score Distribution')
    plt.xlabel('Compound Score')
    plt.ylabel('Frequency')

    # Save the plot to a BytesIO buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format="png")
    img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    # Close the plot to free up resources
    plt.close()
    return img_str

def start_sentiment_analysis_VADER(comments):
    avg_topComments_wordclouds = avgPolarity_topComments_wordclouds(comments)
    dist_img = visualize_compoundScore_distribution(comments)
    return dist_img, avg_topComments_wordclouds
