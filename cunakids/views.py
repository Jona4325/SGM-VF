from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import (
    coordinator, group, server, child, assistance, GroupCoordinator,
)
from django.db import IntegrityError
from django.db.models.deletion import ProtectedError
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import date
from .forms import (
    CoordinatorForm, GroupForm, ServerForm, ChildForm, AssistanceForm, GroupCoordinatorForm,
    BatchAssistanceForm # <-- Añadir BatchAssistanceForm
)
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import Lower, Trim
import traceback # Para debug si es necesario

# Create your views here.


class PaginationQueryMixin:
    """Agrega querystring de filtros (sin page) para construir enlaces de paginación."""

    def get_pagination_querystring(self):
        params = self.request.GET.copy()
        params.pop('page', None)
        querystring = params.urlencode()
        return f"&{querystring}" if querystring else ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagination_query'] = self.get_pagination_querystring()
        return context


def get_pagination_query(request):
    params = request.GET.copy()
    params.pop('page', None)
    querystring = params.urlencode()
    return f"&{querystring}" if querystring else ""


def paginate_queryset(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def get_active_children_queryset():
    """Normaliza el estado para soportar datos heredados (ej. Activo/ ACTIVO )."""
    return child.objects.annotate(
        status_normalized=Lower(Trim('status'))
    ).filter(status_normalized='activo')

def calculated_age(born):
    if not born: return None
    today = date.today()
    age = today.year - born.year
    if (today.month, today.day) < (born.month, born.day): age -= 1
    return age
@login_required
def index(request):
    """
    Vista para la página principal de la aplicación Academia.

    Args:
        request: El objeto HttpRequest.

    Returns:
        HttpResponse: La respuesta HTTP con el contenido de la página.
    """
    return render(request, 'cunakids/index.html')

@login_required
def coordinator_list(request):
    """
    Vista para listar todos los coordinadores.
    
    Args:
        request: El objeto HttpRequest.
    Returns:
    """
    coordinators = coordinator.objects.order_by('surname', 'name')
    page_obj = paginate_queryset(request, coordinators, per_page=10)
    return render(request, 'cunakids/coordinator_list.html', {
        'coordinators': page_obj,
        'page_obj': page_obj,
        'pagination_query': get_pagination_query(request),
    })

@login_required
def coordinator_create(request):
    """
    Vista para crear un nuevo coordinador.
    """
    if request.method == 'POST':
        form = CoordinatorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coordinador registrado exitosamente.')
            return redirect('cunakids:coordinator_list')
    else:
        form = CoordinatorForm()
    return render(request, 'cunakids/coordinator_form.html', {
        'form': form,
        'action': 'Crear',
        'form_title': 'Registrar Coordinador',
        'submit_button_text': 'Guardar',
    })

@login_required
def coordinator_update(request, pk):
    """
    Vista para actualizar un coordinador existente.
    """
    coordinator_obj = get_object_or_404(coordinator, pk=pk)
    if request.method == 'POST':
        form = CoordinatorForm(request.POST, instance=coordinator_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coordinador actualizado exitosamente.')
            return redirect('cunakids:coordinator_list')
    else:
        form = CoordinatorForm(instance=coordinator_obj)
    return render(request, 'cunakids/coordinator_form.html', {
        'form': form,
        'action': 'Actualizar',
        'form_title': f'Editar Coordinador: {coordinator_obj.name} {coordinator_obj.surname}',
        'submit_button_text': 'Actualizar',
    })

@login_required
def coordinator_delete(request, pk):
    """
    Vista para eliminar un coordinador.
    """
    coordinator_obj = get_object_or_404(coordinator, pk=pk)
    if request.method == 'POST':
        try:
            coordinator_obj.delete()
            messages.success(request, 'Coordinador eliminado exitosamente.')
            return redirect('cunakids:coordinator_list')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar este coordinador porque tiene registros relacionados '
                '(asistencias o servidores). Elimina primero esas relaciones.'
            )
            return redirect('cunakids:coordinator_list')
    return render(request, 'cunakids/coordinator_confirm_delete.html', {'coordinator': coordinator_obj})

# vista para crear groups
@login_required
def group_list(request):
    groups = group.objects.order_by('name')
    page_obj = paginate_queryset(request, groups, per_page=10)
    return render(request, 'cunakids/group_list.html', {
        'groups': page_obj,
        'page_obj': page_obj,
        'pagination_query': get_pagination_query(request),
    })

@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo registrado exitosamente.')
            return redirect('cunakids:group_list')
    else:
        form = GroupForm()
    return render(request, 'cunakids/group_form.html', {
        'form': form,
        'form_title': 'Registrar Nuevo Grupo',
        'submit_button_text': 'Guardar',
    })

@login_required
def group_update(request, pk):
    group_obj = get_object_or_404(group, pk=pk) 
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo actualizado exitosamente.')
            return redirect('cunakids:group_list')
    else:
        form = GroupForm(instance=group_obj)
    return render(request, 'cunakids/group_form.html', {
        'form': form,
        'form_title': f'Editar Grupo: {group_obj.name}',
        'submit_button_text': 'Actualizar',
    })

@login_required
def group_delete(request, pk):
    group_obj = get_object_or_404(group, pk=pk)
    if request.method == 'POST':
        group_obj.delete()
        return redirect('cunakids:group_list')
    return render(request, 'cunakids/group_confirm_delete.html', {'group': group_obj})

class ServerListView(PaginationQueryMixin, LoginRequiredMixin, ListView):
    model = server
    template_name = 'cunakids/server_list.html'  # Especifica tu template
    context_object_name = 'servers'  # Nombre de la variable en el template
    paginate_by = 10

class ServerDetailView(LoginRequiredMixin,DetailView):
    model = server
    template_name = 'cunakids/server_detail.html'
    context_object_name = 'server'

class ServerCreateView(LoginRequiredMixin,CreateView):
    model = server
    form_class = ServerForm
    template_name = 'cunakids/server_form.html'
    success_url = reverse_lazy('cunakids:server_list') # Redirige a la lista después de crear

    # Opcional: Añadir contexto extra al template del formulario si es necesario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Registrar Nuevo Servidor'
        context['submit_button_text'] = 'Registrar'
        return context

class ServerUpdateView(LoginRequiredMixin,UpdateView):
    model = server
    form_class = ServerForm
    template_name = 'cunakids/server_form.html'
    success_url = reverse_lazy('cunakids:server_list') # Redirige a la lista después de actualizar

    # Opcional: Añadir contexto extra al template del formulario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Editar Servidor: {self.object.name} {self.object.surname}'
        context['submit_button_text'] = 'Actualizar'
        return context

class ServerDeleteView(LoginRequiredMixin,DeleteView):
    model = server
    template_name = 'cunakids/server_confirm_delete.html'
    context_object_name = 'server'
    success_url = reverse_lazy('cunakids:server_list') # Redirige a la lista después de borrar

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Servidor eliminado exitosamente.')
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar este servidor porque tiene registros relacionados protegidos.'
            )
        except IntegrityError:
            messages.error(
                request,
                'No se pudo eliminar el servidor por una restricción de integridad en la base de datos.'
            )
        return redirect(self.success_url)

