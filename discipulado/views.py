from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from decimal import Decimal
from django.db.models import Count, DecimalField, F, OuterRef, Q, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import (
    BatchMeetingAttendanceForm,
    DiscipleForm,
    DiscipleshipGroupForm,
    DiscipleshipGroupMemberForm,
    DiscipleshipMeetingForm,
    HostFamilyForm,
    MeetingExpenseForm,
    OfferingIncomeForm,
    SupervisorForm,
)
from .models import (
    AttendanceStatus,
    Disciple,
    DiscipleshipGroup,
    DiscipleshipGroupMember,
    DiscipleshipMeeting,
    HostFamily,
    MeetingAttendance,
    MeetingExpense,
    OfferingIncome,
    Supervisor,
)


@login_required
def index(request):
    return render(request, 'discipulado/index.html')


class DiscipleListView(LoginRequiredMixin, ListView):
    model = Disciple
    template_name = 'discipulado/disciple_list.html'
    context_object_name = 'disciples'


class DiscipleCreateView(LoginRequiredMixin, CreateView):
    model = Disciple
    form_class = DiscipleForm
    template_name = 'discipulado/disciple_form.html'
    success_url = reverse_lazy('discipulado:disciple_list')


class DiscipleUpdateView(LoginRequiredMixin, UpdateView):
    model = Disciple
    form_class = DiscipleForm
    template_name = 'discipulado/disciple_form.html'
    success_url = reverse_lazy('discipulado:disciple_list')


class DiscipleDeleteView(LoginRequiredMixin, DeleteView):
    model = Disciple
    template_name = 'discipulado/disciple_confirm_delete.html'
    success_url = reverse_lazy('discipulado:disciple_list')


class HostFamilyListView(LoginRequiredMixin, ListView):
    model = HostFamily
    template_name = 'discipulado/host_family_list.html'
    context_object_name = 'host_families'


class HostFamilyCreateView(LoginRequiredMixin, CreateView):
    model = HostFamily
    form_class = HostFamilyForm
    template_name = 'discipulado/host_family_form.html'
    success_url = reverse_lazy('discipulado:host_family_list')


class HostFamilyUpdateView(LoginRequiredMixin, UpdateView):
    model = HostFamily
    form_class = HostFamilyForm
    template_name = 'discipulado/host_family_form.html'
    success_url = reverse_lazy('discipulado:host_family_list')


class HostFamilyDeleteView(LoginRequiredMixin, DeleteView):
    model = HostFamily
    template_name = 'discipulado/host_family_confirm_delete.html'
    success_url = reverse_lazy('discipulado:host_family_list')


class SupervisorListView(LoginRequiredMixin, ListView):
    model = Supervisor
    template_name = 'discipulado/supervisor_list.html'
    context_object_name = 'supervisors'


class SupervisorCreateView(LoginRequiredMixin, CreateView):
    model = Supervisor
    form_class = SupervisorForm
    template_name = 'discipulado/supervisor_form.html'
    success_url = reverse_lazy('discipulado:supervisor_list')


class SupervisorUpdateView(LoginRequiredMixin, UpdateView):
    model = Supervisor
    form_class = SupervisorForm
    template_name = 'discipulado/supervisor_form.html'
    success_url = reverse_lazy('discipulado:supervisor_list')


class SupervisorDeleteView(LoginRequiredMixin, DeleteView):
    model = Supervisor
    template_name = 'discipulado/supervisor_confirm_delete.html'
    success_url = reverse_lazy('discipulado:supervisor_list')


class DiscipleshipGroupListView(LoginRequiredMixin, ListView):
    model = DiscipleshipGroup
    template_name = 'discipulado/group_list.html'
    context_object_name = 'groups'


class DiscipleshipGroupCreateView(LoginRequiredMixin, CreateView):
    model = DiscipleshipGroup
    form_class = DiscipleshipGroupForm
    template_name = 'discipulado/group_form.html'
    success_url = reverse_lazy('discipulado:group_list')


class DiscipleshipGroupUpdateView(LoginRequiredMixin, UpdateView):
    model = DiscipleshipGroup
    form_class = DiscipleshipGroupForm
    template_name = 'discipulado/group_form.html'
    success_url = reverse_lazy('discipulado:group_list')


class DiscipleshipGroupDeleteView(LoginRequiredMixin, DeleteView):
    model = DiscipleshipGroup
    template_name = 'discipulado/group_confirm_delete.html'
    success_url = reverse_lazy('discipulado:group_list')


