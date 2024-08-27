
from django.urls import path
from .views import LabelView,LabelView2

urlpatterns = [
    path('labels/', LabelView.as_view(), name='label-list-create'),
    path('labels/<int:pk>/', LabelView2.as_view(), name='label-detail'),
]