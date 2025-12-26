# 生成的迁移文件（如 0002_populate_uuids.py）
from django.db import migrations
import uuid

def generate_uuids(apps, schema_editor):
    User = apps.get_model('users', 'User')
    for user in User.objects.filter(uuid__isnull=True):
        user.uuid = uuid.uuid4()
        user.save(update_fields=['uuid'])

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_user_last_updated_user_uuid'),  # 替换成实际的上一个迁移文件名
    ]

    operations = [
        migrations.RunPython(generate_uuids),
    ]
