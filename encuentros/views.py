from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Sum, Max
from django.contrib import messages
from .models import Meeting, Server, Participant, FamilyParticipantInfo, ChurchDataInfo, MeetingParticipant, FinanceMovements, Summary
from .forms import MeetingForm, ServerForm, ParticipantForm, FamilyParticipantInfoForm, ChurchDataInfoForm, MeetingParticipantForm, FinanceMovementsForm, GenerateSummaryForm

# Create your views here.
@login_required
def index(request):
    """
    Vista para la página principal de la aplicación Encuentros.

    Args:
        request: El objeto HttpRequest.

    Returns:
        HttpResponse: La respuesta HTTP con el contenido de la página.
    """
    # Contar el número de reuniones para mostrar en el index
    num_meetings = Meeting.objects.count()
    context = {
        'num_meetings': num_meetings,
        'page_title': _('Encounters Home'),
        'active_page': 'encuentros_home', # Para la navegación activa
    }
    return render(request, 'encuentros/index.html', context)

# Vistas para Meeting
class MeetingListView(LoginRequiredMixin,ListView):
    model = Meeting
    template_name = 'encuentros/meeting_list.html'
    context_object_name = 'meetings'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meetings'
        context['page_title'] = _('List of Meetings')
        return context

class MeetingDetailView(LoginRequiredMixin,DetailView):
    model = Meeting
    template_name = 'encuentros/meeting_detail.html'
    context_object_name = 'meeting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meetings'
        context['page_title'] = _('Meeting Details: %(code)s') % {'code': self.object.code}
        return context

