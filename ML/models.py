from typing import Collection, Optional
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

from django.db import models

# Create your models here.

# Create your models here.
class SentimentModel(models.Model):
    owner = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    keyword = models.CharField(max_length = 100)

    query_start_date = models.DateField(default=(timezone.now() - timezone.timedelta(days=365)).date())
    query_end_date = models.DateField(default=timezone.now)

    def _str_(self):
        return self.keyword



from django.db import models

class Query_data(models.Model):
    query_name = models.CharField(max_length=255, unique=True)
    comments = models.TextField()  
    date_added = models.DateTimeField(auto_now_add=True)

    def save_comments(self, comments_list):
        # Save a list of comments as a serialized string
        self.comments = ','.join(comments_list)
        self.save()

    def get_comments(self):
        # Retrieve comments as a list from the serialized string
        return self.comments.split(',')

    def __str__(self):
        return self.query_name
