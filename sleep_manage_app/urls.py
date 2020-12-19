from django.urls import path
from .views import SleepCreateView,SleepUpdateView

urlpatterns = [
    path('sleep/new/'          , SleepCreateView.as_view() , name='sleep_new' ),
    path('sleep/<int:pk>/edit/', SleepUpdateView.as_view() , name='sleep_edit' ),
]
