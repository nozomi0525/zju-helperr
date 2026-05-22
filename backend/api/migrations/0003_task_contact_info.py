from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_task_status_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='contact_info',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
