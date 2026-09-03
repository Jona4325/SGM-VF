from datetime import date, time

from django.test import TestCase

from account.models import Tenant
from account.tenant import set_current_tenant

from .forms import ClosedCourseReportForm
from .models import Course, Subject, Teacher


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
