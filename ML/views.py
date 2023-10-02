from django.shortcuts import render
from .Textblob_sentiment import start_sentiment_analysis_TextBlob
from .Bert_sentiment import start_sentiment_analysis_BERT
from .VADER_sentiments import start_sentiment_analysis_VADER
from .RoBERTa_sentiment import start_sentiment_analysis_RoBERTa
from django.http import HttpResponse

def index(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        analysis_method = request.POST.get('analysis_method')
        
        if analysis_method == "TextBlob":
            sentiments_data, comments_wordcloud = start_sentiment_analysis_TextBlob(keyword)
        elif analysis_method == "VADER":
            sentiments_data, comments_wordcloud = start_sentiment_analysis_VADER(keyword)
        elif analysis_method == "BERT" or analysis_method == "RoBERTa":
            if analysis_method == "BERT":
                sentiments_bert_plot, comments_wordcloud = start_sentiment_analysis_BERT(keyword)
            else:
                sentiments_bert_plot, comments_wordcloud = start_sentiment_analysis_RoBERTa(keyword)
            
            if sentiments_bert_plot is not None:
                context = {
                    'keyword': keyword,
                    'analysis_method': analysis_method,
                    'sentiments_bert_plot': sentiments_bert_plot,
                    'comments_wordcloud': comments_wordcloud,
                }
            else:
                context = {
                    'keyword': keyword,
                    'analysis_method': '',
                    'sentiments_bert_plot': '',
                    'comments_wordcloud': '',
                }
            
            return render(request, 'ml_templ/bert_result.html', context)
        else:
            return HttpResponse("Analysis Method Invalid")

        if sentiments_data is not None:
            avg_sentiment_score, img_str1, img_str2, top_pos_comments, top_neg_comments = sentiments_data

            context = {
                'keyword': keyword,
                'analysis_method': analysis_method,
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
                'analysis_method': analysis_method,
                'avg_sentiment_score': '',
                'hist_chart_filename': '',
                'sentiments_chart_heatmap': '',
                'top_pos_comments': '',
                'top_neg_comments': '',
                'comments_wordcloud': '',
            }

        return render(request, 'ml_templ/result_page.html', context)

    return render(request, 'ml_templ/index.html')

