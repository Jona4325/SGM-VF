from django import forms
from .models import Coordinator, Group, Server, Assistance
from django.utils import timezone

class CoordinatorForm(forms.ModelForm):
    class Meta:
        model = Coordinator
        fields = ['name', 'surname']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = ['name', 'surname', 'coordinator', 'group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'coordinator': forms.Select(attrs={'class': 'form-select'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
        }

class AssistanceForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), initial=timezone.now().date())

    class Meta:
        model = Assistance
        fields = ['date']  # Incluir solo el campo de fecha aquí

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        servers = Server.objects.all()
        for server in servers:
            self.fields[f'server_{server.id}'] = forms.BooleanField(
                label=f"{server.name} {server.surname}",
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )
            
class AssistanceUpdateForm(forms.ModelForm):
    class Meta:
        model = Assistance
        fields = ['server', 'date', 'attended']
        widgets = {
            'server': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }