from django.db import migrations


def migrate_inactive_courses_to_closed(apps, schema_editor):
    Course = apps.get_model('academia', 'Course')
    Course.objects.filter(is_active=False).update(is_closed=True)


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0009_course_is_closed'),
    ]

    operations = [
        migrations.RunPython(migrate_inactive_courses_to_closed, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='course',
            name='is_active',
        ),
    ]