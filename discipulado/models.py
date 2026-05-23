from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from account.tenant import TenantAwareModel


class PersonStatus(models.TextChoices):
	ACTIVE = 'ACTIVE', _('Active')
	INACTIVE = 'INACTIVE', _('Inactive')


class MemberRole(models.TextChoices):
	MEMBER = 'MEMBER', _('Member')
	LEADER = 'LEADER', _('Leader')
	COLEADER = 'COLEADER', _('Co-Leader')


class AttendanceStatus(models.TextChoices):
	PRESENT = 'PRESENT', _('Present')
	ABSENT = 'ABSENT', _('Absent')
	JUSTIFIED = 'JUSTIFIED', _('Justified')


class OfferingCategory(models.TextChoices):
	GENERAL = 'GENERAL', _('General')
	MISSIONS = 'MISSIONS', _('Missions')
	SPECIAL = 'SPECIAL', _('Special')


class ExpenseCategory(models.TextChoices):
	SNACK = 'SNACK', _('Snack')
	MATERIAL = 'MATERIAL', _('Material')
	LOGISTICS = 'LOGISTICS', _('Logistics')
	OTHER = 'OTHER', _('Other')


class MeetingStatus(models.TextChoices):
	SCHEDULED = 'SCHEDULED', _('Scheduled')
	COMPLETED = 'COMPLETED', _('Completed')
	CANCELED = 'CANCELED', _('Canceled')


class Supervisor(TenantAwareModel):
	first_name = models.CharField(_('first name'), max_length=128)
	last_name = models.CharField(_('last name'), max_length=128)
	email = models.EmailField(_('email'), blank=True, null=True)
	phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
	notes = models.TextField(_('notes'), blank=True)
	status = models.CharField(
		_('status'),
		max_length=16,
		choices=PersonStatus.choices,
		default=PersonStatus.ACTIVE,
	)

	class Meta:
		verbose_name = _('Supervisor')
		verbose_name_plural = _('Supervisors')
		ordering = ['last_name', 'first_name']
		constraints = [
			models.UniqueConstraint(
				fields=['tenant', 'email'],
				condition=Q(email__isnull=False),
				name='discipulado_supervisor_tenant_email_uniq',
			),
		]

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class HostFamily(TenantAwareModel):
	family_name = models.CharField(_('family name'), max_length=160)
	contact_name = models.CharField(_('contact name'), max_length=160)
	contact_phone = models.CharField(_('contact phone'), max_length=20, blank=True, null=True)
	address = models.CharField(_('address'), max_length=255, blank=True)
	reference = models.CharField(_('reference'), max_length=255, blank=True)
	notes = models.TextField(_('notes'), blank=True)
	status = models.CharField(
		_('status'),
		max_length=16,
		choices=PersonStatus.choices,
		default=PersonStatus.ACTIVE,
	)

	class Meta:
		verbose_name = _('Host family')
		verbose_name_plural = _('Host families')
		ordering = ['family_name']
		unique_together = [('tenant', 'family_name')]

	def __str__(self):
		return self.family_name


class Disciple(TenantAwareModel):
	first_name = models.CharField(_('first name'), max_length=128)
	last_name = models.CharField(_('last name'), max_length=128)
	email = models.EmailField(_('email'), blank=True, null=True)
	phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
	date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
	address = models.CharField(_('address'), max_length=255, blank=True)
	notes = models.TextField(_('notes'), blank=True)
	status = models.CharField(
		_('status'),
		max_length=16,
		choices=PersonStatus.choices,
		default=PersonStatus.ACTIVE,
	)

	class Meta:
		verbose_name = _('Disciple')
		verbose_name_plural = _('Disciples')
		ordering = ['last_name', 'first_name']
		constraints = [
			models.UniqueConstraint(
				fields=['tenant', 'email'],
				condition=Q(email__isnull=False),
				name='discipulado_disciple_tenant_email_uniq',
			),
		]

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class DiscipleshipGroup(TenantAwareModel):
	name = models.CharField(_('name'), max_length=128)
	leader = models.ForeignKey(
		Disciple,
		on_delete=models.PROTECT,
		related_name='leading_groups',
	)
	coleader = models.ForeignKey(
		Disciple,
		on_delete=models.PROTECT,
		related_name='coleading_groups',
		blank=True,
		null=True,
	)
	host_family = models.ForeignKey(
		HostFamily,
		on_delete=models.PROTECT,
		related_name='groups',
	)
	supervisor = models.ForeignKey(
		Supervisor,
		on_delete=models.PROTECT,
		related_name='groups',
		blank=True,
		null=True,
	)
	notes = models.TextField(_('notes'), blank=True)
	is_active = models.BooleanField(_('is active'), default=True)

	class Meta:
		verbose_name = _('Discipleship group')
		verbose_name_plural = _('Discipleship groups')
		ordering = ['name']
		unique_together = [('tenant', 'name')]

	def clean(self):
		super().clean()
		if self.coleader_id and self.leader_id == self.coleader_id:
			raise ValidationError({'coleader': _('Leader and co-leader must be different people.')})

	def __str__(self):
		return self.name