class MeetingCreateView(LoginRequiredMixin,CreateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'encuentros/meeting_form.html'
    success_url = reverse_lazy('encuentros:meeting-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meetings'
        context['page_title'] = _('Register New Meeting')
        context['form_title'] = _('New Meeting Form')
        context['submit_button_text'] = _('Save Meeting')
        return context

class MeetingUpdateView(LoginRequiredMixin,UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'encuentros/meeting_form.html'
    success_url = reverse_lazy('encuentros:meeting-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meetings'
        context['page_title'] = _('Update Meeting: %(code)s') % {'code': self.object.code}
        context['form_title'] = _('Update Meeting Form')
        context['submit_button_text'] = _('Update Meeting')
        return context

class MeetingDeleteView(LoginRequiredMixin,DeleteView):
    model = Meeting
    template_name = 'encuentros/meeting_confirm_delete.html'
    success_url = reverse_lazy('encuentros:meeting-list')
    context_object_name = 'meeting'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meetings'
        context['page_title'] = _('Delete Meeting: %(code)s') % {'code': self.object.code}
        return context

# Vistas para Server
class ServerListView(LoginRequiredMixin,ListView):
    model = Server
    template_name = 'encuentros/server_list.html'
    context_object_name = 'servers'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'servers'
        context['page_title'] = _('List of Servers')
        return context

class ServerDetailView(LoginRequiredMixin,DetailView):
    model = Server
    template_name = 'encuentros/server_detail.html'
    context_object_name = 'server'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'servers'
        context['page_title'] = _('Server Details: %(name)s') % {'name': self.object}
        return context

class ServerCreateView(LoginRequiredMixin,CreateView):
    model = Server
    form_class = ServerForm
    template_name = 'encuentros/server_form.html'
    success_url = reverse_lazy('encuentros:server-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'servers'
        context['page_title'] = _('Register New Server')
        context['form_title'] = _('New Server Form')
        context['submit_button_text'] = _('Save Server')
        return context

class ServerUpdateView(LoginRequiredMixin,UpdateView):
    model = Server
    form_class = ServerForm
    template_name = 'encuentros/server_form.html'
    success_url = reverse_lazy('encuentros:server-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'servers'
        context['page_title'] = _('Update Server: %(name)s') % {'name': self.object}
        context['form_title'] = _('Update Server Form')
        context['submit_button_text'] = _('Update Server')
        return context

class ServerDeleteView(LoginRequiredMixin,DeleteView):
    model = Server
    template_name = 'encuentros/server_confirm_delete.html'
    success_url = reverse_lazy('encuentros:server-list')
    context_object_name = 'server'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'servers'
        context['page_title'] = _('Delete Server: %(name)s') % {'name': self.object}
        return context

# Vistas para Participant
class ParticipantListView(LoginRequiredMixin,ListView):
    model = Participant
    template_name = 'encuentros/participant_list.html'
    context_object_name = 'participants'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'participants'
        context['page_title'] = _('List of Participants')
        return context

class ParticipantDetailView(LoginRequiredMixin,DetailView):
    model = Participant
    template_name = 'encuentros/participant_detail.html'
    context_object_name = 'participant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'participants'
        context['page_title'] = _('Participant Details: %(name)s') % {'name': self.object}
        # Consider adding related info like family or church data if needed
        # context['family_members'] = self.object.family_members.all()
        # context['church_info'] = self.object.church_data.first() # Assuming one-to-one or first if one-to-many
        return context

class ParticipantCreateView(LoginRequiredMixin,CreateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'encuentros/participant_form.html' # Reusing a generic form template
    success_url = reverse_lazy('encuentros:participant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'participants'
        context['page_title'] = _('Register New Participant')
        context['form_title'] = _('New Participant Form')
        context['submit_button_text'] = _('Save Participant')
        return context

class ParticipantUpdateView(LoginRequiredMixin,UpdateView):
    model = Participant
    form_class = ParticipantForm
    template_name = 'encuentros/participant_form.html' # Reusing
    success_url = reverse_lazy('encuentros:participant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'participants'
        context['page_title'] = _('Update Participant: %(name)s') % {'name': self.object}
        context['form_title'] = _('Update Participant Form')
        context['submit_button_text'] = _('Update Participant')
        return context

class ParticipantDeleteView(LoginRequiredMixin,DeleteView):
    model = Participant
    template_name = 'encuentros/participant_confirm_delete.html'
    success_url = reverse_lazy('encuentros:participant-list')
    context_object_name = 'participant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'participants'
        context['page_title'] = _('Delete Participant: %(name)s') % {'name': self.object}
        return context
    
# Vistas para FamilyParticipantInfo
class FamilyParticipantInfoListView(LoginRequiredMixin,ListView):
    model = FamilyParticipantInfo
    template_name = 'encuentros/familyparticipantinfo_list.html'
    context_object_name = 'family_infos'
    paginate_by = 10

    def get_queryset(self):
        # Optimizar consulta para incluir el participante relacionado
        return FamilyParticipantInfo.objects.select_related('participant').order_by('participant__surname', 'participant__name', 'surname', 'name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'family_info' # O anidarlo bajo participantes
        context['page_title'] = _('List of Family Member Information')
        return context

class FamilyParticipantInfoDetailView(LoginRequiredMixin,DetailView):
    model = FamilyParticipantInfo
    template_name = 'encuentros/familyparticipantinfo_detail.html'
    context_object_name = 'family_info'

    def get_queryset(self):
        return FamilyParticipantInfo.objects.select_related('participant')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'family_info'
        context['page_title'] = _('Family Member Details: %(name)s for %(participant)s') % {
            'name': f"{self.object.name} {self.object.surname}",
            'participant': self.object.participant
        }
        return context

class FamilyParticipantInfoCreateView(LoginRequiredMixin,CreateView):
    model = FamilyParticipantInfo
    form_class = FamilyParticipantInfoForm
    template_name = 'encuentros/familyparticipantinfo_form.html'
    success_url = reverse_lazy('encuentros:familyparticipantinfo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'family_info'
        context['page_title'] = _('Add New Family Member Information')
        context['form_title'] = _('New Family Member Information Form')
        context['submit_button_text'] = _('Save Family Member Info')
        return context

class FamilyParticipantInfoUpdateView(LoginRequiredMixin,UpdateView):
    model = FamilyParticipantInfo
    form_class = FamilyParticipantInfoForm
    template_name = 'encuentros/familyparticipantinfo_form.html'
    success_url = reverse_lazy('encuentros:familyparticipantinfo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'family_info'
        context['page_title'] = _('Update Family Member Info: %(name)s') % {'name': self.object}
        context['form_title'] = _('Update Family Member Information Form')
        context['submit_button_text'] = _('Update Family Member Info')
        return context

class FamilyParticipantInfoDeleteView(LoginRequiredMixin,DeleteView):
    model = FamilyParticipantInfo
    template_name = 'encuentros/familyparticipantinfo_confirm_delete.html'
    success_url = reverse_lazy('encuentros:familyparticipantinfo-list')
    context_object_name = 'family_info'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'family_info'
        context['page_title'] = _('Delete Family Member Info: %(name)s') % {'name': self.object}
        return context

# Vistas para ChurchDataInfo
class ChurchDataInfoListView(LoginRequiredMixin,ListView):
    model = ChurchDataInfo
    template_name = 'encuentros/churchdatainfo_list.html'
    context_object_name = 'church_data_entries'
    paginate_by = 10

    def get_queryset(self):
        return ChurchDataInfo.objects.select_related('participant', 'server').order_by('participant__surname', 'participant__name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'church_data' # O anidarlo bajo participantes
        context['page_title'] = _('List of Church Data Information')
        return context

class ChurchDataInfoDetailView(LoginRequiredMixin,DetailView):
    model = ChurchDataInfo
    template_name = 'encuentros/churchdatainfo_detail.html'
    context_object_name = 'church_data'

    def get_queryset(self):
        return ChurchDataInfo.objects.select_related('participant', 'server')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'church_data'
        context['page_title'] = _('Church Data Details for: %(participant)s') % {'participant': self.object.participant}
        return context

class ChurchDataInfoCreateView(LoginRequiredMixin,CreateView):
    model = ChurchDataInfo
    form_class = ChurchDataInfoForm
    template_name = 'encuentros/churchdatainfo_form.html'
    success_url = reverse_lazy('encuentros:churchdatainfo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'church_data'
        context['page_title'] = _('Add New Church Data Information')
        context['form_title'] = _('New Church Data Information Form')
        context['submit_button_text'] = _('Save Church Data')
        return context

class ChurchDataInfoUpdateView(LoginRequiredMixin,UpdateView):
    model = ChurchDataInfo
    form_class = ChurchDataInfoForm
    template_name = 'encuentros/churchdatainfo_form.html'
    success_url = reverse_lazy('encuentros:churchdatainfo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'church_data'
        context['page_title'] = _('Update Church Data for: %(participant)s') % {'participant': self.object.participant}
        context['form_title'] = _('Update Church Data Information Form')
        context['submit_button_text'] = _('Update Church Data')
        return context

class ChurchDataInfoDeleteView(LoginRequiredMixin,DeleteView):
    model = ChurchDataInfo
    template_name = 'encuentros/churchdatainfo_confirm_delete.html'
    success_url = reverse_lazy('encuentros:churchdatainfo-list')
    context_object_name = 'church_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'church_data'
        context['page_title'] = _('Delete Church Data for: %(participant)s') % {'participant': self.object.participant}
        return context

# Vistas para MeetingParticipant
class MeetingParticipantListView(LoginRequiredMixin,ListView):
    model = MeetingParticipant
    template_name = 'encuentros/meetingparticipant_list.html'
    context_object_name = 'meeting_participants'
    paginate_by = 15

    def get_queryset(self):
        return MeetingParticipant.objects.select_related('meeting', 'participant').order_by('-event_date', 'meeting__code', 'participant__surname')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meeting_attendance'
        context['page_title'] = _('List of Meeting Attendances')
        return context

class MeetingParticipantDetailView(LoginRequiredMixin,DetailView):
    model = MeetingParticipant
    template_name = 'encuentros/meetingparticipant_detail.html'
    context_object_name = 'meeting_participant'

    def get_queryset(self):
        return MeetingParticipant.objects.select_related('meeting', 'participant')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meeting_attendance'
        context['page_title'] = _('Attendance Details: %(participant)s at %(meeting)s') % {
            'participant': self.object.participant,
            'meeting': self.object.meeting.code
        }
        return context

class MeetingParticipantCreateView(LoginRequiredMixin,CreateView):
    model = MeetingParticipant
    form_class = MeetingParticipantForm
    template_name = 'encuentros/meetingparticipant_form.html'
    success_url = reverse_lazy('encuentros:meetingparticipant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meeting_attendance'
        context['page_title'] = _('Record New Meeting Attendance')
        context['form_title'] = _('New Meeting Attendance Form')
        context['submit_button_text'] = _('Save Attendance Record')
        return context

class MeetingParticipantUpdateView(LoginRequiredMixin,UpdateView):
    model = MeetingParticipant
    form_class = MeetingParticipantForm
    template_name = 'encuentros/meetingparticipant_form.html'
    success_url = reverse_lazy('encuentros:meetingparticipant-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meeting_attendance'
        context['page_title'] = _('Update Attendance: %(participant)s at %(meeting)s') % {'participant': self.object.participant, 'meeting': self.object.meeting.code}
        context['form_title'] = _('Update Meeting Attendance Form')
        context['submit_button_text'] = _('Update Attendance Record')
        return context

class MeetingParticipantDeleteView(LoginRequiredMixin,DeleteView):
    model = MeetingParticipant
    template_name = 'encuentros/meetingparticipant_confirm_delete.html'
    success_url = reverse_lazy('encuentros:meetingparticipant-list')
    context_object_name = 'meeting_participant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'meeting_attendance'
        context['page_title'] = _('Delete Attendance Record')
        return context
    
# Vistas para FinanceMovements
class FinanceMovementsListView(LoginRequiredMixin,ListView):
    model = FinanceMovements
    template_name = 'encuentros/financemovements_list.html'
    context_object_name = 'finance_movements'
    paginate_by = 15

    def get_queryset(self):
        return FinanceMovements.objects.select_related('meeting_related').order_by('-trans_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'finance'
        context['page_title'] = _('List of Financial Movements')
        return context

class FinanceMovementsDetailView(LoginRequiredMixin,DetailView):
    model = FinanceMovements
    template_name = 'encuentros/financemovements_detail.html'
    context_object_name = 'movement'

    def get_queryset(self):
        return FinanceMovements.objects.select_related('meeting_related')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'finance'
        context['page_title'] = _('Financial Movement Details: %(type)s - %(amount)s') % {
            'type': self.object.get_transaction_type_display(),
            'amount': self.object.amount
        }
        return context

class FinanceMovementsCreateView(LoginRequiredMixin,CreateView):
    model = FinanceMovements
    form_class = FinanceMovementsForm
    template_name = 'encuentros/financemovements_form.html'
    success_url = reverse_lazy('encuentros:financemovements-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'finance'
        context['page_title'] = _('Record New Financial Movement')
        context['form_title'] = _('New Financial Movement Form')
        context['submit_button_text'] = _('Save Movement')
        return context

class FinanceMovementsUpdateView(LoginRequiredMixin,UpdateView):
    model = FinanceMovements
    form_class = FinanceMovementsForm
    template_name = 'encuentros/financemovements_form.html'
    success_url = reverse_lazy('encuentros:financemovements-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'finance'
        context['page_title'] = _('Update Financial Movement')
        context['form_title'] = _('Update Financial Movement Form')
        context['submit_button_text'] = _('Update Movement')
        return context

class FinanceMovementsDeleteView(LoginRequiredMixin,DeleteView):
    model = FinanceMovements
    template_name = 'encuentros/financemovements_confirm_delete.html'
    success_url = reverse_lazy('encuentros:financemovements-list')
    context_object_name = 'movement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'finance'
        context['page_title'] = _('Delete Financial Movement')
        return context    

# Vistas para Summary
class SummaryListView(LoginRequiredMixin,ListView):
    model = Summary
    template_name = 'encuentros/summary_list.html'
    context_object_name = 'summaries'
    paginate_by = 10

    def get_queryset(self):
        return Summary.objects.select_related('meeting').order_by('-period_end', 'meeting__code')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'summaries'
        context['page_title'] = _('List of Financial Summaries')
        return context

class SummaryDetailView(LoginRequiredMixin,DetailView):
    model = Summary
    template_name = 'encuentros/summary_detail.html'
    context_object_name = 'summary'

    def get_queryset(self):
        return Summary.objects.select_related('meeting')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'summaries'
        context['page_title'] = _('Financial Summary for: %(meeting)s') % {'meeting': self.object.meeting}
        return context

class GenerateSummaryView(LoginRequiredMixin,View):
    form_class = GenerateSummaryForm
    template_name = 'encuentros/generate_summary_form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        # Si se pasa un meeting_id por GET, se puede preseleccionar
        meeting_id = request.GET.get('meeting_id')
        if meeting_id:
            try:
                meeting = Meeting.objects.get(pk=meeting_id)
                form = self.form_class(initial={'meeting': meeting})
            except Meeting.DoesNotExist:
                pass # El formulario se mostrará vacío
        
        return render(request, self.template_name, {
            'form': form,
            'page_title': _('Generate Financial Summary'),
            'active_page': 'summaries',
            'form_title': _('Select Meeting to Summarize'),
            'submit_button_text': _('Generate/Update Summary')
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            meeting = form.cleaned_data['meeting']
            
            movements = FinanceMovements.objects.filter(meeting_related=meeting)
            
            if not movements.exists():
                messages.warning(request, _("No financial movements found for meeting '%(meeting)s'. Summary not generated.") % {'meeting': meeting.code})
                return redirect('encuentros:summary-list')

            income_total = movements.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
            expense_total = movements.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
            balance = income_total - expense_total
            last_movement_date = movements.aggregate(latest_date=Max('trans_date'))['latest_date']

            summary, created = Summary.objects.update_or_create(
                meeting=meeting,
                defaults={
                    'period_end': last_movement_date,
                    'income': income_total,
                    'expense': expense_total,
                    'balance': balance
                }
            )

            if created:
                messages.success(request, _("Financial summary for meeting '%(meeting)s' generated successfully.") % {'meeting': meeting.code})
            else:
                messages.success(request, _("Financial summary for meeting '%(meeting)s' updated successfully.") % {'meeting': meeting.code})
            
            return redirect('encuentros:summary-detail', pk=summary.pk)
        
        return render(request, self.template_name, {'form': form, 'page_title': _('Generate Financial Summary'), 'active_page': 'summaries'})

class SummaryDeleteView(LoginRequiredMixin,DeleteView):
    model = Summary
    template_name = 'encuentros/summary_confirm_delete.html'
    success_url = reverse_lazy('encuentros:summary-list')
    context_object_name = 'summary'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'summaries'
        context['page_title'] = _('Delete Financial Summary')
        return context