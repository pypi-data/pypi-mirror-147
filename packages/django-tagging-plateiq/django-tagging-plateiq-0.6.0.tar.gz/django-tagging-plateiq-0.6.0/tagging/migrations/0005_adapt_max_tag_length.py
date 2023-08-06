from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagging', '0004_auto_20170802_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(
                unique=True,
                max_length=getattr(settings, 'MAX_TAG_LENGTH', 50),
                verbose_name='name',
                db_index=True),
        ),
    ]
