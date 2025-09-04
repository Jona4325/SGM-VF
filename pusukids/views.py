from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import (
    coordinator, group, server, groupage, child, assistance, fecha, GroupCoordinator,
    weekinfo, expense
)
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from datetime import date
from .forms import (
    CoordinatorForm, GroupForm, ServerForm, GroupageForm, ChildForm,
    AssistanceForm, WeekinfoForm, ExpenseForm, FechaForm, GroupCoordinatorForm,
    BatchAssistanceForm
)
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import ProtectedError, Q
import traceback # Para debug si es necesario

# Create your views here.

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
    return render(request, 'pusukids/index.html')

@login_required
def coordinator_list(request):
    """
    Vista para listar todos los coordinadores.
    
    Args:
        request: El objeto HttpRequest.
    Returns:
    """
    print("pase por aqui")
    coordinators = coordinator.objects.all()
    print(coordinators)
    return render(request, 'pusukids/coordinator_list.html', {'coordinators': coordinators})

@login_required
def coordinator_create(request):
    """
    Vista para crear un nuevo coordinador.
    """
    if request.method == 'POST':
        form = CoordinatorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pusukids:coordinator_list')
    else:
        form = CoordinatorForm()
    return render(request, 'pusukids/coordinator_form.html', {'form': form, 'action': 'Crear'})

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
            return redirect('pusukids:coordinator_list')
    else:
        form = CoordinatorForm(instance=coordinator_obj)
    return render(request, 'pusukids/coordinator_form.html', {'form': form, 'action': 'Actualizar'})

@login_required
def coordinator_delete(request, pk):
    """
    Vista para eliminar un coordinador.
    """
    coordinator_obj = get_object_or_404(coordinator, pk=pk)
    if request.method == 'POST':
        coordinator_obj.delete()
        return redirect('pusukids:coordinator_list')
    return render(request, 'pusukids/coordinator_confirm_delete.html', {'coordinator': coordinator_obj})

# vista para crear groups
@login_required
def group_list(request):
    groups = group.objects.all()
    return render(request, 'pusukids/group_list.html', {'groups': groups})

@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pusukids:group_list')
    else:
        form = GroupForm()
    return render(request, 'pusukids/group_form.html', {'form': form})

@login_required
def group_update(request, pk):
    group_obj = get_object_or_404(group, pk=pk) 
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group_obj)
        if form.is_valid():
            form.save()
            return redirect('pusukids:group_list')
    else:
        form = GroupForm(instance=group_obj)
    return render(request, 'pusukids/group_form.html', {'form': form})

@login_required
def group_delete(request, pk):
    group_obj = get_object_or_404(group, pk=pk)
    if request.method == 'POST':
        group_obj.delete()
        return redirect('pusukids:group_list')
    return render(request, 'pusukids/group_confirm_delete.html', {'group': group_obj})

class ServerListView(LoginRequiredMixin,ListView):
    model = server
    template_name = 'pusukids/server_list.html'  # Especifica tu template
    context_object_name = 'servers'  # Nombre de la variable en el template

class ServerDetailView(LoginRequiredMixin,DetailView):
    model = server
    template_name = 'pusukids/server_detail.html'
    context_object_name = 'server'

class ServerCreateView(LoginRequiredMixin,CreateView):
    model = server
    form_class = ServerForm
    template_name = 'pusukids/server_form.html'
    success_url = reverse_lazy('pusukids:server_list') # Redirige a la lista después de crear

    # Opcional: Añadir contexto extra al template del formulario si es necesario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Registrar Nuevo Servidor'
        context['submit_button_text'] = 'Registrar'
        return context

class ServerUpdateView(LoginRequiredMixin,UpdateView):
    model = server
    form_class = ServerForm
    template_name = 'pusukids/server_form.html'
    success_url = reverse_lazy('pusukids:server_list') # Redirige a la lista después de actualizar

    # Opcional: Añadir contexto extra al template del formulario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Editar Servidor: {self.object.name} {self.object.surname}'
        context['submit_button_text'] = 'Actualizar'
        return context

class ServerDeleteView(LoginRequiredMixin,DeleteView):
    model = server
    template_name = 'pusukids/server_confirm_delete.html'
    context_object_name = 'server'
    success_url = reverse_lazy('pusukids:server_list') # Redirige a la lista después de borrar

# --- Vistas para el CRUD de GroupAge (Refactorizadas a CBV) ---
class GroupageListView(LoginRequiredMixin, ListView):
    model = groupage
    template_name = 'pusukids/groupage_list.html'
    context_object_name = 'groupages'

