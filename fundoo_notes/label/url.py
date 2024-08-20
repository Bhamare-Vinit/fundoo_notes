
from django.urls import path
from .views import LabelView

urlpatterns = [
    path('labels/', LabelView.as_view(), name='label-list-create'),
    path('labels/<int:pk>/', LabelView.as_view(), name='label-detail'),
]