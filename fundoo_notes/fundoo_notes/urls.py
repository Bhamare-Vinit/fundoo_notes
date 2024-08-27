'''
@Author: Vinit Gorakhnath Bhamare
@Date: 2024-08-16 13:58:30
@Last Modified by: Vinit Gorakhnath Bhamare
@Last Modified time: 2024-08-26 18:00:30
@Title : Fundoo Notes Project URL
'''

from django.contrib import admin
from django.urls import path, include
import user.views as views
...
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="Fundoo Notes API",
      default_version='v1',
      description="fundoo notes api by vinit bhamare",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@vinit.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("admin/", admin.site.urls),
    
    # path('verify-token/<str:token>/', views.verify_registered_user),
    path('notes/', include('notes.urls')),
    path('user/', include('user.urls',)),
    path('label/', include('label.url')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
