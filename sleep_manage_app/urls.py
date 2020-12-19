from django.urls import path
from .views import SleepCreateView

urlpatterns = [
    path('sleep/new/', SleepCreateView.as_view() , name='sleep_new' ),
]
