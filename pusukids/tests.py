from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from account.models import Tenant
from account.tenant import set_current_tenant
from .models import coordinator, group, fecha, weekinfo


class WeeklyConsolidatedReportTest(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name='Tenant Consolidado', slug='tenant-consolidado')
        set_current_tenant(self.tenant)

        self.user = get_user_model().objects.create_user(username='admin', password='pass123')

        self.group_a = group.objects.create(tenant=self.tenant, name='Grupo A', description='Grupo A')
        self.group_b = group.objects.create(tenant=self.tenant, name='Grupo B', description='Grupo B')

        self.coordinator_a = coordinator.objects.create(
            tenant=self.tenant, user=self.user, name='Ana', surname='Pérez'
        )
        self.coordinator_b = coordinator.objects.create(
            tenant=self.tenant, user=None, name='Luis', surname='García'
        )

        self.fecha_a = fecha.objects.create(tenant=self.tenant, date='2026-10-05', week_no=41)
        self.fecha_b = fecha.objects.create(tenant=self.tenant, date='2026-10-12', week_no=42)

        weekinfo.objects.create(
            tenant=self.tenant,
            fecha=self.fecha_a,
            coordinator=self.coordinator_a,
            group=self.group_a,
            total_kids=12,
            total_servers=3,
            money_collected=80.0,
        )
        weekinfo.objects.create(
            tenant=self.tenant,
            fecha=self.fecha_a,
            coordinator=self.coordinator_b,
            group=self.group_b,
            total_kids=8,
            total_servers=2,
            money_collected=70.0,
        )
        weekinfo.objects.create(
            tenant=self.tenant,
            fecha=self.fecha_b,
            coordinator=self.coordinator_a,
            group=self.group_a,
            total_kids=15,
            total_servers=4,
            money_collected=95.0,
        )

    def test_consolidated_weekly_report_ignores_group_and_coordinator(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('pusukids:attendance_report_weekly_consolidated'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '20')
        self.assertContains(response, '15')
        self.assertNotContains(response, 'Grupo A')
        self.assertNotContains(response, 'Ana')
        self.assertEqual(len(response.context['report_rows']), 2)
        self.assertEqual(response.context['report_rows'][0]['total_kids'], 20)
        self.assertEqual(response.context['report_rows'][1]['total_kids'], 15)
