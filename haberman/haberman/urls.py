"""
URL configuration for haberman project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from visualization.views import create_patient, predict_survival, predict_new, predict_kaplan, predict_kaplan2, get_summary

urlpatterns = [
    path('patients/create/', create_patient),
    path('patients/random/', predict_survival),
    path('patients/predict/', predict_new),
    path('patients/kaplan/',predict_kaplan),
    path('patients/kaplan2/', predict_kaplan2),
    path('patients/summary/', get_summary)
]