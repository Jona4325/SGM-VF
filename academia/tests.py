from datetime import date, time
from io import BytesIO

from django.test import TestCase
from openpyxl import load_workbook

from account.models import Tenant
from account.tenant import set_current_tenant

from .forms import ClosedCourseReportForm, EnrolledStudentsReportForm
from .models import Course, Enrollment, Student, Subject, Teacher
from .views import build_enrolled_students_xlsx, get_enrolled_students_report_rows


class ClosedCourseReportFormTests(TestCase):
	def setUp(self):
		self.tenant = Tenant.objects.create(name='Tenant Reportes Academia')
		set_current_tenant(self.tenant)

		self.subject = Subject.objects.create(name='Matemáticas', description='Curso de prueba', number_of_lessons=8)
		self.teacher = Teacher.objects.create(name='Ana', surname='Pérez')
		self.closed_course = Course.objects.create(
			subject=self.subject,
			teacher=self.teacher,
			academic_period='2026 - C1',
			day_of_week='MON',
			start_time=time(8, 0),
			start_date=date(2026, 1, 5),
			is_closed=True,
		)
		self.open_course = Course.objects.create(
			subject=self.subject,
			teacher=self.teacher,
			academic_period='2026 - C2',
			day_of_week='TUE',
			start_time=time(9, 0),
			start_date=date(2026, 3, 10),
			is_closed=False,
		)

	def tearDown(self):
		set_current_tenant(None)

	def test_default_queryset_shows_only_closed_courses(self):
		form = ClosedCourseReportForm()

		self.assertEqual(
			list(form.fields['course'].queryset.values_list('id', flat=True)),
			[self.closed_course.id],
		)
		self.assertIn('onchange', form.fields['course_status'].widget.attrs)

	def test_open_filter_shows_open_courses(self):
		form = ClosedCourseReportForm({'course_status': 'open', 'course': self.open_course.pk})

		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data['course'], self.open_course)
		self.assertEqual(
			list(form.fields['course'].queryset.values_list('id', flat=True)),
			[self.open_course.id],
		)

	def test_all_filter_shows_both_courses(self):
		form = ClosedCourseReportForm({'course_status': 'all'})

		self.assertCountEqual(
			list(form.fields['course'].queryset.values_list('id', flat=True)),
			[self.closed_course.id, self.open_course.id],
		)


class EnrolledStudentsReportTests(TestCase):
	def setUp(self):
		self.tenant = Tenant.objects.create(name='Tenant Reporte Matriculados')
		set_current_tenant(self.tenant)

		self.subject = Subject.objects.create(name='Doctrina', description='Curso de prueba', number_of_lessons=8)
		self.teacher = Teacher.objects.create(name='Juan', surname='López')
		self.course = Course.objects.create(
			subject=self.subject,
			teacher=self.teacher,
			academic_period='CICLO 2 - 2026',
			day_of_week='SUN',
			start_time=time(7, 45),
			start_date=date(2026, 5, 31),
			is_closed=False,
		)
		self.other_course = Course.objects.create(
			subject=self.subject,
			teacher=self.teacher,
			academic_period='CICLO 2 - 2026',
			day_of_week='MON',
			start_time=time(8, 30),
			start_date=date(2026, 2, 1),
			is_closed=False,
		)
		self.other_period_course = Course.objects.create(
			subject=self.subject,
			teacher=self.teacher,
			academic_period='CICLO 1 - 2026',
			day_of_week='WED',
			start_time=time(9, 0),
			start_date=date(2026, 3, 1),
			is_closed=False,
		)
		self.student_1 = Student.objects.create(name='Ana', surname='Pérez')
		self.student_2 = Student.objects.create(name='Luis', surname='García')
		Enrollment.objects.create(student=self.student_1, course=self.course)
		Enrollment.objects.create(student=self.student_2, course=self.course)
		self.student_3 = Student.objects.create(name='Marta', surname='Zamora')
		Enrollment.objects.create(student=self.student_3, course=self.other_course)

	def tearDown(self):
		set_current_tenant(None)

	def test_course_queryset_is_available(self):
		form = EnrolledStudentsReportForm()
		self.assertEqual(form.fields['academic_period'].initial, 'CICLO 2 - 2026')
		self.assertEqual(list(form.fields['academic_period'].choices)[1:], [('CICLO 2 - 2026', 'CICLO 2 - 2026'), ('CICLO 1 - 2026', 'CICLO 1 - 2026')])

	def test_course_queryset_filters_by_period(self):
		form = EnrolledStudentsReportForm({'academic_period': 'CICLO 1 - 2026'})
		self.assertTrue(form.is_valid())
		self.assertEqual(form.cleaned_data['academic_period'], 'CICLO 1 - 2026')
		self.assertEqual(form.fields['academic_period'].initial, 'CICLO 1 - 2026')

	def test_rows_and_excel_export(self):
		rows = get_enrolled_students_report_rows('CICLO 2 - 2026')
		self.assertEqual(len(rows), 3)
		self.assertCountEqual([row['student'].surname for row in rows], ['Pérez', 'García', 'Zamora'])

		xlsx_bytes = build_enrolled_students_xlsx('CICLO 2 - 2026', rows)
		workbook = load_workbook(filename=BytesIO(xlsx_bytes))
		worksheet = workbook.active

		self.assertEqual(worksheet.title, 'Matriculados')
		self.assertEqual(worksheet['A1'].value, 'Listado de alumnos matriculados')
		self.assertEqual(worksheet['A2'].value, 'Periodo académico: CICLO 2 - 2026')
		self.assertCountEqual([worksheet['B6'].value, worksheet['B7'].value, worksheet['B8'].value], ['Ana Perez', 'Luis García', 'Marta Zamora'])
		self.assertEqual(worksheet['C6'].value, 'Doctrina')
