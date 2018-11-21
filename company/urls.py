from django.urls import path

from company import views

urlpatterns = [
    path('companies', views.CompanyList.as_view()),
    path('companies/<int:pk>/', views.CompanyDetails.as_view()),
]