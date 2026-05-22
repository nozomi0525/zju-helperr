from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_task_contact_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='reward',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
