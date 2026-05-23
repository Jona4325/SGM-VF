from django.conf import settings
from django.db import migrations


def seed_default_tenant(apps, schema_editor):
    Tenant = apps.get_model('account', 'Tenant')
    TenantMembership = apps.get_model('account', 'TenantMembership')
    User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

    tenant, _ = Tenant.objects.get_or_create(
        slug='pusuqui',
        defaults={'name': 'Pusuqui', 'is_active': True},
    )

    for user in User.objects.all():
        TenantMembership.objects.get_or_create(
            user_id=user.pk,
            tenant_id=tenant.pk,
            defaults={'is_default': True, 'is_active': True},
        )

    tenant_models = {
        'academia': ['Teacher', 'Student', 'Subject', 'Course', 'Enrollment', 'AttendanceLog', 'Grade'],
        'alabanza': ['Coordinator', 'Group', 'Server', 'Assistance'],
        'anfitriones': ['Coordinator', 'Group', 'Server', 'Ministry', 'Assistance', 'Attendance'],
        'cunakids': ['coordinator', 'group', 'server', 'child', 'assistance', 'GroupCoordinator'],
        'encuentros': ['Meeting', 'Server', 'Participant', 'FamilyParticipantInfo', 'ChurchDataInfo', 'MeetingParticipant', 'FinanceMovements', 'Summary'],
        'jap': ['coordinator', 'group', 'server', 'child', 'assistance', 'GroupCoordinator'],
        'jpro': ['coordinator', 'group', 'server', 'child', 'assistance', 'GroupCoordinator'],
        'pequediks': ['coordinator', 'group', 'server', 'child', 'assistance', 'GroupCoordinator'],
        'pusukids': ['coordinator', 'group', 'server', 'groupage', 'child', 'fecha', 'assistance', 'weekinfo', 'expense', 'GroupCoordinator'],
    }

    for app_label, model_names in tenant_models.items():
        for model_name in model_names:
            Model = apps.get_model(app_label, model_name)
            Model.objects.filter(tenant__isnull=True).update(tenant_id=tenant.pk)


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('academia', '0008_alter_attendancelog_unique_together_and_more'),
        ('alabanza', '0003_alter_coordinator_unique_together_and_more'),
        ('anfitriones', '0003_alter_assistance_unique_together_and_more'),
        ('cunakids', '0007_alter_groupcoordinator_options_and_more'),
        ('encuentros', '0002_alter_meetingparticipant_unique_together_and_more'),
        ('jap', '0003_alter_groupcoordinator_options_and_more'),
        ('jpro', '0002_alter_groupcoordinator_options_and_more'),
        ('pequediks', '0003_alter_groupcoordinator_options_and_more'),
        ('pusukids', '0013_alter_groupcoordinator_options_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_default_tenant, migrations.RunPython.noop),
    ]
