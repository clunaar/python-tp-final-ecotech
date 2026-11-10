from django.urls import path

from sustentabilidad import views

urlpatterns = [
    path('', views.vista_panel_sustentabilidad, name="Panel"),
]
