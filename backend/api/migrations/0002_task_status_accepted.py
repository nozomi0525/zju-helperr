from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(
                choices=[
                    ('active', 'active'),
                    ('accepted', 'accepted'),
                    ('completed', 'completed'),
                    ('expired', 'expired'),
                ],
                default='active',
                max_length=20,
            ),
        ),
    ]
