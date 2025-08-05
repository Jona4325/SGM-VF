from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Coordinator, Group, Server, Assistance
from .forms import CoordinatorForm, GroupForm, ServerForm, AssistanceForm,AssistanceUpdateForm

from django.contrib import messages
# Create your views here.
@login_required
def index(request):
    """
    Vista para la página principal de la aplicación Academia.

    Args:
        request: El objeto HttpRequest.

    Returns:
        HttpResponse: La respuesta HTTP con el contenido de la página.
    """
    return render(request, 'alabanza/index.html')

class CoordinatorListView(LoginRequiredMixin,ListView):
    model = Coordinator
    template_name = 'alabanza/coordinator_list.html' # Especifica tu template
    context_object_name = 'coordinators' # Nombre del objeto en el contexto del template

class CoordinatorCreateView(LoginRequiredMixin,CreateView):
    model = Coordinator
    form_class = CoordinatorForm
    template_name = 'alabanza/coordinator_form.html' # Template para crear/editar
    success_url = reverse_lazy('alabanza:coordinator_list') # Redirige después de crear

class CoordinatorUpdateView(LoginRequiredMixin,UpdateView):
    model = Coordinator
    form_class = CoordinatorForm
    template_name = 'alabanza/coordinator_form.html'
    success_url = reverse_lazy('alabanza:coordinator_list')

class CoordinatorDeleteView(LoginRequiredMixin,DeleteView):
    model = Coordinator
    template_name = 'alabanza/coordinator_confirm_delete.html' # Template de confirmación
    success_url = reverse_lazy('alabanza:coordinator_list')


# Views para CRUD de Group
class GroupListView(LoginRequiredMixin,ListView):
    model = Group
    template_name = 'alabanza/group_list.html'
    context_object_name = 'groups'

class GroupCreateView(LoginRequiredMixin,CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'alabanza/group_form.html'
    success_url = reverse_lazy('alabanza:group_list')

class GroupUpdateView(LoginRequiredMixin,UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'alabanza/group_form.html'
    success_url = reverse_lazy('alabanza:group_list')

class GroupDeleteView(LoginRequiredMixin,DeleteView):
    model = Group
    template_name = 'alabanza/group_confirm_delete.html'
    success_url = reverse_lazy('alabanza:group_list')    

# Vista para el CRUD de Server
class ServerListView(LoginRequiredMixin,ListView):
    model = Server
    template_name = 'alabanza/server_list.html'
    context_object_name = 'servers'

class ServerCreateView(LoginRequiredMixin,CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'alabanza/server_form.html'
    success_url = reverse_lazy('alabanza:server_list')

class ServerUpdateView(LoginRequiredMixin,UpdateView):
    model = Server
    form_class = ServerForm
    template_name = 'alabanza/server_form.html'
    success_url = reverse_lazy('alabanza:server_list')

class ServerDeleteView(LoginRequiredMixin,DeleteView):
    model = Server
    template_name = 'alabanza/server_confirm_delete.html'
    success_url = reverse_lazy('alabanza:server_list')

# Crud para assistance
class AssistanceListView(LoginRequiredMixin,ListView):
    model = Assistance
    template_name = 'alabanza/assistance_list.html'
    context_object_name = 'assistance_list'

class AssistanceCreateView(LoginRequiredMixin,CreateView):
    model = Assistance
    form_class = AssistanceForm
    template_name = 'alabanza/assistance_form.html'
    success_url = reverse_lazy('alabanza:assistance_list')

    def form_valid(self, form):
        # Cuando form_valid es llamado, el formulario ya ha sido validado.
        # Los campos requeridos como 'date' estarán presentes en form.cleaned_data.
        assistance_date = form.cleaned_data['date']

        servers_assisted_count = 0
        # Iterar sobre los campos del formulario para encontrar las asistencias marcadas
        for field_name, was_attended in form.cleaned_data.items():
            if field_name.startswith('server_') and was_attended: # Procesar solo campos de servidor marcados como asistidos
                try:
                    # Extraer el ID del servidor del nombre del campo (ej: 'server_1' -> '1')
                    server_id_str = field_name.split('_')[-1]
                    server_id = int(server_id_str)
                    
                    # Crear el registro de asistencia
                    Assistance.objects.create(
                        server_id=server_id, 
                        date=assistance_date, 
                        attended=True # 'was_attended' es True en esta rama del if
                    )
                    servers_assisted_count += 1
                except ValueError:
                    # Esto ocurriría si server_id_str no es un entero.
                    messages.warning(self.request, f"Error al procesar el campo de asistencia: {field_name}. ID de servidor no numérico.")
                except Server.DoesNotExist: # Capturar si el server_id no corresponde a un Server existente
                    messages.warning(self.request, f"Servidor con ID '{server_id_str}' no encontrado para el campo {field_name}.")
        
        if servers_assisted_count > 0:
            messages.success(self.request, f"{servers_assisted_count} asistencia(s) registrada(s) exitosamente.")
        else:
            messages.info(self.request, "No se marcó ninguna asistencia para registrar.")

        # Redirigir a la URL de éxito directamente.
        return HttpResponseRedirect(str(self.success_url))
    
class AssistanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Assistance
    form_class = AssistanceUpdateForm
    template_name = 'alabanza/assistance_update_form.html'
    success_url = reverse_lazy('alabanza:assistance_list')

class AssistanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Assistance
    template_name = 'alabanza/assistance_confirm_delete.html'
    success_url = reverse_lazy('alabanza:assistance_list')    