class DiscipleshipGroupMember(TenantAwareModel):
	group = models.ForeignKey(
		DiscipleshipGroup,
		on_delete=models.CASCADE,
		related_name='memberships',
	)
	disciple = models.ForeignKey(
		Disciple,
		on_delete=models.PROTECT,
		related_name='group_memberships',
	)
	role = models.CharField(
		_('role'),
		max_length=16,
		choices=MemberRole.choices,
		default=MemberRole.MEMBER,
	)
	joined_on = models.DateField(_('joined on'), blank=True, null=True)
	is_active = models.BooleanField(_('is active'), default=True)

	class Meta:
		verbose_name = _('Discipleship group member')
		verbose_name_plural = _('Discipleship group members')
		ordering = ['group', 'disciple']
		unique_together = [('tenant', 'group', 'disciple')]

	def __str__(self):
		return f'{self.disciple} - {self.group} ({self.get_role_display()})'


class DiscipleshipMeeting(TenantAwareModel):
	group = models.ForeignKey(
		DiscipleshipGroup,
		on_delete=models.PROTECT,
		related_name='meetings',
	)
	meeting_date = models.DateField(_('meeting date'))
	start_time = models.TimeField(_('start time'), blank=True, null=True)
	topic = models.CharField(_('topic'), max_length=255, blank=True)
	notes = models.TextField(_('notes'), blank=True)
	status = models.CharField(
		_('status'),
		max_length=16,
		choices=MeetingStatus.choices,
		default=MeetingStatus.COMPLETED,
	)

	class Meta:
		verbose_name = _('Discipleship meeting')
		verbose_name_plural = _('Discipleship meetings')
		ordering = ['-meeting_date', 'group__name']
		unique_together = [('tenant', 'group', 'meeting_date')]

	def __str__(self):
		return f'{self.group} - {self.meeting_date}'

	@property
	def total_offerings(self):
		value = self.offerings.aggregate(total=models.Sum('amount'))['total']
		return value or Decimal('0.00')

	@property
	def total_expenses(self):
		value = self.expenses.aggregate(total=models.Sum('amount'))['total']
		return value or Decimal('0.00')

	@property
	def balance(self):
		return self.total_offerings - self.total_expenses


class MeetingAttendance(TenantAwareModel):
	meeting = models.ForeignKey(
		DiscipleshipMeeting,
		on_delete=models.CASCADE,
		related_name='attendances',
	)
	disciple = models.ForeignKey(
		Disciple,
		on_delete=models.PROTECT,
		related_name='attendances',
	)
	status = models.CharField(
		_('attendance status'),
		max_length=16,
		choices=AttendanceStatus.choices,
		default=AttendanceStatus.PRESENT,
	)
	notes = models.CharField(_('notes'), max_length=255, blank=True)

	class Meta:
		verbose_name = _('Meeting attendance')
		verbose_name_plural = _('Meeting attendances')
		ordering = ['meeting', 'disciple']
		unique_together = [('tenant', 'meeting', 'disciple')]

	def __str__(self):
		return f'{self.disciple} - {self.meeting} ({self.get_status_display()})'


class OfferingIncome(TenantAwareModel):
	meeting = models.ForeignKey(
		DiscipleshipMeeting,
		on_delete=models.CASCADE,
		related_name='offerings',
	)
	amount = models.DecimalField(
		_('amount'),
		max_digits=12,
		decimal_places=2,
		validators=[MinValueValidator(Decimal('0.01'))],
	)
	category = models.CharField(
		_('category'),
		max_length=16,
		choices=OfferingCategory.choices,
		default=OfferingCategory.GENERAL,
	)
	received_from = models.ForeignKey(
		Disciple,
		on_delete=models.SET_NULL,
		related_name='offerings_made',
		blank=True,
		null=True,
	)
	notes = models.CharField(_('notes'), max_length=255, blank=True)
	registered_at = models.DateField(_('registered at'))

	class Meta:
		verbose_name = _('Offering income')
		verbose_name_plural = _('Offering incomes')
		ordering = ['-registered_at', '-id']

	def __str__(self):
		return f'{self.meeting} - {self.amount}'


class MeetingExpense(TenantAwareModel):
	meeting = models.ForeignKey(
		DiscipleshipMeeting,
		on_delete=models.CASCADE,
		related_name='expenses',
	)
	amount = models.DecimalField(
		_('amount'),
		max_digits=12,
		decimal_places=2,
		validators=[MinValueValidator(Decimal('0.01'))],
	)
	category = models.CharField(
		_('category'),
		max_length=16,
		choices=ExpenseCategory.choices,
		default=ExpenseCategory.SNACK,
	)
	description = models.CharField(_('description'), max_length=255)
	paid_to = models.CharField(_('paid to'), max_length=160, blank=True)
	notes = models.CharField(_('notes'), max_length=255, blank=True)
	registered_at = models.DateField(_('registered at'))

	class Meta:
		verbose_name = _('Meeting expense')
		verbose_name_plural = _('Meeting expenses')
		ordering = ['-registered_at', '-id']

	def __str__(self):
		return f'{self.meeting} - {self.amount}'


class SupervisionVisit(TenantAwareModel):
	supervisor = models.ForeignKey(
		Supervisor,
		on_delete=models.PROTECT,
		related_name='visits',
	)
	meeting = models.ForeignKey(
		DiscipleshipMeeting,
		on_delete=models.PROTECT,
		related_name='supervision_visits',
	)
	visit_date = models.DateField(_('visit date'))
	observations = models.TextField(_('observations'), blank=True)

	class Meta:
		verbose_name = _('Supervision visit')
		verbose_name_plural = _('Supervision visits')
		ordering = ['-visit_date']
		unique_together = [('tenant', 'supervisor', 'meeting', 'visit_date')]

	def __str__(self):
		return f'{self.supervisor} - {self.meeting} ({self.visit_date})'
