from django.urls import path
from .views import InferenceAPIView, DataInferenceAPIView
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "backend"  

urlpatterns = [
                path('inference/api/', DataInferenceAPIView.as_view(), name="inference-api"),
                path('results/api', InferenceAPIView.as_view(), name="results-api"),
                path('predict/', views.prediction, name="predict")
                 ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)