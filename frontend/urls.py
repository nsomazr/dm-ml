from django.urls import path
from .views import FrontendAPIView
from django.conf import settings
from django.conf.urls.static import static
app_name = "frontend"  

urlpatterns = [
                path('', FrontendAPIView.index, name = 'index'),
                # path('home/api/', FrontendAPIView.as_view(), name="home-api")
                ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)