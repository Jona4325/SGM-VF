from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _ # Para choices
from decimal import Decimal

# Validator function (similar to the one in cunakids)
def validate_date(value):
    """
    Valida que el valor sea una fecha válida y se pueda formatear.
    """
    try:
        # Intenta formatear para asegurar que es un objeto date válido
        value.strftime('%Y-%m-%d')
    except AttributeError: # Si no es un objeto date
        raise ValidationError(_('Invalid date format. Expected a date object.'))
    except ValueError as e: # Si strftime falla por alguna razón con un objeto date (poco común)
        raise ValidationError(str(e))

class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("user account"),
        help_text=_("Link this teacher profile to a Django user account to allow login.")
    )
    name = models.CharField(_("name"), max_length=128)
    surname = models.CharField(_("surname"), max_length=128)
    email = models.EmailField(_("email"), max_length=254, unique=True, null=True, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = _("teacher")
        verbose_name_plural = _("teachers")
        ordering = ['surname', 'name']

class Student(models.Model):
    name = models.CharField(_("name"), max_length=128)
    surname = models.CharField(_("surname"), max_length=128)
    email = models.EmailField(_("email"), max_length=254, unique=True, null=True, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(
        _("date of birth"),
        null=True, blank=True,
        validators=[validate_date],
        help_text=_("Format: YYYY-MM-DD")
    )

    def __str__(self):
        return f"{self.name} {self.surname}"

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - \
               ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    class Meta:
        verbose_name = _("student")
        verbose_name_plural = _("students")
        ordering = ['surname', 'name']
        unique_together = [['name', 'surname']]

class Subject(models.Model):
    name = models.CharField(_("subject name"), max_length=128, unique=True)
    description = models.TextField(_("description"), blank=True)
    number_of_lessons = models.PositiveIntegerField(
        _("number of lessons"),
        default=10,
        help_text=_("Default number of lessons for courses of this subject.")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")
        ordering = ['name']

class Course(models.Model):
    class DayOfWeek(models.TextChoices):
        SUNDAY = 'SUN', _('Sunday')
        MONDAY = 'MON', _('Monday')
        TUESDAY = 'TUE', _('Tuesday')
        WEDNESDAY = 'WED', _('Wednesday')
        THURSDAY = 'THU', _('Thursday')
        FRIDAY = 'FRI', _('Friday')
        SATURDAY = 'SAT', _('Saturday')

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, verbose_name=_("subject"))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, verbose_name=_("teacher"))
    academic_period = models.CharField(
        _("academic period"),
        max_length=50,
        help_text=_("E.g., '2025 - Ciclo 1', '2025 - C1'")
    )
    day_of_week = models.CharField(
        _("day of week"),
        max_length=3,
        choices=DayOfWeek.choices,
        help_text=_("Day of the week the course is held.")
    )
    start_time = models.TimeField(_("start time"), help_text=_("Format: HH:MM"))
    start_date = models.DateField(_("start date"), validators=[validate_date], help_text=_("Format: YYYY-MM-DD"))
    end_date = models.DateField(
        _("end date"),
        validators=[validate_date],
        blank=True, null=True,
        help_text=_("Calculated automatically if not provided, based on start date and number of lessons.")
    )
    is_active = models.BooleanField(_("is active"), default=True, help_text=_("Is this course currently active?"))

    def __str__(self):
        return f"{self.subject.name} ({self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')}) - {self.academic_period}"

    def save(self, *args, **kwargs):
        if not self.end_date and self.start_date and self.subject:
            # Assumes one lesson per week
            self.end_date = self.start_date + timedelta(weeks=self.subject.number_of_lessons - 1)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")
        unique_together = ('subject', 'academic_period', 'day_of_week', 'start_time')
        ordering = ['-academic_period', 'subject__name', 'start_date']

class Enrollment(models.Model):
    class Status(models.TextChoices):
        ENROLLED = 'ENROLLED', _('Enrolled')
        APPROVED = 'APPROVED', _('Approved')
        REPROVED = 'REPROVED', _('Reproved')
        COMPLETED = 'COMPLETED', _('Completed')
        DROPPED = 'DROPPED', _('Dropped Out')
        # Add more statuses if needed, e.g., 'AUDITING'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments', verbose_name=_("student"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name=_("course"))
    enrollment_date = models.DateField(_("enrollment date"), default=date.today)
    
    lesson_score = models.DecimalField(
        _("lesson score"),
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text=_("Average score for lessons (e.g., out of 100).")
    )
    exam_score = models.DecimalField(
        _("exam score"),
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text=_("Score for the final exam (e.g., out of 100).")
    )
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=Status.choices,
        default=Status.ENROLLED
    )

    @property
    def attendance_score(self):
        """
        Calculates attendance score as a percentage (0-100).
        Assumes 100 points for perfect attendance.
        """
        total_lessons = self.course.subject.number_of_lessons
        if total_lessons == 0:
            return None # Or 0, depending on policy

        attended_lessons_count = self.attendance_logs.filter(is_present=True).count()
        
        if attended_lessons_count > total_lessons: # Should not happen with proper data entry
            attended_lessons_count = total_lessons

        return (attended_lessons_count / total_lessons) * 100 if total_lessons > 0 else 0.00

    @property
    def final_grade(self):
        """
        Calculates the final grade as an average of homework, attendance, and exam scores.
        Scores are assumed to be on a similar scale (e.g., 0-100).
        """
        scores = []
        if self.lesson_score is not None: # This is already a Decimal
            scores.append(self.lesson_score) 
        
        att_score = self.attendance_score
        if att_score is not None:
            scores.append(Decimal(att_score)) # Convert float to Decimal

        if self.exam_score is not None: # This is already a Decimal
            scores.append(self.exam_score) 

        if not scores:
            return None
        
        return sum(scores) / Decimal(len(scores))

    def __str__(self):
        return f"{self.student} - {self.course.subject.name} ({self.course.academic_period})"

    class Meta:
        verbose_name = _("enrollment")
        verbose_name_plural = _("enrollments")
        unique_together = ('student', 'course')
        ordering = ['course', 'student__surname', 'student__name']

