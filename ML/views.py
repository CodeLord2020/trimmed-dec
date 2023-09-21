from django.shortcuts import render
from .Sentiment import start_sentiment_analysis_VADER

# Create your views here.


def index(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        sentiments_data, comments_wordcloud  = start_sentiment_analysis_VADER(keyword)
        avg_vader_score, avg_textblob_score, img_str1, img_str2 = sentiments_data
        context = {
        'keyword':keyword,
        'avg_vader_score': avg_vader_score,
        'avg_textblob_score': avg_textblob_score,
        'vader_chart_filename': img_str1,
        'textblob_chart_filename': img_str2,
        'comments_wordcloud': comments_wordcloud,  # You can pass this as well
    }
        return render(request, 'ml_templ/result_page.html', context)
    
    return render(request, 'ml_templ/index.html')
