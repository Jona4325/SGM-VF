
from django import forms
from .models import (
    coordinator, group, server,  child, assistance, GroupCoordinator,

)


class CoordinatorForm(forms.ModelForm):
    class Meta:
        model = coordinator
        fields = ['name', 'surname']
        labels = {
            'name': 'Nombre',
            'surname': 'Apellido',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = group
        fields = ['name', 'description']        
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ServerForm(forms.ModelForm):
    class Meta:
        model = server
        fields = ['name', 'surname', 'coordinator', 'group']
        # Opcional: Personalizar etiquetas si lo deseas
        labels = {
            'name': 'Nombre',
            'surname': 'Apellido',
            'coordinator': 'Coordinador(a)',
            'group': 'Grupo',
        }
        # Opcional: Añadir widgets si necesitas más control (ej. selects más bonitos)
        widgets = {
             'coordinator': forms.Select(attrs={'class': 'form-control'}),
             'group': forms.Select(attrs={'class': 'form-control'}),
        }


class ChildForm(forms.ModelForm): # <-- Renombrada
    class Meta:
        model = child # <-- Cambiado a child
        fields = ['name', 'surname', 'birthday', 'parent_name', 'contact_phone', 'status']
        # ... (labels y widgets como los tenías, asegúrate que las claves coinciden con los fields) ...
        labels = {
            'name': 'Nombre',
            'surname': 'Apellido',
            'birthday': 'Fecha de Nacimiento',
            'parent_name': 'Nombre del Padre/Madre/Representante',
            'contact_phone': 'Teléfono de Contacto',
            'status': 'Estado',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'tel'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
class AssistanceForm(forms.ModelForm):
    class Meta:
        model = assistance
        fields = ['child', 'date', 'group', 'coordinator', 'attended']
        labels = {
            'child': 'Niño/a',
            'date': 'Fecha de Asistencia',
            'group': 'Grupo (en esa fecha)',
            'coordinator': 'Coordinador(a) (en esa fecha)',
            'attended': '¿Asistió?',
        }
        widgets = {
            # Usar Select para las ForeignKeys
            'child': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # Corregido para DateField
            'group': forms.Select(attrs={'class': 'form-control'}),
            'coordinator': forms.Select(attrs={'class': 'form-control'}),
            # Checkbox para el BooleanField
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    # Opcional: Ordenar los desplegables para mejor usabilidad
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar niños por apellido y nombre
        self.fields['child'].queryset = child.objects.order_by('surname', 'name')
        # Ordenar grupos por nombre
        self.fields['group'].queryset = group.objects.order_by('name')
        # Ordenar coordinadores por apellido y nombre
        self.fields['coordinator'].queryset = coordinator.objects.order_by('surname', 'name')
        # El campo 'date' es un DateField, no necesita un queryset.
        # Si antes había una línea como self.fields['date'].queryset = ..., debe eliminarse.

class BatchAssistanceForm(forms.Form):
    date = forms.DateField(
        label="Fecha de Asistencia",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text="Seleccione la fecha para la cual se registrará la asistencia."
    )
    group = forms.ModelChoiceField(
        queryset=group.objects.all().order_by('name'),
        label="Grupo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    coordinator = forms.ModelChoiceField(
        queryset=coordinator.objects.all().order_by('surname', 'name'),
        label="Coordinador(a)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class GroupCoordinatorForm(forms.ModelForm):
    class Meta:
        model = GroupCoordinator
        fields = ['group', 'coordinator']
        labels = {
            'group': 'Grupo',
            'coordinator': 'Coordinador(a)',
        }
        widgets = {
            'group': forms.Select(attrs={'class': 'form-control'}),
            'coordinator': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = group.objects.order_by('name')
        self.fields['coordinator'].queryset = coordinator.objects.order_by('surname', 'name')
