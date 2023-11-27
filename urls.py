# myapp/urls.py

from django.urls import path
from .multy import slack_command  # multy.py에서 함수 가져오기

urlpatterns = [
    path('slack/command', slack_command, name='slack_command'),
]