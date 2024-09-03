
from django.urls import path
from .views import LabelView,LabelView2,RawLabelView,RawLabelView2

urlpatterns = [
    path('labels/', LabelView.as_view(), name='label-list-create'),
    path('labels/<int:pk>/', LabelView2.as_view(), name='label-detail'),
    path('rawlabels/', RawLabelView.as_view(), name='rawlabel-list'),
    path('rawlabels/<int:pk>/', RawLabelView2.as_view(), name='rawlabel-detail'),
]