class AttendanceLog(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.PROTECT,
        related_name='attendance_logs',
        verbose_name=_("enrollment")
    )
    lesson_date = models.DateField(_("lesson date"), validators=[validate_date])
    lesson_number = models.PositiveIntegerField(
        _("lesson number"),
        help_text=_("Indicates which lesson of the course this is (e.g., 1, 2, ..., N).")
    )
    is_present = models.BooleanField(_("was present"), default=False)
    notes = models.TextField(_("notes"), blank=True, null=True, help_text=_("Optional notes by the teacher for this session."))

    def __str__(self):
        status = _("Present") if self.is_present else _("Absent")
        return f"{self.enrollment.student} - Lesson {self.lesson_number} ({self.lesson_date.strftime('%Y-%m-%d')}) - {status}"

    class Meta:
        verbose_name = _("attendance log")
        verbose_name_plural = _("attendance logs")
        # A student can only have one attendance record per lesson number in a specific enrollment
        unique_together = ('enrollment', 'lesson_number')
        # Or, if dates are more fixed than lesson numbers:
        # unique_together = ('enrollment', 'lesson_date')
        ordering = ['enrollment', 'lesson_date', 'lesson_number']

class Grade(models.Model):
    GRADE_TYPE_CHOICES = [
        ('Leccion', _('Lesson')),
        ('Examen', _('Exam')),
    ]

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.PROTECT,
        related_name='grades',
        verbose_name=_("enrollment")
    )
    lesson_number = models.PositiveIntegerField(
        _("lesson number"),
        help_text=_("The lesson number this grade refers to. If 'Exam', put 0.")
    )
    grade = models.DecimalField(_("grade"), max_digits=5, decimal_places=2)
    grade_type = models.CharField(_("grade type"), max_length=10, choices=GRADE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.enrollment} - {self.get_grade_type_display()} - {self.grade}"

    class Meta:
        verbose_name = _("grade")
        verbose_name_plural = _("grades")
        # Consider a unique constraint.  Is a student allowed multiple grades
        # for the same lesson number (e.g., a retake)? If so, remove the unique_together.
        unique_together = ('enrollment', 'lesson_number', 'grade_type')
        ordering = ['enrollment', 'grade_type', 'lesson_number']        