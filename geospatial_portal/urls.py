from django.urls import path
from . import views

app_name = 'geospatial_portal'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/nodes/', views.api_map_nodes, name='api_map_nodes'),
]

