from django import forms
from .models import Assistance, Attendance, Coordinator, Group, Server, Ministry

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

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            'coordinator', 'group', 'ministry', 'date', 'attended',
            'adults', 'youngs', 'children', 'autos', 'note'
        ]
        widgets = {
            'coordinator': forms.Select(attrs={'class': 'form-select'}),
            'group': forms.Select(attrs={'class': 'form-select'}),
            'ministry': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'adults': forms.NumberInput(attrs={'class': 'form-control'}),
            'youngs': forms.NumberInput(attrs={'class': 'form-control'}),
            'children': forms.NumberInput(attrs={'class': 'form-control'}),
            'autos': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AssistanceForm(forms.ModelForm):
    class Meta:
        model = Assistance
        fields = ['server', 'date', 'starthour', 'service', 'attended']
        widgets = {
            'server': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'starthour': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'service': forms.Select(attrs={'class': 'form-select'}),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class BatchAssistanceForm(forms.Form):
    """
    Formulario para registrar la asistencia de múltiples servidores a la vez.
    """
    date = forms.DateField(label="Fecha", widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    starthour = forms.TimeField(label="Hora de Inicio", widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    service = forms.ChoiceField(label="Servicio", choices=Assistance.ServiceChoices.choices, widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_fields = []  # Lista para agrupar los campos de los servidores
        # Ordenamos los servidores por apellido y nombre para una lista consistente
        servers = Server.objects.all().order_by('surname', 'name')
        for server in servers:
            # Creamos un campo booleano (checkbox) para cada servidor.
            # El nombre del campo es único para poder identificarlo en la vista.
            field_name = f'server_{server.pk}'
            self.fields[field_name] = forms.BooleanField(
                label=f"{server.surname}, {server.name}",
                required=False,
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input me-2'})
            )
            # Añadimos el campo a nuestra lista para renderizarlo fácilmente en la plantilla
            self.server_fields.append(self[field_name])

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

class MinistryForm(forms.ModelForm):
    class Meta:
        model = Ministry
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
