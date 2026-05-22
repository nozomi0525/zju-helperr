from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_task_deadline_reward_text'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('order', 'reviewer')},
        ),
    ]
