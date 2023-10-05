from django.shortcuts import render, redirect
from .Textblob_sentiment import start_sentiment_analysis_TextBlob
from .Bert3_sentiment import start_sentiment_analysis_BERT3
from .Bert1_sentiment import start_sentiment_analysis_BERT1
from .VADER_sentiments import start_sentiment_analysis_VADER
from .RoBERTa1_sentiment import start_sentiment_analysis_RoBERTa1
from django.http import HttpResponse
# from django.views.decorators.cache import cache_page


def home(request):
    
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        analysis_method = request.POST.get('analysis_method')

        # Redirect to the corresponding method view based on the selected_method
        if analysis_method == 'method1':
            return redirect('textblob_view', keyword=keyword)
        elif analysis_method == 'method2':
            return redirect('vader_view', keyword=keyword)
        elif analysis_method == 'method3':
            return redirect('bert1_view', keyword=keyword)
        elif analysis_method == 'method4':
            return redirect('bert3_view', keyword=keyword)
        elif analysis_method == 'method5':
            return redirect('roberta1_view', keyword=keyword)
        elif analysis_method == 'method6':
            return redirect('method6_view', keyword=keyword)

    return render (request, 'templ/index.html')

# @cache_page(60 * 30)
def textblob_view(request, keyword):
    sentiments_data, comments_wordcloud = start_sentiment_analysis_TextBlob(keyword)
    
    if sentiments_data is not None:
        avg_sentiment_score, img_str1, img_str2, top_pos_comments, top_neg_comments = sentiments_data

        context = {
            'keyword': keyword,
            'analysis_method': 'TextBlob',
            'avg_sentiment_score': avg_sentiment_score,
            'hist_chart_filename': img_str1,
            'sentiments_chart_heatmap': img_str2,
            'top_neg_comments': top_neg_comments,
            'top_pos_comments': top_pos_comments,
            'comments_wordcloud': comments_wordcloud,
        }
    else:
        context = {
            'keyword': keyword,
            'analysis_method': 'TextBlob',
            'avg_sentiment_score': '',
            'hist_chart_filename': '',
            'sentiments_chart_heatmap': '',
            'top_pos_comments': '',
            'top_neg_comments': '',
            'comments_wordcloud': '',
        }

    return render(request, 'ml_templ/result_page.html', context)


def vader_view(request, keyword):
    sentiments_data, comments_wordcloud = start_sentiment_analysis_VADER(keyword)
    
    if sentiments_data is not None:
        avg_sentiment_score, img_str1, img_str2, top_pos_comments, top_neg_comments = sentiments_data

        context = {
            'keyword': keyword,
            'analysis_method': 'VADER',
            'avg_sentiment_score': avg_sentiment_score,
            'hist_chart_filename': img_str1,
            'sentiments_chart_heatmap': img_str2,
            'top_neg_comments': top_neg_comments,
            'top_pos_comments': top_pos_comments,
            'comments_wordcloud': comments_wordcloud,
        }
    else:
        context = {
            'keyword': keyword,
            'analysis_method': 'VADER',
            'avg_sentiment_score': '',
            'hist_chart_filename': '',
            'sentiments_chart_heatmap': '',
            'top_pos_comments': '',
            'top_neg_comments': '',
            'comments_wordcloud': '',
        }

    return render(request, 'ml_templ/result_page.html', context)

def bert1_view(request, keyword):
    average_score, sentiments_bert_plot, comments_wordcloud = start_sentiment_analysis_BERT1(keyword)
    
    if sentiments_bert_plot is not None:
        context = {
            'keyword': keyword,
            'analysis_method': 'BERT(nlptown/bert-base-multilingual-uncased-sentiment)',
            'average_score':average_score,
            'sentiments_bert_plot': sentiments_bert_plot,
            'comments_wordcloud': comments_wordcloud,
        }
    else:
        context = {
            
            'keyword': keyword,
            'analysis_method': 'BERT',
            'average_score':'',
            'sentiments_bert_plot': '',
            'comments_wordcloud': '',
        }

    return render(request, 'ml_templ/bert_result.html', context)

def bert3_view(request, keyword):
    average_score, sentiments_bert_plot, comments_wordcloud = start_sentiment_analysis_BERT3(keyword)

    if sentiments_bert_plot is not None:
        context = {
            'keyword': keyword,
            'analysis_method': 'BERT(finiteautomata/bertweet-base-sentiment-analysis)',
            'average_score':average_score,
            'sentiments_bert_plot': sentiments_bert_plot,
            'comments_wordcloud': comments_wordcloud,
        }
    else:
        context = {
            
            'keyword': keyword,
            'analysis_method': 'BERT(finiteautomata/bertweet-base-sentiment-analysis)',
            'average_score':'',
            'sentiments_bert_plot': '',
            'comments_wordcloud': '',
        }

    return render(request, 'ml_templ/bert_result.html', context)


def roberta1_view(request, keyword):
    average_score, sentiments_bert_plot, comments_wordcloud = start_sentiment_analysis_RoBERTa1(keyword)
    
    if sentiments_bert_plot is not None:
        context = {
            'keyword': keyword,
            'analysis_method': 'RoBERTa(cardiffnlp/twitter-roberta-base-sentiment-latest)',
            'average_score':average_score,
            'sentiments_bert_plot': sentiments_bert_plot,
            'comments_wordcloud': comments_wordcloud,
        }
    else:
        context = {
            
            'keyword': keyword,
            'analysis_method': 'RoBERTa(cardiffnlp/twitter-roberta-base-sentiment-latest)',
            'average_score':'',
            'sentiments_bert_plot': '',
            'comments_wordcloud': '',
        }

    return render(request, 'ml_templ/bert_result.html', context)


def contact(request):
    print('contact')
    return render (request, 'templ/contact.html')

