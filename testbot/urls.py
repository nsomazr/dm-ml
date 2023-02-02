from django.urls import path
from .views import TestbotAPIView
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = "testbot"  

urlpatterns = [
                path('', TestbotAPIView.testbot, name = 'testbot'),
                path('letschat/', views.convo, name = 'letschat'),
                path('testbot/api/', TestbotAPIView.as_view(), name="testbot-api")
                ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)