class GroupageCreateView(LoginRequiredMixin, CreateView):
    model = groupage
    form_class = GroupageForm
    template_name = 'pusukids/groupage_form.html'
    success_url = reverse_lazy('pusukids:groupage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Crear'
        context['action_title'] = 'Registrar Nuevo Grupo de Edad'
        return context

class GroupageUpdateView(LoginRequiredMixin, UpdateView):
    model = groupage
    form_class = GroupageForm
    template_name = 'pusukids/groupage_form.html'
    success_url = reverse_lazy('pusukids:groupage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Actualizar'
        context['action_title'] = f'Editar Grupo de Edad: {self.object.name}'
        return context

class GroupageDeleteView(LoginRequiredMixin, DeleteView):
    model = groupage
    template_name = 'pusukids/groupage_confirm_delete.html'
    context_object_name = 'groupage'
    success_url = reverse_lazy('pusukids:groupage_list')

# --- Vistas para el CRUD de Kid ---
@login_required
def child_list(request):
    """Vista para listar todos los niños."""
    # Por defecto, mostrar solo los niños activos.
    # Se puede pasar un parámetro GET ?status=all para ver todos, o ?status=promovido.
    status_filter = request.GET.get('status', 'activo')
    search_query = request.GET.get('q', '')
    groupage_filter_id = request.GET.get('groupage', '')

    if status_filter == 'all':
        children_list = child.objects.all()
    else:
        # Filtra por el estado solicitado ('activo', 'promovido', etc.)
        children_list = child.objects.filter(status=status_filter)
        
    # Aplicar filtro de búsqueda si existe
    if search_query:
        children_list = children_list.filter(
            Q(name__icontains=search_query) | Q(surname__icontains=search_query)
        )
        # Aplicar filtro de grupo de edad si existe
    if groupage_filter_id and groupage_filter_id.isdigit():
        children_list = children_list.filter(groupage_id=groupage_filter_id)

    children_list = children_list.order_by('surname', 'name')    

    # Paginación
    paginator = Paginator(children_list, 10) # 10 niños por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener todos los grupos de edad para los botones de filtro
    all_groupages = groupage.objects.all().order_by('name')

    # La propiedad @property calculated_age estará disponible en cada objeto 'c' dentro del template.
    return render(request, 'pusukids/child_list.html', {
        'page_obj': page_obj, 
        'current_status': status_filter,
        'search_query': search_query,
        'all_groupages': all_groupages,
        'current_groupage_id': int(groupage_filter_id) if groupage_filter_id and groupage_filter_id.isdigit() else None,
    })

@login_required
def child_create(request): # <-- Renombrada
    """Vista para crear un nuevo niño."""
    if request.method == 'POST':
        form = ChildForm(request.POST) # <-- Cambiado
        if form.is_valid():
            new_child = form.save()
            messages.success(request, f"El niño/a '{new_child}' ha sido registrado/a exitosamente.")
            return redirect('pusukids:child_list') # <-- Cambiado
        else:
            # El error de 'unique_together' se mostrará automáticamente en el formulario.
            # Añadimos un mensaje general para mayor claridad.
            messages.error(request, 'No se pudo registrar al niño. Por favor, revisa los errores en el formulario.')
    else:
        form = ChildForm() # <-- Cambiado
    # Asegúrate que el template existe o renómbralo
    return render(request, 'pusukids/child_form.html', {'form': form, 'action': 'Registrar'}) # <-- Cambiado template

@login_required
def child_update(request, pk): # <-- Renombrada
    """Vista para actualizar un niño existente."""
    child_obj = get_object_or_404(child, pk=pk) # <-- Cambiado
    if request.method == 'POST':
        form = ChildForm(request.POST, instance=child_obj) # <-- Cambiado
        if form.is_valid():
            updated_child = form.save()
            messages.success(request, f"Los datos de '{updated_child}' han sido actualizados exitosamente.")
            return redirect('pusukids:child_list') # <-- Cambiado
        else:
            # El error de 'unique_together' se mostrará automáticamente en el formulario.
            # Añadimos un mensaje general para mayor claridad.
            messages.error(request, 'No se pudieron guardar los cambios. Por favor, revisa los errores en el formulario.')
    else:
        form = ChildForm(instance=child_obj) # <-- Cambiado
    current_age = calculated_age(child_obj.birthday) if child_obj.birthday else "N/A"
    action_title = f"Editar Niño: {child_obj.name} {child_obj.surname} (Edad: {current_age})"
    # Asegúrate que el template existe o renómbralo
    return render(request, 'pusukids/child_form.html', {'form': form, 'action': 'Actualizar', 'action_title': action_title}) # <-- Cambiado template

@login_required
def child_delete(request, pk): # <-- Renombrada
    """Vista para eliminar un niño."""
    child_obj = get_object_or_404(child, pk=pk) # <-- Cambiado
    if request.method == 'POST':
        child_obj.delete()
        return redirect('pusukids:child_list') # <-- Cambiado
    # Asegúrate que el template existe o renómbralo
    return render(request, 'pusukids/child_confirm_delete.html', {'child': child_obj}) # <-- Cambiado template y contexto


# --- Vistas para el CRUD de Assistance ---
@login_required
def assistance_list(request):
    """Vista para listar todos los registros de asistencia."""
    # Obtener parámetros de búsqueda del GET request
    search_surname = request.GET.get('surname', '')
    search_date_id = request.GET.get('date_id', '')

    # Optimizar consulta usando select_related para cargar datos relacionados
    assistances_list = assistance.objects.select_related(
        'child', 'date', 'group', 'coordinator'
    ).order_by('-date__date', 'child__surname', 'child__name') # Ordenar por fecha desc, luego por niño

    # Aplicar filtros si existen
    if search_surname:
        assistances_list = assistances_list.filter(child__surname__icontains=search_surname)
    if search_date_id:
        assistances_list = assistances_list.filter(date__id=search_date_id)

    # Obtener las fechas del mes y año actual para el menú desplegable del filtro
    today = date.today()
    available_dates = fecha.objects.filter(
        date__year=today.year,
        date__month=today.month
    ).order_by('-date')

    return render(request, 'pusukids/assistance_list.html', {
        'assistances': assistances_list,
        'available_dates': available_dates,
        'search_surname': search_surname,
        'search_date_id': int(search_date_id) if search_date_id else None,
    })

@login_required
def assistance_create(request):
    """
    Vista para crear registros de asistencia en lote para todos los niños.
    """
    children_list = child.objects.filter(status=child.STATUS_ACTIVO).order_by('surname', 'name')

    if request.method == 'POST':
        form = BatchAssistanceForm(request.POST)
        if form.is_valid():
            date_obj = form.cleaned_data['date']
            group_obj = form.cleaned_data['group']
            coordinator_obj = form.cleaned_data['coordinator']

            assistances_to_create = []
            for child_obj in children_list:
                attended = request.POST.get(f'attended_{child_obj.pk}') == 'on'
                assistances_to_create.append(
                    assistance(
                        child=child_obj,
                        date=date_obj,
                        group=group_obj,
                        coordinator=coordinator_obj,
                        attended=attended
                    )
                )
            
            if assistances_to_create:
                try:
                    assistance.objects.bulk_create(assistances_to_create)
                    messages.success(request, 'Asistencias registradas exitosamente.')
                    return redirect('pusukids:assistance_list')
                except IntegrityError:
                    messages.error(request, 'Error: No se pudo registrar la asistencia. Es probable que ya existan registros para uno o más niños en la fecha seleccionada.')
    else:
        form = BatchAssistanceForm()

    return render(request, 'pusukids/assistance_batch_form.html', {
        'form': form,
        'children': children_list,
        'action_title': 'Registrar Asistencia Grupal'
    })

@login_required
def assistance_update(request, pk):
    """Vista para actualizar un registro de asistencia existente."""
    assistance_obj = get_object_or_404(assistance, pk=pk)
    if request.method == 'POST':
        form = AssistanceForm(request.POST, instance=assistance_obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Registro de asistencia actualizado.')
            return redirect('pusukids:assistance_list')
        # else:
            # messages.error(request, 'Por favor corrige los errores.')
    else:
        form = AssistanceForm(instance=assistance_obj)

    # Crear un título descriptivo
    action_title = (
        f"Editar Asistencia: {assistance_obj.child.name} {assistance_obj.child.surname} "
        f"({assistance_obj.date.date.strftime('%Y-%m-%d')})"
    )
    return render(request, 'pusukids/assistance_form.html', {
        'form': form,
        'action': 'Actualizar',
        'action_title': action_title
    })

@login_required
def assistance_delete(request, pk):
    """Vista para eliminar un registro de asistencia."""
    assistance_obj = get_object_or_404(assistance.objects.select_related('child', 'date'), pk=pk)
    if request.method == 'POST':
        try:
            assistance_obj.delete()
            # messages.success(request, 'Registro de asistencia eliminado.')
            return redirect('pusukids:assistance_list')
        except Exception as e:
             # Manejar error si on_delete=PROTECT impide borrar (aunque aquí no aplica directamente)
             # messages.error(request, f'No se pudo eliminar el registro: {e}')
             # Podrías redirigir a la lista o mostrar el error en la misma página
             return render(request, 'pusukids/assistance_confirm_delete.html', {
                 'assistance': assistance_obj,
                 'error': f'Error al eliminar: {e}'
             })

    return render(request, 'pusukids/assistance_confirm_delete.html', {'assistance': assistance_obj})

@login_required
def weekinfo_list(request):
    """Vista para listar toda la información semanal."""
    weekinfos_list = weekinfo.objects.select_related(
        'fecha', 'group', 'coordinator'
    ).order_by('-fecha__date') # Ordenar por fecha más reciente

    return render(request, 'pusukids/weekinfo_list.html', {'weekinfos': weekinfos_list})

@login_required
def weekinfo_create(request):
    """Vista para crear un nuevo registro de información semanal."""
    if request.method == 'POST':
        form = WeekinfoForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Información semanal registrada exitosamente.')
            return redirect('pusukids:weekinfo_list')
        # else:
            # messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = WeekinfoForm()
    return render(request, 'pusukids/weekinfo_form.html', {'form': form, 'action': 'Registrar'})

@login_required
def weekinfo_update(request, pk):
    """Vista para actualizar un registro de información semanal existente."""
    weekinfo_obj = get_object_or_404(weekinfo, pk=pk)
    if request.method == 'POST':
        form = WeekinfoForm(request.POST, instance=weekinfo_obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Información semanal actualizada.')
            return redirect('pusukids:weekinfo_list')
        # else:
            # messages.error(request, 'Por favor corrige los errores.')
    else:
        form = WeekinfoForm(instance=weekinfo_obj)

    action_title = (
        f"Editar Info Semana: {weekinfo_obj.fecha.date.strftime('%Y-%m-%d')} - "
        f"Grupo: {weekinfo_obj.group.name}"
    )
    return render(request, 'pusukids/weekinfo_form.html', {
        'form': form,
        'action': 'Actualizar',
        'action_title': action_title
    })

@login_required
def weekinfo_delete(request, pk):
    """Vista para eliminar un registro de información semanal."""
    # Incluir related para mostrar info en la confirmación
    weekinfo_obj = get_object_or_404(weekinfo.objects.select_related('fecha', 'group'), pk=pk)
    if request.method == 'POST':
        try:
            weekinfo_obj.delete()
            # messages.success(request, 'Información semanal eliminada.')
            return redirect('pusukids:weekinfo_list')
        except Exception as e:
             # Manejar error si on_delete=PROTECT impide borrar (ej. si expense dependiera de weekinfo)
             # messages.error(request, f'No se pudo eliminar el registro: {e}')
             return render(request, 'pusukids/weekinfo_confirm_delete.html', {
                 'weekinfo': weekinfo_obj,
                 'error': f'Error al eliminar: {e}'
             })

    return render(request, 'pusukids/weekinfo_confirm_delete.html', {'weekinfo': weekinfo_obj})

# --- Vistas para el CRUD de Expense ---
@login_required
def expense_list(request):
    """Vista para listar todos los gastos."""
    expenses_list = expense.objects.select_related('fecha').order_by('-fecha__date', 'description')
    return render(request, 'pusukids/expense_list.html', {'expenses': expenses_list})

@login_required
def expense_create(request):
    """Vista para crear un nuevo registro de gasto."""
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Gasto registrado exitosamente.')
            return redirect('pusukids:expense_list')
        # else:
            # messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ExpenseForm()
    return render(request, 'pusukids/expense_form.html', {'form': form, 'action': 'Registrar'})

@login_required
def expense_update(request, pk):
    """Vista para actualizar un registro de gasto existente."""
    expense_obj = get_object_or_404(expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense_obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Gasto actualizado.')
            return redirect('pusukids:expense_list')
        # else:
            # messages.error(request, 'Por favor corrige los errores.')
    else:
        form = ExpenseForm(instance=expense_obj)

    action_title = (
        f"Editar Gasto: {expense_obj.description} "
        f"({expense_obj.fecha.date.strftime('%Y-%m-%d')})"
    )
    return render(request, 'pusukids/expense_form.html', {
        'form': form,
        'action': 'Actualizar',
        'action_title': action_title
    })

@login_required
def expense_delete(request, pk):
    """Vista para eliminar un registro de gasto."""
    expense_obj = get_object_or_404(expense.objects.select_related('fecha'), pk=pk)
    if request.method == 'POST':
        try:
            expense_obj.delete()
            # messages.success(request, 'Gasto eliminado.')
            return redirect('pusukids:expense_list')
        except Exception as e:
             # messages.error(request, f'No se pudo eliminar el registro: {e}')
             return render(request, 'pusukids/expense_confirm_delete.html', {
                 'expense': expense_obj,
                 'error': f'Error al eliminar: {e}'
             })
    return render(request, 'pusukids/expense_confirm_delete.html', {'expense': expense_obj})

# --- Vistas para el CRUD de Fecha ---
@login_required
def fecha_list(request):
    """Vista para listar todas las fechas (semanas)."""
    fechas_list = fecha.objects.order_by('-date')
    return render(request, 'pusukids/fecha_list.html', {'fechas': fechas_list})

@login_required
def fecha_create(request):
    """Vista para crear una nueva fecha (semana)."""
    if request.method == 'POST':
        form = FechaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                # messages.success(request, 'Fecha registrada exitosamente.')
                return redirect('pusukids:fecha_list')
            except Exception as e: # Podría ser IntegrityError si la fecha ya existe y es unique
                # messages.error(request, f'Error al guardar la fecha: {e}')
                pass # Mantener el formulario con el error
        # else:
            # messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = FechaForm()
    return render(request, 'pusukids/fecha_form.html', {'form': form, 'action': 'Registrar'})

@login_required
def fecha_update(request, pk):
    """Vista para actualizar una fecha existente."""
    fecha_obj = get_object_or_404(fecha, pk=pk)
    if request.method == 'POST':
        form = FechaForm(request.POST, instance=fecha_obj)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Fecha actualizada.')
            return redirect('pusukids:fecha_list')
        # else:
            # messages.error(request, 'Por favor corrige los errores.')
    else:
        form = FechaForm(instance=fecha_obj)

    action_title = f"Editar Fecha: {fecha_obj.date.strftime('%Y-%m-%d')}"
    return render(request, 'pusukids/fecha_form.html', {
        'form': form,
        'action': 'Actualizar',
        'action_title': action_title
    })

@login_required
def fecha_delete(request, pk):
    """Vista para eliminar una fecha."""
    fecha_obj = get_object_or_404(fecha, pk=pk)
    if request.method == 'POST':
        try:
            fecha_obj.delete()
            # messages.success(request, 'Fecha eliminada.')
            return redirect('pusukids:fecha_list')
        except ProtectedError:
             # messages.error(request, 'No se puede eliminar esta fecha porque está siendo utilizada en registros de información semanal o gastos.')
             return render(request, 'pusukids/fecha_confirm_delete.html', {
                 'fecha': fecha_obj,
                 'error': 'Esta fecha no se puede eliminar porque está asociada a otros registros (información semanal, gastos, etc.).'
             })
        except Exception as e:
             # messages.error(request, f'Ocurrió un error inesperado: {e}')
             return render(request, 'pusukids/fecha_confirm_delete.html', {
                 'fecha': fecha_obj,
                 'error': f'Error inesperado al eliminar: {e}'
             })

    return render(request, 'pusukids/fecha_confirm_delete.html', {'fecha': fecha_obj})

# --- Vistas para el CRUD de GroupCoordinator ---
@login_required
def groupcoordinator_list(request):
    """Vista para listar todas las asignaciones de grupo-coordinador."""
    assignments = GroupCoordinator.objects.select_related('group', 'coordinator').order_by('group__name', 'coordinator__surname')
    return render(request, 'pusukids/groupcoordinator_list.html', {'assignments': assignments})

@login_required
def groupcoordinator_create(request):
    """Vista para crear una nueva asignación."""
    if request.method == 'POST':
        form = GroupCoordinatorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Asignación creada exitosamente.')
                return redirect('pusukids:groupcoordinator_list')
            except IntegrityError:
                messages.error(request, 'Error: Esta asignación de grupo y coordinador ya existe.')
    else:
        form = GroupCoordinatorForm()
    return render(request, 'pusukids/groupcoordinator_form.html', {'form': form, 'action': 'Asignar'})

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
                return redirect('pusukids:groupcoordinator_list')
            except IntegrityError:
                messages.error(request, 'Error: Esta asignación de grupo y coordinador ya existe.')
    else:
        form = GroupCoordinatorForm(instance=assignment)
    
    action_title = f"Editar Asignación: {assignment}"
    return render(request, 'pusukids/groupcoordinator_form.html', {
        'form': form, 
        'action': 'Actualizar', 
        'action_title': action_title
    })

@login_required
def groupcoordinator_delete(request, pk):
    """Vista para eliminar una asignación."""
    assignment = get_object_or_404(GroupCoordinator.objects.select_related('group', 'coordinator'), pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Asignación eliminada exitosamente.')
        return redirect('pusukids:groupcoordinator_list')
    return render(request, 'pusukids/groupcoordinator_confirm_delete.html', {'assignment': assignment})