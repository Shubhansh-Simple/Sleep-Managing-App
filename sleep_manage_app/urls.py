from django.urls import path
from .views import SleepCreateView,SleepUpdateView,SleepDetailView,SleepListView

urlpatterns = [
    path('sleep/'              , SleepListView.as_view() ,   name='sleep_list'    ),
    path('sleep/new/'          , SleepCreateView.as_view() , name='sleep_new'    ),
    path('sleep/<int:pk>/'     , SleepDetailView.as_view() , name='sleep_detail' ),
    path('sleep/<int:pk>/edit/', SleepUpdateView.as_view() , name='sleep_edit'   ),
]
