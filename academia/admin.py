
from django.contrib import admin
# Register your models here.
from django.utils.translation import gettext_lazy as _ # <--- AÑADE ESTA LÍNEA
from .models import Teacher, Student, Subject, Course, Enrollment, AttendanceLog,Grade
from .models import Grade  # Import the new model
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
     list_display = ('name', 'surname', 'email', 'phone_number', 'user')
     search_fields = ('name', 'surname', 'email', 'user__username')
     ordering = ('surname', 'name')
     raw_id_fields = ('user',) # Facilita la selección de usuarios
 
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
     list_display = ('name', 'surname', 'email', 'phone_number', 'date_of_birth', 'age')
     search_fields = ('name', 'surname', 'email')
     list_filter = ('date_of_birth',)
     ordering = ('surname', 'name')
     readonly_fields = ('age',) # La edad es una propiedad calculada
 
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
     list_display = ('name', 'number_of_lessons')
     search_fields = ('name',)
     ordering = ('name',)
 
class AttendanceLogInline(admin.TabularInline): # O admin.StackedInline
    model = AttendanceLog
    extra = 1 # Número de formularios extra para agregar asistencia
    fields = ('lesson_number', 'lesson_date', 'is_present', 'notes')
    ordering = ('lesson_number',)
    # Podrías añadir validaciones o campos readonly aquí si es necesario
 
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'academic_period', 'day_of_week', 'start_time', 'start_date', 'end_date', 'is_active')
    list_filter = ('academic_period', 'day_of_week', 'teacher', 'subject', 'is_active')
    search_fields = ('subject__name', 'teacher__name', 'teacher__surname', 'academic_period')
    ordering = ('-academic_period', 'subject__name', 'start_date')
    raw_id_fields = ('teacher', 'subject') # Útil si tienes muchos profesores o materias
 
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'status', 'lesson_score', 'exam_score', 'attendance_score_display', 'final_grade_display')
    list_filter = ('course__academic_period', 'course__subject', 'status', 'student')
    search_fields = ('student__name', 'student__surname', 'course__subject__name')
    ordering = ('course__academic_period', 'course__subject__name', 'student__surname')
    readonly_fields = ('attendance_score_display', 'final_grade_display')
    raw_id_fields = ('student', 'course') # Útil para muchos estudiantes o cursos
    inlines = [AttendanceLogInline] # Permite administrar la asistencia directamente desde la inscripción

    def attendance_score_display(self, obj):
        score = obj.attendance_score
        return f"{score:.2f}%" if score is not None else "N/A"
    attendance_score_display.short_description = _("Attendance Score")

    def final_grade_display(self, obj):
        grade = obj.final_grade
        return f"{grade:.2f}" if grade is not None else "N/A"
    final_grade_display.short_description = _("Final Grade")
 
@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('enrollment_student_name', 'enrollment_course_name', 'lesson_number', 'lesson_date', 'is_present')
    list_filter = ('lesson_date', 'is_present', 'enrollment__course__subject', 'enrollment__course__academic_period')
    search_fields = ('enrollment__student__name', 'enrollment__student__surname', 'enrollment__course__subject__name')
    ordering = ('enrollment__course', 'enrollment__student', 'lesson_number')
    list_select_related = ('enrollment__student', 'enrollment__course') # Optimiza queries

    def enrollment_student_name(self, obj):
        return obj.enrollment.student
    enrollment_student_name.short_description = _("Student")
    enrollment_student_name.admin_order_field = 'enrollment__student__surname'
 
 
    def enrollment_course_name(self, obj):
        return obj.enrollment.course
    enrollment_course_name.short_description = _("Course")
    enrollment_course_name.admin_order_field = 'enrollment__course__subject__name'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson_number', 'grade', 'grade_type')
    list_filter = ('grade_type', 'enrollment__course__subject')
    search_fields = ('enrollment__student__surname', 'enrollment__student__name', 'enrollment__course__subject__name')
    ordering = ('enrollment__student__surname', 'enrollment__course__subject__name', 'lesson_number')
    raw_id_fields = ('enrollment',)  # For performance, especially if you have many enrollments
 
 # Si prefieres un registro más simple sin personalización, puedes usar:
 # admin.site.register(Teacher)
 # admin.site.register(Student)
 # admin.site.register(Subject)
 # admin.site.register(Course)
 # admin.site.register(Enrollment)
 # admin.site.register(AttendanceLog)
