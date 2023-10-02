import os
from environs import Env
env = Env()
env.read_env()

import matplotlib.pyplot as plt
import praw
from io import BytesIO
import base64
from .models import Query_data

from transformers import RobertaTokenizer, RobertaForSequenceClassification, pipeline

# Initialize RoBERTa tokenizer and model
tokenizer = RobertaTokenizer.from_pretrained("roberta-base")
model = RobertaForSequenceClassification.from_pretrained("roberta-base")
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id = os.getenv('Marvel_Client_ID'),
    client_secret = os.getenv('Marvel_Client_Secret'),
    user_agent =  os.getenv('Marvel_user_agent'),
    )

def analyze_sentiment_with_roberta(comments):
    sentiments = []

    for comment in comments:
        # Analyze sentiment for each comment
        result = nlp(comment)
        sentiment_label = result[0]['label']
        sentiments.append(sentiment_label)

    return sentiments

# Replace your existing code with this part
def start_sentiment_analysis_RoBERTa(query):
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
                    comments.append(comment.body)
                    if len(comments) >= comments_max:
                        break

            # Save the newly fetched comments to the database.
            if not existing_query:
                # If the query doesn't exist in the database, create a new instance and save comments.
                query_instance = Query_data(query_name=query)
                query_instance.save_comments(comments)
                print(query + ' data saved to database')

        sentiments_data_roberta = analyze_sentiment_with_roberta(comments)
        #top_comments = get_top_comments(sentiments_data_roberta, comments)
        sentiments_roberta_plot = plot_sentiments(sentiments_data_roberta)
        comments_wordcloud = generate_wordcloud(comments)

    except praw.exceptions.PRAWException as reddit_exception:
        print('Reddit API error:', str(reddit_exception))
        return None, None

    except Exception as e:
        print('Error:', str(e))
        return None, None

    return sentiments_roberta_plot, comments_wordcloud

import matplotlib.pyplot as plt

from collections import Counter
def plot_sentiments(sentiments_data_roberta):
    # Count the occurrences of each sentiment label
    sentiment_counts = Counter(sentiments_data_roberta)

    # Define color mapping for sentiment labels
    color_mapping = {
        'LABEL_1': 'red',    # Negative sentiment
        'LABEL_2': 'yellow', # Neutral sentiment
        'LABEL_3': 'green'   # Positive sentiment
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