# --- Vistas para el CRUD de Kid ---
@login_required
def child_list(request):
    """Vista para listar todos los niños."""
    # Obtén el queryset directamente
    children_list = child.objects.all().order_by('surname', 'name')
    page_obj = paginate_queryset(request, children_list, per_page=10)

    # Pasa el queryset directamente al template.
    # La propiedad @property calculated_age estará disponible en cada objeto 'c' dentro del template.
    return render(request, 'cunakids/child_list.html', {
        'children': page_obj,
        'page_obj': page_obj,
        'pagination_query': get_pagination_query(request),
    })
@login_required
def child_create(request): # <-- Renombrada
    """Vista para crear un nuevo niño."""
    if request.method == 'POST':
        form = ChildForm(request.POST) # <-- Cambiado
        if form.is_valid():
            form.save()
            messages.success(request, 'Niño registrado exitosamente.')
            return redirect('cunakids:child_list')
    else:
        form = ChildForm() # <-- Cambiado
    # Asegúrate que el template existe o renómbralo
    return render(request, 'cunakids/child_form.html', {
        'form': form,
        'action': 'Registrar',
        'form_title': 'Registrar Niño',
        'submit_button_text': 'Guardar',
    }) # <-- Cambiado template

@login_required
def child_update(request, pk): # <-- Renombrada
    """Vista para actualizar un niño existente."""
    child_obj = get_object_or_404(child, pk=pk) # <-- Cambiado
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child_obj) # <-- Cambiado
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro del niño actualizado exitosamente.')
            return redirect('cunakids:child_list') # <-- Cambiado
    else:
        form = ChildForm(instance=child_obj) # <-- Cambiado
    current_age = calculated_age(child_obj.birthday) if child_obj.birthday else "N/A"
    action_title = f"Editar Niño: {child_obj.name} {child_obj.surname} (Edad: {current_age})"
    # Asegúrate que el template existe o renómbralo
    return render(request, 'cunakids/child_form.html', {
        'form': form,
        'action': 'Actualizar',
        'action_title': action_title,
        'form_title': action_title,
        'submit_button_text': 'Actualizar',
    }) # <-- Cambiado template

