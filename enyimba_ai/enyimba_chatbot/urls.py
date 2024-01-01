# Enyimba AI, Inc Proprietary Software License

# Copyright (c) 2023, Chukwuma Chukwuma. All rights reserved.

from django.urls import path
from . import views

urlpatterns = [
    path('process-query/', views.chatbot_response, name='process_query'),
    # ... any other URL patterns ...
]
