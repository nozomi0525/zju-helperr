from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Task, Order, Review, Message, Report, Blacklist

User = get_user_model()


class Command(BaseCommand):
    help = '清空所有测试帖子、订单、评价及注册用户（上线前清库用）'

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help='确认执行删除（不加此参数仅预览，不会删除）',
        )

    def handle(self, *args, **options):
        counts = {
            '用户': User.objects.count(),
            '帖子': Task.objects.count(),
            '订单': Order.objects.count(),
            '评价': Review.objects.count(),
            '消息': Message.objects.count(),
            '举报': Report.objects.count(),
            '黑名单': Blacklist.objects.count(),
        }

        self.stdout.write('当前数据库中的数据：')
        for name, n in counts.items():
            self.stdout.write(f'  {name}: {n}')

        if not options['yes']:
            self.stdout.write(self.style.WARNING(
                '\n未执行删除。确认后请运行：\n'
                '  python manage.py purge_demo_data --yes\n'
                '或在 Docker 中：\n'
                '  docker-compose exec web python manage.py purge_demo_data --yes'
            ))
            return

        Review.objects.all().delete()
        Message.objects.all().delete()
        Report.objects.all().delete()
        Blacklist.objects.all().delete()
        Order.objects.all().delete()
        Task.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            '\n已清空：所有注册用户、帖子、订单及相关数据。'
            '\n网站已恢复为空白状态，可重新注册正式账号。'
        ))