@login_required
def child_delete(request, pk): # <-- Renombrada
    """Vista para eliminar un niño."""
    child_obj = get_object_or_404(child, pk=pk) # <-- Cambiado
    if request.method == 'POST':
        child_obj.delete()
        return redirect('cunakids:child_list') # <-- Cambiado
    # Asegúrate que el template existe o renómbralo
    return render(request, 'cunakids/child_confirm_delete.html', {'child': child_obj}) # <-- Cambiado template y contexto


# --- Vistas para el CRUD de Assistance ---
@login_required
def assistance_list(request):
    """Vista para listar todos los registros de asistencia."""
    search_surname = request.GET.get('surname', '').strip()
    search_date = request.GET.get('date', '').strip()

    # Optimizar consulta usando select_related para cargar datos relacionados
    assistances_list = assistance.objects.select_related(
        'child', 'group', 'coordinator'  # 'date' no es una relación
    ).order_by('-date', '-child__surname', '-child__name') # Ordenar en descendente por fecha y niño

    if search_surname:
        assistances_list = assistances_list.filter(child__surname__icontains=search_surname)
    if search_date:
        assistances_list = assistances_list.filter(date=search_date)

    page_obj = paginate_queryset(request, assistances_list, per_page=15)
    return render(request, 'cunakids/assistance_list.html', {
        'assistances': page_obj,
        'page_obj': page_obj,
        'search_surname': search_surname,
        'search_date': search_date,
        'pagination_query': get_pagination_query(request),
    })

@login_required
def assistance_create(request):
    """
    Vista para crear registros de asistencia en lote para todos los niños ACTIVOS.
    """
    # Filtrar para incluir solo niños con estado 'activo'
    children_list = get_active_children_queryset().order_by('surname', 'name')

    if request.method == 'POST':
        form = BatchAssistanceForm(request.POST)
        if form.is_valid():
            date_obj = form.cleaned_data['date']
            group_obj = form.cleaned_data['group']
            coordinator_obj = form.cleaned_data['coordinator']

            assistances_to_create = []
            for child_obj in children_list:
                # El valor 'on' es el que envía un checkbox HTML cuando está marcado
                attended = request.POST.get(f'attended_{child_obj.pk}') == 'on'
                assistances_to_create.append(
                    assistance(
                        tenant=child_obj.tenant,
                        child=child_obj,
                        date=date_obj,
                        group=group_obj,
                        coordinator=coordinator_obj,
                        attended=attended
                    )
                )
            try:
                if assistances_to_create:
                    # ignore_conflicts=True podría ser una opción, pero es mejor notificar el error.
                    assistance.objects.bulk_create(assistances_to_create)
                messages.success(request, 'Asistencias registradas exitosamente.')
                return redirect('cunakids:assistance_list')
            except IntegrityError:
                # Esto ocurre si se intenta registrar una asistencia para un niño en una fecha que ya existe.
                messages.error(request, 'Error: Ya existe un registro de asistencia para uno o más niños en la fecha seleccionada. No se guardó ningún registro.')
                # Volvemos a renderizar el formulario con los datos que el usuario ya había llenado
                return render(request, 'cunakids/assistance_batch_form.html', {
                    'form': form,
                    'children': children_list,
                    'action_title': 'Registrar Asistencia Grupal'
                })
    else:
        form = BatchAssistanceForm()

    return render(request, 'cunakids/assistance_batch_form.html', {
        'form': form,
        'children': children_list,
        'action_title': 'Registrar Asistencia Grupal',
    })

