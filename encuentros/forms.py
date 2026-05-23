from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Meeting, Server, Participant, FamilyParticipantInfo, ChurchDataInfo, MeetingParticipant, FinanceMovements

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['code', 'type', 'description', 'date']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'code': _('Meeting Code'),
            'type': _('Meeting Type'),
            'description': _('Description'),
            'date': _('Meeting Date'),
        }
        help_texts = {
            'code': model._meta.get_field('code').help_text,
            'type': model._meta.get_field('type').help_text,
            'description': model._meta.get_field('description').help_text,
            'date': model._meta.get_field('date').help_text,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['first_name', 'last_name', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
        }
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'phone_number': _('Phone Number'),
        }
        help_texts = {
            'first_name': model._meta.get_field('first_name').help_text,
            'last_name': model._meta.get_field('last_name').help_text,
            'phone_number': model._meta.get_field('phone_number').help_text,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'name', 'surname', 'email', 'phone_number', 
            'date_of_birth', 'height', 'address_reference', 
            'civil_status', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'address_reference': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'civil_status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': _('Name'),
            'surname': _('Surname'),
            'email': _('Email Address'),
            'phone_number': _('Phone Number'),
            'date_of_birth': _('Date of Birth'),
            'height': _('Height (cm)'),
            'address_reference': _('Address Reference'),
            'civil_status': _('Civil Status'),
            'notes': _('Notes (Allergies, disabilities, etc.)'),
        }
        # Help texts can be inherited from the model if defined there, 
        # or you can add/override them here if needed.
        # For example: help_texts = {'email': _('Optional but recommended.')}        

class FamilyParticipantInfoForm(forms.ModelForm):
    class Meta:
        model = FamilyParticipantInfo
        fields = ['participant', 'name', 'surname', 'phone_number', 'familiar_relationship']
        widgets = {
            'participant': forms.Select(attrs={'class': 'form-control select2'}), # Usaremos select2 para buscar participantes
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'familiar_relationship': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'participant': _('Main Participant'),
            'name': _('Family Member Name'),
            'surname': _('Family Member Surname'),
            'phone_number': _('Family Member Phone Number'),
            'familiar_relationship': _('Relationship to Participant'),
        }
        help_texts = {
            'participant': _("Select the main participant this family member is related to."),
            'familiar_relationship': _("E.g., Spouse, Son, Mother, Emergency Contact."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Podrías filtrar el queryset de 'participant' si es necesario, por ejemplo, por activos.
        # self.fields['participant'].queryset = Participant.objects.filter(is_active=True)

class ChurchDataInfoForm(forms.ModelForm):
    class Meta:
        model = ChurchDataInfo
        fields = [
            'participant', 'is_member_of_church', 'church_name', 
            'is_baptized', 'baptism_date', 'is_part_of_disciple_group', 
            'name_of_leader', 'is_part_of_bible_academy', 'actual_subject',
            'is_registered_paid', 'amount_paid', 'payment_reference', 'server'
        ]
        widgets = {
            'participant': forms.Select(attrs={'class': 'form-control select2'}),
            'is_member_of_church': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'church_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_baptized': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'baptism_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_part_of_disciple_group': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'name_of_leader': forms.TextInput(attrs={'class': 'form-control'}),
            'is_part_of_bible_academy': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'actual_subject': forms.TextInput(attrs={'class': 'form-control'}),
            'is_registered_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_reference': forms.TextInput(attrs={'class': 'form-control'}),
            'server': forms.Select(attrs={'class': 'form-control select2'}),
        }
        labels = {
            'participant': _('Participant'),
            'is_member_of_church': _('Is Member of a Church?'),
            'church_name': _('Church Name'),
            'is_baptized': _('Is Baptized?'),
            'baptism_date': _('Baptism Date'),
            'is_part_of_disciple_group': _('Is Part of a Disciple Group?'),
            'name_of_leader': _('Name of Leader'),
            'is_part_of_bible_academy': _('Is Part of Bible Academy?'),
            'actual_subject': _('Actual Subject in Academy'),
            'is_registered_paid': _('Is Registered and Paid?'),
            'amount_paid': _('Amount Paid'),
            'payment_reference': _('Payment Reference'),
            'server': _('Assisting Server'),
        }        


class MeetingParticipantForm(forms.ModelForm):
    class Meta:
        model = MeetingParticipant
        fields = ['meeting', 'participant', 'event_date', 'is_present']
        widgets = {
            'meeting': forms.Select(attrs={'class': 'form-control select2'}),
            'participant': forms.Select(attrs={'class': 'form-control select2'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'meeting': _('Meeting'),
            'participant': _('Participant'),
            'event_date': _('Attendance Date'), # Consistent with model's verbose_name
            'is_present': _('Was Present?'),
        }
        help_texts = {
            'event_date': _("The specific date the participant attended this meeting session."),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optimize choices by ordering them or prefetching related data if needed for display
        self.fields['meeting'].queryset = Meeting.objects.order_by('-date', 'code')
        self.fields['participant'].queryset = Participant.objects.order_by('surname', 'name')

    # Django's model validation will handle the unique_together constraint by default.
    # If you need a more custom error message for the unique_together constraint,
    # you could add a clean() method here.        

class FinanceMovementsForm(forms.ModelForm):
    class Meta:
        model = FinanceMovements
        fields = ['trans_date', 'transaction_type', 'amount', 'description', 'meeting_related']
        widgets = {
            'trans_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'meeting_related': forms.Select(attrs={'class': 'form-control select2'}),
        }
        labels = {
            'trans_date': _('Transaction Date'),
            'transaction_type': _('Transaction Type'),
            'amount': _('Amount'),
            'description': _('Description'),
            'meeting_related': _('Related Meeting (Optional)'),
        }
        help_texts = {
            'meeting_related': model._meta.get_field('meeting_related').help_text,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order meetings for better selection
        self.fields['meeting_related'].queryset = Meeting.objects.order_by('-date', 'code')
        # The 'meeting_related' field is already optional in the model (blank=True, null=True)
        # so the form will allow it to be empty.

class GenerateSummaryForm(forms.Form):
    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.order_by('-date', 'code'),
        label=_("Meeting to Summarize"),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        help_text=_("Select the meeting for which you want to generate a financial summary.")
    )
        # The 'meeting_related' field is already optional in the model (blank=True, null=True)
        # so the form will allow it to be empty.