class DiscipleshipGroupMemberListView(LoginRequiredMixin, ListView):
    model = DiscipleshipGroupMember
    template_name = 'discipulado/group_member_list.html'
    context_object_name = 'memberships'


class DiscipleshipGroupMemberCreateView(LoginRequiredMixin, CreateView):
    model = DiscipleshipGroupMember
    form_class = DiscipleshipGroupMemberForm
    template_name = 'discipulado/group_member_form.html'
    success_url = reverse_lazy('discipulado:group_member_list')


class DiscipleshipGroupMemberUpdateView(LoginRequiredMixin, UpdateView):
    model = DiscipleshipGroupMember
    form_class = DiscipleshipGroupMemberForm
    template_name = 'discipulado/group_member_form.html'
    success_url = reverse_lazy('discipulado:group_member_list')


class DiscipleshipGroupMemberDeleteView(LoginRequiredMixin, DeleteView):
    model = DiscipleshipGroupMember
    template_name = 'discipulado/group_member_confirm_delete.html'
    success_url = reverse_lazy('discipulado:group_member_list')


class DiscipleshipMeetingListView(LoginRequiredMixin, ListView):
    model = DiscipleshipMeeting
    template_name = 'discipulado/meeting_list.html'
    context_object_name = 'meetings'


class DiscipleshipMeetingCreateView(LoginRequiredMixin, CreateView):
    model = DiscipleshipMeeting
    form_class = DiscipleshipMeetingForm
    template_name = 'discipulado/meeting_form.html'
    success_url = reverse_lazy('discipulado:meeting_list')


class DiscipleshipMeetingUpdateView(LoginRequiredMixin, UpdateView):
    model = DiscipleshipMeeting
    form_class = DiscipleshipMeetingForm
    template_name = 'discipulado/meeting_form.html'
    success_url = reverse_lazy('discipulado:meeting_list')


class DiscipleshipMeetingDeleteView(LoginRequiredMixin, DeleteView):
    model = DiscipleshipMeeting
    template_name = 'discipulado/meeting_confirm_delete.html'
    success_url = reverse_lazy('discipulado:meeting_list')


class MeetingAttendanceListView(LoginRequiredMixin, ListView):
    model = MeetingAttendance
    template_name = 'discipulado/attendance_list.html'
    context_object_name = 'attendances'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('meeting', 'meeting__group', 'disciple')
            .order_by('-meeting__meeting_date', 'disciple__last_name', 'disciple__first_name')
        )


def _meeting_disciples(meeting):
    member_ids = list(
        DiscipleshipGroupMember.objects.filter(group=meeting.group, is_active=True).values_list('disciple_id', flat=True)
    )
    if meeting.group.leader_id:
        member_ids.append(meeting.group.leader_id)
    if meeting.group.coleader_id:
        member_ids.append(meeting.group.coleader_id)
    return Disciple.objects.filter(pk__in=set(member_ids)).order_by('last_name', 'first_name')


@login_required
def batch_attendance_create(request, meeting_id):
    meeting = get_object_or_404(DiscipleshipMeeting, pk=meeting_id)
    disciples = _meeting_disciples(meeting)

    if request.method == 'POST':
        form = BatchMeetingAttendanceForm(disciples, request.POST)
        if form.is_valid():
            with transaction.atomic():
                for disciple in disciples:
                    field_name = f'disciple_{disciple.pk}'
                    is_present = form.cleaned_data.get(field_name, False)
                    status = AttendanceStatus.PRESENT if is_present else AttendanceStatus.ABSENT
                    MeetingAttendance.objects.update_or_create(
                        meeting=meeting,
                        disciple=disciple,
                        defaults={'status': status},
                    )
            return redirect('discipulado:attendance_list')
    else:
        initial_data = {}
        existing = {
            attendance.disciple_id: attendance.status
            for attendance in MeetingAttendance.objects.filter(meeting=meeting)
        }
        for disciple in disciples:
            initial_data[f'disciple_{disciple.pk}'] = existing.get(disciple.pk) == AttendanceStatus.PRESENT
        form = BatchMeetingAttendanceForm(disciples, initial=initial_data)

    return render(
        request,
        'discipulado/batch_attendance_form.html',
        {
            'form': form,
            'meeting': meeting,
        },
    )


