# c:\Proyectos\pusuqui\iap\pusukids\forms.py
from django import forms
from .models import (
    coordinator, group, server, groupage, child, assistance, fecha, GroupCoordinator,
    weekinfo, expense
)
from datetime import date as datetime_date # Renombrar para evitar conflicto con el modelo fecha

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

class GroupageForm(forms.ModelForm):
    class Meta:
        model = groupage
        fields = ['name', 'description']


class ChildForm(forms.ModelForm): # <-- Renombrada
    class Meta:
        model = child # <-- Cambiado a child
        fields = ['name', 'surname', 'birthday', 'groupage', 'parent_name', 'contact_phone', 'status']
        # ... (labels y widgets como los tenías, asegúrate que las claves coinciden con los fields) ...
        labels = {
            'name': 'Nombre',
            'surname': 'Apellido',
            'birthday': 'Fecha de Nacimiento',
            'groupage': 'Grupo de Edad',
            'parent_name': 'Nombre del Padre/Madre/Representante',
            'contact_phone': 'Teléfono de Contacto',
            'status': 'Estado',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'groupage': forms.Select(attrs={'class': 'form-control'}),
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
            'date': forms.Select(attrs={'class': 'form-control'}),
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
        # Ordenar fechas por la más reciente primero
        self.fields['date'].queryset = fecha.objects.order_by('-date')
        # Ordenar grupos por nombre
        self.fields['group'].queryset = group.objects.order_by('name')
        # Ordenar coordinadores por apellido y nombre
        self.fields['coordinator'].queryset = coordinator.objects.order_by('surname', 'name')

class WeekinfoForm(forms.ModelForm):
    class Meta:
        model = weekinfo
        fields = ['fecha', 'group', 'coordinator', 'total_kids', 'total_servers', 'money_collected']
        labels = {
            'fecha': 'Fecha (Semana)',
            'group': 'Grupo',
            'coordinator': 'Coordinador(a)',
            'total_kids': 'Total Niños Asistentes',
            'total_servers': 'Total Servidores Presentes',
            'money_collected': 'Dinero Recolectado (€/$) ', # Ajusta el símbolo de moneda
        }
        widgets = {
            'fecha': forms.Select(attrs={'class': 'form-control'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
            'coordinator': forms.Select(attrs={'class': 'form-control'}),
            # Usar NumberInput para campos numéricos
            'total_kids': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'total_servers': forms.NumberInput(attrs={'class': 'form-control', 'step': '1'}),
            'money_collected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}), # step para decimales
        }

    # Ordenar desplegables
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].queryset = fecha.objects.order_by('-date')
        self.fields['group'].queryset = group.objects.order_by('name')
        self.fields['coordinator'].queryset = coordinator.objects.order_by('surname', 'name')

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = expense
        fields = ['description', 'amount', 'fecha', 'reference', 'transdate']
        labels = {
            'description': 'Descripción del Gasto',
            'amount': 'Monto (€/$)', # Ajusta el símbolo de moneda si es necesario
            'fecha': 'Fecha (Semana del Gasto)',
            'reference': 'Referencia (Factura, Ticket, etc.)',
            'transdate': 'Fecha de Transacción (Opcional)', # <-- Nueva etiqueta
        }
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fecha': forms.Select(attrs={'class': 'form-control'}),
            'reference': forms.TextInput(attrs={'class': 'form-control'}),
            'transdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # <-- Nuevo widget        
        }

    # Ordenar desplegable de fecha
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha'].queryset = fecha.objects.order_by('-date')        

class BatchAssistanceForm(forms.Form):
    date = forms.ModelChoiceField(
        queryset=fecha.objects.none(), # Queryset inicial vacío, se llenará en __init__
        label="Fecha de Asistencia",
        widget=forms.Select(attrs={'class': 'form-control'})
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = datetime_date.today()
        self.fields['date'].queryset = fecha.objects.filter(
            date__year=today.year,
            date__month=today.month
        ).order_by('-date')

class FechaForm(forms.ModelForm):
    class Meta:
        model = fecha
        fields = ['date'] # Asumiendo que el campo principal es 'date'
        labels = {
            'date': 'Fecha (Inicio de Semana)',
        }
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }        

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