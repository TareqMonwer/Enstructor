from django.urls import path
from . import views


urlpatterns = [
    path('register/',
         views.StudentRegistration.as_view(),
         name='student_registration'),
    path('enroll-course/',
         views.StudentEnrollCourseView.as_view(),
         name='student_enroll_course'),
]
