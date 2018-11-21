from django.urls import path

from employee import views

urlpatterns = [
    path('employees', views.EmployeeList.as_view()),
    path('employees/<int:pk>/', views.EmployeeDetails.as_view()),
]