from django.urls import path
from .views import deploy_container, get_container_logs

urlpatterns = [
    path('deploy/', deploy_container, name='deploy-container'),
    path('logs/<str:container_id>/', get_container_logs, name='get-container-logs'),
]
