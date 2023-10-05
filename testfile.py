# from transformers import BertTokenizer, BertForSequenceClassification, pipeline

# # Initialize BERT model and tokenizer
# tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
# model = BertForSequenceClassification.from_pretrained("bert-base-uncased")
# nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# results = []

# # Analyze sentiment for a comment

# comment1 = "This is a positive comment."
# result = nlp(comment1)
# results.append(result)

# comment2 = "This is a negative comment."
# result = nlp(comment2)
# results.append(result)

# comment3 = "This is a neither good nor bad."
# result = nlp(comment3)
# results.append(result)

# comment4 = "This is a very neutral comment."
# result = nlp(comment4)
# results.append(result)
# print(results)

# [{'label': 'POSITIVE', 'score': 0.9998656511306763}, {'label': 'NEGATIVE', 'score': 0.9991129040718079}] [{'label': 'POS', 'score': 0.9916695356369019}, {'label': 'NEG', 'score': 0.9806600213050842}]
# (finalyearenv) macsauce-zen@macsaucezen-HP-630-Notebook-PC:~/Documents/FinalYear/Base$ python testfile.py 
# Downloading (…)lve/main/config.json: 100%|█████| 953/953 [00:00<00:00, 1.31MB/s]
# Downloading pytorch_model.bin: 100%|█████████| 669M/669M [03:07<00:00, 3.58MB/s]
# Downloading (…)okenizer_config.json: 100%|███| 39.0/39.0 [00:00<00:00, 38.1kB/s]
# Downloading (…)solve/main/vocab.txt: 100%|████| 872k/872k [00:00<00:00, 988kB/s]
# Downloading (…)cial_tokens_map.json: 100%|██████| 112/112 [00:00<00:00, 223kB/s]
# [{'label': '5 stars', 'score': 0.8546808362007141}, {'label': '1 star', 'score': 0.6346078515052795}] [{'label': 'POS', 'score': 0.9916695356369019}, {'label': 'NEG', 'score': 0.9806600213050842}]

# from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
# # Initialize GPT-2 model and tokenizer
# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# model = GPT2LMHeadModel.from_pretrained("gpt2")
# nlp = pipeline("text-generation", model=model, tokenizer=tokenizer)
# # Input text
# input_text = "Manchester United"
# # Generate text using GPT-2
# generated_text = nlp(input_text, max_length=100, num_return_sequences=1)[0]["generated_text"]
# # Print the generated text



# print(generated_text)

from transformers import pipeline
data = ["I love you", "I hate you"]

sentiment_pipeline = pipeline(model="nlptown/bert-base-multilingual-uncased-sentiment")
result1 = sentiment_pipeline(data)

sentiment_pipeline2 = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment-latest")
result2 = sentiment_pipeline(data)

specific_model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")
result3 = specific_model(data)

print(result1, result2)

from django.views.decorators.cache import cache_page

# @cache_page(60 * 30)  # Cache the view for 30 minutes
# def analyze_sentiment(request, query, method):
#     return perform_sentiment_analysis(query, method)
