# academia/urls.py
from django.urls import path
from . import views

app_name = 'academia'  # Namespace para las URLs de esta aplicación

urlpatterns = [
    path('', views.index, name='index'),  # URL para la página principal de academia

    # URLs para Teacher
    path('teachers/', views.TeacherListView.as_view(), name='teacher-list'),
    path('teachers/new/', views.TeacherCreateView.as_view(), name='teacher-create'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
    path('teachers/<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='teacher-update'),
    path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher-delete'),

    # URLs para Student
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/new/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student-update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),

    # URLs para Subject
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/new/', views.SubjectCreateView.as_view(), name='subject-create'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('subjects/<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='subject-update'),
    path('subjects/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject-delete'),

    # URLs para Course
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),

    # URLs para Enrollment
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/new/', views.EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('enrollments/<int:pk>/edit/', views.EnrollmentUpdateView.as_view(), name='enrollment-update'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment-delete'),

    # URLs para AttendanceLog
    path('attendancelogs/take/', views.TakeAttendanceView.as_view(), name='take-attendance'), # Nueva URL para tomar asistencia masiva
    path('attendancelogs/', views.AttendanceLogListView.as_view(), name='attendancelog-list'),
    path('attendancelogs/new/', views.AttendanceLogCreateView.as_view(), name='attendancelog-create'),
    path('attendancelogs/<int:pk>/', views.AttendanceLogDetailView.as_view(), name='attendancelog-detail'),
    path('attendancelogs/<int:pk>/edit/', views.AttendanceLogUpdateView.as_view(), name='attendancelog-update'),
    path('attendancelogs/<int:pk>/delete/', views.AttendanceLogDeleteView.as_view(), name='attendancelog-delete'),

    # URLs para Grade
    path('grades/take/', views.TakeGradesView.as_view(), name='take-grades'),
    path('grades/', views.GradeListView.as_view(), name='grade-list'),
    path('grades/new/', views.GradeCreateView.as_view(), name='grade-create'),
    path('grades/<int:pk>/', views.GradeDetailView.as_view(), name='grade-detail'),
    path('grades/<int:pk>/edit/', views.GradeUpdateView.as_view(), name='grade-update'),
    path('grades/<int:pk>/delete/', views.GradeDeleteView.as_view(), name='grade-delete'),
    
    # --- NUEVA URL PARA CIERRE DE PERIODO ---
    path('courses/close-period/', views.ClosePeriodView.as_view(), name='close-period'),
]
