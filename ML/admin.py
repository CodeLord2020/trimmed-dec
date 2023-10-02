from django.contrib import admin

# Register your models here.
from .models import SentimentModel, Query_data
# Register your models here.


admin.site.register(SentimentModel)
admin.site.register(Query_data)