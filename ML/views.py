from django.shortcuts import render, redirect
from .VADER import start_sentiment_analysis_VADER 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .Textblob import collect_data, start_sentiment_analysis_TB
from django.template.loader import render_to_string
from django.conf import settings

def landing(request):
    return render (request, 'templ/landing.html')


@login_required(login_url='login')
def home(request):
    
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        analysis_method = request.POST.get('analysis_method')

        # Redirect to the corresponding method view based on the selected_method
        if analysis_method == 'method1':
            return redirect('textblob_view', keyword=keyword)
        elif analysis_method == 'method2':
            return redirect('vader_view', keyword=keyword)

    return render (request, 'templ/index.html')


# @login_required(login_url='login')
# def textblob_view(request, keyword):
#     sentiments_data, comments_wordcloud = start_sentiment_analysis_TextBlob(keyword)
    
#     if sentiments_data is not None:
#         avg_sentiment_score, img_str1, img_str2, top_pos_comments, top_neg_comments = sentiments_data

#         context = {
#             'keyword': keyword,
#             'analysis_method': 'TextBlob',
#             'chart1type': 'dist',
#             'avg_sentiment_score': avg_sentiment_score,
#             'hist_chart_filename': img_str1,
#             'sentiments_chart_heatmap': img_str2,
#             'top_neg_comments': top_neg_comments,
#             'top_pos_comments': top_pos_comments,
#             'comments_wordcloud': comments_wordcloud,
#         }
#     else:
#         context = {
#             'keyword': keyword,
#             'analysis_method': 'TextBlob',
#             'chart1type': '',
#             'avg_sentiment_score': '',
#             'hist_chart_filename': '',
#             'sentiments_chart_heatmap': '',
#             'top_pos_comments': '',
#             'top_neg_comments': '',
#             'comments_wordcloud': '',
#         }

#     return render(request, 'templ/result_page.html', context)

from django.shortcuts import render, redirect

@login_required(login_url='login')
def textblob_view(request, keyword):
    context = {}
    try:
        data = collect_data(keyword)

        if data is not None:
            dist_img, avg_topComments_wordclouds = start_sentiment_analysis_TB(data)
            avg_polarity, top_positive, top_negative, img_str_positive, img_str_negative = avg_topComments_wordclouds

            context = {
                'keyword': keyword,
                'analysis_method': 'TextBlob',
                'chart1type': 'dist',
                'avg_sentiment_score': avg_polarity,
                'hist_chart_filename': dist_img,
                'top_neg_comments': top_negative,
                'top_pos_comments': top_positive,
                'comments_wordcloud': img_str_positive,
                'neg_comments_wordcloud': img_str_negative,
            }
        else:
            context = {
                'keyword': keyword,
                'analysis_method': 'TextBlob',
                'chart1type': '',
                'avg_sentiment_score': '',
                'hist_chart_filename': '',
                'top_pos_comments': '',
                'top_neg_comments': '',
                'comments_wordcloud': '',
                'neg_comments_wordcloud': '',
            }

    except Exception as e:
        # Log the error for further investigation
        print(f"An error occurred: {str(e)}")
        # Redirect to the landing page in case of an error
        return redirect('landing')

    return render(request, 'templ/result_page.html', context)


@login_required(login_url='login')
def vader_view(request, keyword):
    context = {}
    try:
        data = collect_data(keyword)

        if data is not None:
            dist_img, avg_topComments_wordclouds = start_sentiment_analysis_VADER(data)
            avg_polarity, top_positive, top_negative, img_str_positive, img_str_negative = avg_topComments_wordclouds

            context = {
                'keyword': keyword,
                'analysis_method': 'VADER',
                'chart1type': 'dist',
                'avg_sentiment_score': avg_polarity,
                'hist_chart_filename': dist_img,
                'top_neg_comments': top_negative,
                'top_pos_comments': top_positive,
                'comments_wordcloud': img_str_positive,
                'neg_comments_wordcloud': img_str_negative,
            }
        else:
            context = {
                'keyword': keyword,
                'analysis_method': 'VADER',
                'chart1type': '',
                'avg_sentiment_score': '',
                'hist_chart_filename': '',
                'top_pos_comments': '',
                'top_neg_comments': '',
                'comments_wordcloud': '',
                'neg_comments_wordcloud': '',
            }

    except Exception as e:
        # Log the error for further investigation
        print(f"An error occurred: {str(e)}")
        # Redirect to the landing page in case of an error
        return redirect('landing')

    return render(request, 'templ/result_page.html', context)


@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('topic')
        message = request.POST.get('message')
        user_email = request.user.email
        username = request.user.username
        email_from = settings.EMAIL_HOST_USER
        email_to = settings.EMAIL_CONTACT

        try:
            # Send the email
            send_mail(
                'New Message from {}'.format(username),
                '',  # Leave the body empty, as we'll use the HTML template
                email_from,
                [email_to],
                html_message=render_to_string('auth/contact_email.html', {
                    'subject': subject,
                    'message': message,
                    'username': username,
                    'user_email': user_email,
                })
            )

            messages.success(request, 'Message sent successfully')
        except Exception as e:
            messages.error(request, f'Failed to send message. Error: {e}')

        return render(request, 'templ/contact.html')

    return render(request, 'templ/contact.html')



@login_required(login_url='login')
def donate(request):
    return render(request, 'templ/donate.html')

