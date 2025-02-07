from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include(router.urls)),
    path('profile/', views.profile, name='profile'),
    path('add_question/', views.add_question, name='add_question'),
    path('course/<int:course_id>/', views.course_subjects, name='course_subjects'),
    path('subject/<int:subject_id>/questions/', views.subject_questions, name='subject_questions'),
    path('quiz/<int:subject_id>/question/', views.quiz_question, name='quiz_question'),
    path('quiz/<int:subject_id>/submit/<int:question_id>/', views.submit_answer, name='submit_answer'),
]