@login_required
def assistance_update(request, pk):
    """Vista para actualizar un registro de asistencia existente."""
    assistance_obj = get_object_or_404(assistance, pk=pk)
    if request.method == 'POST':
        form = AssistanceForm(request.POST, instance=assistance_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro de asistencia actualizado.')
            return redirect('cunakids:assistance_list')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AssistanceForm(instance=assistance_obj)

    # Crear un título descriptivo
    action_title = (
        f"Editar Asistencia: {assistance_obj.child.name} {assistance_obj.child.surname} "
        f"({assistance_obj.date.strftime('%Y-%m-%d')})"
    )
    return render(request, 'cunakids/assistance_form.html', {
        'form': form,
        'action': 'Actualizar',
        'action_title': action_title,
        'submit_button_text': 'Actualizar',
    })

@login_required
def assistance_delete(request, pk):
    """Vista para eliminar un registro de asistencia."""
    assistance_obj = get_object_or_404(assistance.objects.select_related('child', 'group', 'coordinator'), pk=pk)
    if request.method == 'POST':
        try:
            assistance_obj.delete()
            messages.success(request, 'Registro de asistencia eliminado.')
            return redirect('cunakids:assistance_list')
        except IntegrityError as e:
             # Esto podría ocurrir si otro objeto depende de este registro de asistencia y tiene on_delete=PROTECT.
             messages.error(request, f'No se pudo eliminar el registro debido a una restricción de la base de datos: {e}')
             return render(request, 'cunakids/assistance_confirm_delete.html', {
                 'assistance': assistance_obj,
             })

    return render(request, 'cunakids/assistance_confirm_delete.html', {'assistance': assistance_obj})

# --- Vistas para el CRUD de GroupCoordinator (Cunakids) ---
@login_required
def groupcoordinator_list(request):
    """Vista para listar todas las asignaciones de grupo-coordinador."""
    assignments = GroupCoordinator.objects.select_related('group', 'coordinator').order_by('group__name', 'coordinator__surname')
    page_obj = paginate_queryset(request, assignments, per_page=10)
    return render(request, 'cunakids/groupcoordinator_list.html', {
        'assignments': page_obj,
        'page_obj': page_obj,
        'pagination_query': get_pagination_query(request),
    })

@login_required
def groupcoordinator_create(request):
    """Vista para crear una nueva asignación."""
    if request.method == 'POST':
        form = GroupCoordinatorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Asignación creada exitosamente.')
                return redirect('cunakids:groupcoordinator_list')
            except IntegrityError:
                messages.error(request, 'Error: Esta asignación de grupo y coordinador ya existe.')
    else:
        form = GroupCoordinatorForm()
    return render(request, 'cunakids/groupcoordinator_form.html', {
        'form': form,
        'action': 'Asignar',
        'action_title': 'Asignar Coordinador a Grupo',
        'submit_button_text': 'Guardar',
    })

@login_required
def groupcoordinator_update(request, pk):
    """Vista para actualizar una asignación."""
    assignment = get_object_or_404(GroupCoordinator, pk=pk)
    if request.method == 'POST':
        form = GroupCoordinatorForm(request.POST, instance=assignment)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Asignación actualizada exitosamente.')
                return redirect('cunakids:groupcoordinator_list')
            except IntegrityError:
                messages.error(request, 'Error: Esta asignación de grupo y coordinador ya existe.')
    else:
        form = GroupCoordinatorForm(instance=assignment)
    
    action_title = f"Editar Asignación: {assignment}"
    return render(request, 'cunakids/groupcoordinator_form.html', {
        'form': form, 
        'action': 'Actualizar', 
        'action_title': action_title,
        'submit_button_text': 'Actualizar',
    })

@login_required
def groupcoordinator_delete(request, pk):
    """Vista para eliminar una asignación."""
    assignment = get_object_or_404(GroupCoordinator.objects.select_related('group', 'coordinator'), pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Asignación eliminada exitosamente.')
        return redirect('cunakids:groupcoordinator_list')
    return render(request, 'cunakids/groupcoordinator_confirm_delete.html', {'assignment': assignment})