class OfferingIncomeListView(LoginRequiredMixin, ListView):
    model = OfferingIncome
    template_name = 'discipulado/offering_list.html'
    context_object_name = 'offerings'


class OfferingIncomeCreateView(LoginRequiredMixin, CreateView):
    model = OfferingIncome
    form_class = OfferingIncomeForm
    template_name = 'discipulado/offering_form.html'
    success_url = reverse_lazy('discipulado:offering_list')


class OfferingIncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = OfferingIncome
    form_class = OfferingIncomeForm
    template_name = 'discipulado/offering_form.html'
    success_url = reverse_lazy('discipulado:offering_list')


class OfferingIncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = OfferingIncome
    template_name = 'discipulado/offering_confirm_delete.html'
    success_url = reverse_lazy('discipulado:offering_list')


class MeetingExpenseListView(LoginRequiredMixin, ListView):
    model = MeetingExpense
    template_name = 'discipulado/expense_list.html'
    context_object_name = 'expenses'


class MeetingExpenseCreateView(LoginRequiredMixin, CreateView):
    model = MeetingExpense
    form_class = MeetingExpenseForm
    template_name = 'discipulado/expense_form.html'
    success_url = reverse_lazy('discipulado:expense_list')


class MeetingExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = MeetingExpense
    form_class = MeetingExpenseForm
    template_name = 'discipulado/expense_form.html'
    success_url = reverse_lazy('discipulado:expense_list')


class MeetingExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = MeetingExpense
    template_name = 'discipulado/expense_confirm_delete.html'
    success_url = reverse_lazy('discipulado:expense_list')


@login_required
def reports(request):
    selected_disciple = request.GET.get('disciple')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    attendance_by_meeting = (
        DiscipleshipMeeting.objects.select_related('group')
        .annotate(
            total_marked=Count('attendances'),
            present_count=Count('attendances', filter=Q(attendances__status=AttendanceStatus.PRESENT)),
            absent_count=Count('attendances', filter=Q(attendances__status=AttendanceStatus.ABSENT)),
            justified_count=Count('attendances', filter=Q(attendances__status=AttendanceStatus.JUSTIFIED)),
        )
        .order_by('-meeting_date')
    )

    disciple_history = MeetingAttendance.objects.select_related('meeting', 'meeting__group', 'disciple').order_by(
        '-meeting__meeting_date'
    )
    if selected_disciple:
        disciple_history = disciple_history.filter(disciple_id=selected_disciple)

    offering_totals = OfferingIncome.objects.values('meeting').filter(meeting=OuterRef('pk')).annotate(total=Sum('amount'))
    expense_totals = MeetingExpense.objects.values('meeting').filter(meeting=OuterRef('pk')).annotate(total=Sum('amount'))

    financial_summary = DiscipleshipMeeting.objects.select_related('group').annotate(
        total_income=Coalesce(
            Subquery(offering_totals.values('total')[:1], output_field=DecimalField(max_digits=12, decimal_places=2)),
            Value(Decimal('0.00')),
        ),
        total_expense=Coalesce(
            Subquery(expense_totals.values('total')[:1], output_field=DecimalField(max_digits=12, decimal_places=2)),
            Value(Decimal('0.00')),
        ),
    ).annotate(net_balance=F('total_income') - F('total_expense')).order_by('-meeting_date')

    offering_query = OfferingIncome.objects.all()
    expense_query = MeetingExpense.objects.all()
    if start_date:
        financial_summary = financial_summary.filter(meeting_date__gte=start_date)
        offering_query = offering_query.filter(meeting__meeting_date__gte=start_date)
        expense_query = expense_query.filter(meeting__meeting_date__gte=start_date)
    if end_date:
        financial_summary = financial_summary.filter(meeting_date__lte=end_date)
        offering_query = offering_query.filter(meeting__meeting_date__lte=end_date)
        expense_query = expense_query.filter(meeting__meeting_date__lte=end_date)

    total_income = offering_query.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    total_expense = expense_query.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    context = {
        'disciples': Disciple.objects.order_by('last_name', 'first_name'),
        'attendance_by_meeting': attendance_by_meeting[:20],
        'disciple_history': disciple_history[:50],
        'financial_summary': financial_summary[:30],
        'total_income': total_income,
        'total_expense': total_expense,
        'net_total': total_income - total_expense,
        'selected_disciple': selected_disciple,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'discipulado/reports.html', context)