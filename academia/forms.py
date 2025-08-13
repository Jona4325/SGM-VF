from django import forms
from .models import Teacher, Student, Subject, Course, Enrollment, AttendanceLog, Grade
from django.utils.translation import gettext_lazy as _
from datetime import date

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'email', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre',
            'surname': 'Apellido',
            'email': 'Correo Electrónico',
            'phone_number': 'Número de Teléfono',
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'surname', 'email', 'phone_number', 'date_of_birth']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': 'Nombre',
            'surname': 'Apellido',
            'email': 'Correo Electrónico',
            'phone_number': 'Número de Teléfono',
            'date_of_birth': 'Fecha de Nacimiento',
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'number_of_lessons']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'number_of_lessons': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nombre de la Asignatura',
            'description': 'Descripción',
            'number_of_lessons': 'Número de Lecciones',
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'subject', 'teacher', 'academic_period', 'day_of_week',
            'start_time', 'start_date', 'end_date', 'is_active'
        ]
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control select2'}), # Usar select2 para mejor UX
            'teacher': forms.Select(attrs={'class': 'form-control select2'}), # Usar select2 para mejor UX
            'academic_period': forms.TextInput(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # El modelo lo calcula si se deja vacío
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'subject': 'Asignatura',
            'teacher': 'Profesor',
            'academic_period': 'Periodo Académico',
            'day_of_week': 'Día de la Semana',
            'start_time': 'Hora de Inicio',
            'start_date': 'Fecha de Inicio',
            'end_date': 'Fecha de Fin (opcional, se calcula si se deja en blanco)',
            'is_active': '¿Está Activo?',
        }
        help_texts = {
            'end_date': Course._meta.get_field('end_date').help_text # Heredar help_text del modelo
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo end_date no es obligatorio en el formulario ya que el modelo puede calcularlo.
        self.fields['end_date'].required = False

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date', 'status', 'lesson_score', 'exam_score']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control select2'}),
            'course': forms.Select(attrs={'class': 'form-control select2'}),
            'enrollment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'lesson_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'exam_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'student': _('Student'),
            'course': _('Course'),
            'enrollment_date': _('Enrollment Date'),
            'status': _('Status'),
            'lesson_score': _('Lesson Score'),
            'exam_score': _('Exam Score'),
        }
        help_texts = {
            'enrollment_date': _('Defaults to today if not specified.'),
            'lesson_score': Enrollment._meta.get_field('lesson_score').help_text,
            'exam_score': Enrollment._meta.get_field('exam_score').help_text,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El ModelForm ya debería usar el 'default' del modelo para 'initial'
        # cuando se crea un nuevo formulario.
        # Si necesitas establecer explícitamente el atributo 'value' del widget:
        default_enrollment_date_callable = Enrollment._meta.get_field('enrollment_date').default
        if callable(default_enrollment_date_callable):
            actual_default_value = default_enrollment_date_callable()
            # El widget DateInput(type='date') puede manejar un objeto date directamente.
            self.fields['enrollment_date'].widget.attrs.setdefault('value', actual_default_value.strftime('%Y-%m-%d'))

class AttendanceLogForm(forms.ModelForm):
    class Meta:
        model = AttendanceLog
        fields = ['enrollment', 'lesson_date', 'lesson_number', 'is_present', 'notes']
        widgets = {
            'enrollment': forms.Select(attrs={'class': 'form-control select2'}),
            'lesson_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lesson_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'enrollment': _('Enrollment (Student - Course)'),
            'lesson_date': _('Lesson Date'),
            'lesson_number': _('Lesson Number'),
            'is_present': _('Was Present?'),
            'notes': _('Notes'),
        }
        help_texts = {
            'lesson_number': AttendanceLog._meta.get_field('lesson_number').help_text,
            'notes': AttendanceLog._meta.get_field('notes').help_text,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer la fecha de hoy como valor por defecto para lesson_date si es un formulario nuevo
        if not self.instance.pk and 'initial' not in kwargs: # Solo para creación y si no se provee initial
             self.fields['lesson_date'].widget.attrs.setdefault('value', AttendanceLog._meta.get_field('lesson_date').validators[0].__self__.today().strftime('%Y-%m-%d') if hasattr(AttendanceLog._meta.get_field('lesson_date').validators[0], '__self__') and hasattr(AttendanceLog._meta.get_field('lesson_date').validators[0].__self__, 'today') else date.today().strftime('%Y-%m-%d'))

    def clean_lesson_number(self):
        lesson_number = self.cleaned_data.get('lesson_number')
        enrollment = self.cleaned_data.get('enrollment')
        if enrollment and lesson_number > enrollment.course.subject.number_of_lessons:
            raise forms.ValidationError(_("Lesson number cannot exceed the total number of lessons for the course's subject (%(max_lessons)s).") % {'max_lessons': enrollment.course.subject.number_of_lessons})
        return lesson_number


class AttendanceTakingSelectionForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.select_related('subject').order_by('-academic_period', 'subject__name'),
        label=_("Course"),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    lesson_date = forms.DateField(
        label=_("Lesson Date"),
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=date.today
    )
    lesson_number = forms.IntegerField(
        label=_("Lesson Number"),
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        min_value=1
    )

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get("course")
        lesson_number = cleaned_data.get("lesson_number")

        if course and lesson_number:
            if lesson_number > course.subject.number_of_lessons:
                self.add_error('lesson_number', forms.ValidationError(
                    _("Lesson number (%(lesson_num)s) cannot exceed the total number of lessons (%(max_lessons)s) for this course's subject.") % {
                        'lesson_num': lesson_number,
                        'max_lessons': course.subject.number_of_lessons
                    }
                ))
        return cleaned_data

class StudentAttendanceForm(forms.Form):
    enrollment_id = forms.IntegerField(widget=forms.HiddenInput())
    is_present = forms.BooleanField(label=_("P"), required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input ms-2 me-1'})) # P for Present
    notes = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': _('Optional notes')}))


class GradeTakingSelectionForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.select_related('subject').order_by('-academic_period', 'subject__name'),
        label=_("Course"),
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    lesson_number = forms.IntegerField(
        label=_("Lesson Number (0 for Exam)"),
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        min_value=0,
        help_text=_("Use 0 for the final exam grade.")
    )
    grade_type = forms.ChoiceField(
        choices=Grade.GRADE_TYPE_CHOICES,
        label=_("Grade Type"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get("course")
        lesson_number = cleaned_data.get("lesson_number")
        grade_type = cleaned_data.get("grade_type")

        if course and lesson_number is not None:
            if grade_type == 'Leccion' and lesson_number == 0:
                 self.add_error('lesson_number', forms.ValidationError(
                    _("Lesson number must be greater than 0 for grade type 'Lesson'.")
                ))
            if grade_type == 'Examen' and lesson_number != 0:
                 self.add_error('lesson_number', forms.ValidationError(
                    _("Lesson number must be 0 for grade type 'Exam'.")
                ))
            if lesson_number > course.subject.number_of_lessons:
                self.add_error('lesson_number', forms.ValidationError(
                    _("Lesson number (%(lesson_num)s) cannot exceed the total number of lessons (%(max_lessons)s) for this course's subject.") % {
                        'lesson_num': lesson_number,
                        'max_lessons': course.subject.number_of_lessons
                    }
                ))
        return cleaned_data

class StudentGradeForm(forms.Form):
    enrollment_id = forms.IntegerField(widget=forms.HiddenInput())
    grade = forms.DecimalField(label="", required=False, widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': _('Grade'), 'step': '0.01'}))

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['enrollment', 'lesson_number', 'grade', 'grade_type']
        widgets = {
            'enrollment': forms.Select(attrs={'class': 'form-control select2'}),
            'lesson_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control'}),
            'grade_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'enrollment': _('Enrollment'),
            'lesson_number': _('Lesson Number (0 for Exam)'),
            'grade': _('Grade'),
            'grade_type': _('Grade Type'),
        }    

class ClosePeriodForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.select_related('subject').order_by('-academic_period', 'subject__name'),
        label=_("Course to Close"),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        help_text=_("Select the course to close the period and calculate final grades.")
    )