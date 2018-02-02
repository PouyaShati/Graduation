from django.urls import path

from . import views

urlpatterns = [
    path('studentDetail/<int:question_id>/', views.student_detail, name='student detail'),
    path('processBlueprint/<int:question_id>/', views.process_blueprint_detail, name='process blueprint detail'),
]