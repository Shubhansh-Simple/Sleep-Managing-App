from django.urls import path
from .views import hello_function, SleepCreateView

urlpatterns = [
    path('', hello_function , name='hello'),
    path('sleep/new/', SleepCreateView.as_view() , name='sleep_new' ),
]
