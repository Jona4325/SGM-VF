from django import forms

from .models import (
    Disciple,
    DiscipleshipGroup,
    DiscipleshipGroupMember,
    DiscipleshipMeeting,
    ExpenseCategory,
    HostFamily,
    MeetingExpense,
    OfferingCategory,
    OfferingIncome,
    Supervisor,
)


class DiscipleForm(forms.ModelForm):
    class Meta:
        model = Disciple
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'date_of_birth',
            'address',
            'status',
            'notes',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class HostFamilyForm(forms.ModelForm):
    class Meta:
        model = HostFamily
        fields = [
            'family_name',
            'contact_name',
            'contact_phone',
            'address',
            'reference',
            'status',
            'notes',
        ]
        widgets = {
            'family_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class SupervisorForm(forms.ModelForm):
    class Meta:
        model = Supervisor
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'status', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DiscipleshipGroupForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipGroup
        fields = ['name', 'leader', 'coleader', 'host_family', 'supervisor', 'is_active', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.Select(attrs={'class': 'form-select'}),
            'coleader': forms.Select(attrs={'class': 'form-select'}),
            'host_family': forms.Select(attrs={'class': 'form-select'}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DiscipleshipGroupMemberForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipGroupMember
        fields = ['group', 'disciple', 'role', 'joined_on', 'is_active']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-select'}),
            'disciple': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'joined_on': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DiscipleshipMeetingForm(forms.ModelForm):
    class Meta:
        model = DiscipleshipMeeting
        fields = ['group', 'meeting_date', 'start_time', 'topic', 'status', 'notes']
        widgets = {
            'group': forms.Select(attrs={'class': 'form-select'}),
            'meeting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OfferingIncomeForm(forms.ModelForm):
    class Meta:
        model = OfferingIncome
        fields = ['meeting', 'amount', 'category', 'received_from', 'registered_at', 'notes']
        widgets = {
            'meeting': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select', 'data-kind': OfferingCategory.GENERAL}),
            'received_from': forms.Select(attrs={'class': 'form-select'}),
            'registered_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MeetingExpenseForm(forms.ModelForm):
    class Meta:
        model = MeetingExpense
        fields = ['meeting', 'amount', 'category', 'description', 'paid_to', 'registered_at', 'notes']
        widgets = {
            'meeting': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'category': forms.Select(attrs={'class': 'form-select', 'data-kind': ExpenseCategory.SNACK}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'paid_to': forms.TextInput(attrs={'class': 'form-control'}),
            'registered_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BatchMeetingAttendanceForm(forms.Form):
    """Formulario dinámico para marcar asistencia de todos los integrantes del grupo en una reunión."""

    def __init__(self, disciples, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disciple_fields = []
        for disciple in disciples:
            field_name = f'disciple_{disciple.pk}'
            self.fields[field_name] = forms.BooleanField(
                label=f'{disciple.last_name}, {disciple.first_name}',
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-2'}),
            )
            self.disciple_fields.append(self[field_name])
