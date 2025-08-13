# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _

class Meeting(models.Model): # Renombrado de Encounter a Meeting
    """
    Represents a meeting.
    """
    TYPE_CHOICES = [
        ('M', _('Male')),   # Opción para Masculino
        ('F', _('Female')), # Opción para Femenino
    ]

    code = models.CharField(
        _("Code"),
        max_length=50,
        unique=True,
        help_text=_("Unique code identifying the meeting.")
    )
    type = models.CharField(
        _("Type"),
        max_length=1, # Suficiente para 'M' o 'F'
        choices=TYPE_CHOICES,
        help_text=_("Specify if the meeting is for Male or Female participants.")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("Detailed description of the meeting.")
    )
    date = models.DateField(
        _("Date"),
        help_text=_("Date on which the meeting takes place.")
    )

    class Meta:
        verbose_name = _("Meeting")
        verbose_name_plural = _("Meetings")
        ordering = ['-date', 'code']

    def __str__(self):
        # Mostrar el valor legible del tipo usando get_type_display()
        return f"{self.code} - {self.get_type_display()} ({self.date.strftime('%Y-%m-%d') if self.date else 'N/A'})"


class Server(models.Model):
    """
    Represents a person who serves or volunteers at meetings.
    """
    first_name = models.CharField(
        _("First Name"),
        max_length=100
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=100
    )
    phone_number = models.CharField(
        _("Phone Number"),
        max_length=20,
        blank=True, # Making phone number optional
        null=True,
        help_text=_("Contact phone number (optional).")
    )

    class Meta:
        verbose_name = _("Server") # Manteniendo "Server" como nombre de modelo, "Servidor" para visualización
        verbose_name_plural = _("Servers")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Participant(models.Model):
    STATUS_CHOICES = [
        ('SOLTERO', _('Single')),
        ('CASADO', _('Married')),
        ('DIVORCIADO', _('Divorced')),
        ('VIUDO', _('Widowed')),
        ('UNIÓN LIBRE', _('Union Free')),

    ]
    name = models.CharField(_("name"), max_length=128)
    surname = models.CharField(_("surname"), max_length=128)
    email = models.EmailField(_("email"), max_length=254, unique=True, null=True, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(
        _("date of birth"),
        null=True, blank=True,
        help_text=_("Format: YYYY-MM-DD")
    )
    height = models.PositiveIntegerField( # Changed to PositiveIntegerField, assuming height cannot be negative
        _("height"),
        null=True, blank=True, # Making height optional
        help_text=_("Height in centimeters (optional).")
    )
    address_reference = models.CharField(
        _("address reference"),
        max_length=256,
        null=True, blank=True
    )
    civil_status = models.CharField(
        _("civil status"),
        max_length=16, # Suficiente para 'M' o 'F'
        choices=STATUS_CHOICES,
        null=True, blank=True # Making civil status optional
    )
    notes = models.TextField(
        _("Notes"),
        blank=True,
        null=True,
        help_text=_("Allergies, disabilities, medications, etc.")
    )


    def __str__(self):
        return f"{self.name} {self.surname}"    

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        ordering = ['surname', 'name']

class FamilyParticipantInfo(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.PROTECT,
        related_name='family_members'
    )
    name = models.CharField(_("name"), max_length=128)
    surname = models.CharField(_("surname"), max_length=128)
    phone_number = models.CharField(_("phone number"), max_length=20, null=True, blank=True)
    familiar_relationship = models.CharField(
        _("familiar relationship"),
        max_length=32,
        null=True, blank=True
    )

    class Meta:
        verbose_name = _("Family Participant Info")
        verbose_name_plural = _("Family Participant Infos")

    def __str__(self):
        return f"{self.name} {self.surname} (Family of {self.participant})"

class ChurchDataInfo(models.Model):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.PROTECT,
        related_name='church_data'
    )
    is_member_of_church = models.BooleanField(_("is member of church"), default=False)
    church_name = models.CharField(_("church name"), max_length=128, blank=True, null=True) # Made optional
    is_baptized = models.BooleanField(_("is baptized"), default=False)
    baptism_date = models.DateField(
        _("baptism date"),
        null=True, blank=True,
        help_text=_("Format: YYYY-MM-DD")
    )
    is_part_of_disciple_group = models.BooleanField(_("is part of disciple group"), default=False)
    name_of_leader = models.CharField(_("name of leader"), max_length=128, null=True, blank=True)
    is_part_of_bible_academy = models.BooleanField(_("is part of bible academy"), default=False)
    actual_subject = models.CharField(_("actual subject"), max_length=128, null=True, blank=True)
    is_registered_paid = models.BooleanField(_("is registered and paid"), default=False)
    amount_paid = models.DecimalField(
        _("amount paid"),
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    payment_reference = models.CharField(_("payment reference"), max_length=128, null=True, blank=True)
    server = models.ForeignKey(
        Server,
        on_delete=models.PROTECT, # Consider models.SET_NULL if a server can be deleted but data retained
        null=True, blank=True, # Assuming a server might not always be assigned
        related_name='assisted_church_infos'
    )

    class Meta:
        verbose_name = _("Church Data Info")
        verbose_name_plural = _("Church Data Infos")

    def __str__(self):
        return f"Church info for {self.participant}"

    
class MeetingParticipant(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.PROTECT,
        related_name='attendees'
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.PROTECT,
        related_name='meeting_attendances'
    )
    event_date = models.DateField(
        _("attendance date"), # Changed verbose_name for clarity
    )
    is_present = models.BooleanField(_("was present"), default=False)

    class Meta:
        verbose_name = _("Meeting Participant")
        verbose_name_plural = _("Meeting Participants")
        unique_together = [['meeting', 'participant', 'event_date']] # Ensure one record per participant per meeting on a given date

    def __str__(self):
        return f"{self.participant} at {self.meeting} on {self.event_date}"


class FinanceMovements(models.Model):
    TRANS_CHOICES = [
        ('INCOME', _('Income')),
        ('EXPENSE', _('Expense')),
    ]

    trans_date = models.DateField(_("transaction date"))
    transaction_type = models.CharField( # Renamed from transaction_code for clarity
        _("transaction type"),
        max_length=16,
        choices=TRANS_CHOICES,
        help_text=_("Specify if the transaction is an Income or Expense.")
    )
    amount = models.DecimalField(
        _("amount"),
        max_digits=10, decimal_places=2
    )
    description = models.CharField(_("description"), max_length=255, blank=True)
    meeting_related = models.ForeignKey( # Optional link to a meeting
        Meeting,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='financial_movements',
        help_text=_("Optional: Link this transaction to a specific meeting.")
    )

    class Meta:
        verbose_name = _("Financial Movement")
        verbose_name_plural = _("Financial Movements")
        ordering = ['-trans_date']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} on {self.trans_date}"

class Summary(models.Model):
    period_end = models.DateField(_("period end"))
    income = models.DecimalField(_("total income"), max_digits=12, decimal_places=2)
    expense = models.DecimalField(_("total expense"), max_digits=12, decimal_places=2)
    balance = models.DecimalField(_("balance"), max_digits=12, decimal_places=2)
    meeting = models.ForeignKey( # Assuming this summary is per meeting
        Meeting,
        on_delete=models.PROTECT,
        related_name='financial_summaries'
    )

    class Meta:
        verbose_name = _("Financial Summary")
        verbose_name_plural = _("Financial Summaries")
        ordering = ['-period_end', 'meeting']

    def __str__(self):
        return f"Summary for {self.meeting} as of {self.period_end}"