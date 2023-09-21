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