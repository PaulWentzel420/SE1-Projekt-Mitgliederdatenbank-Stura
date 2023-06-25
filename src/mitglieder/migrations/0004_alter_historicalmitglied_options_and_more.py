<<<<<<< HEAD
# Generated by Django 4.2.2 on 2023-06-17 08:58
=======
# Generated by Django 4.2.2 on 2023-06-18 13:47
>>>>>>> 56fe793af97bc06dcad644cbaea3e286fec930aa

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mitglieder', '0003_auto_20210620_1913'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalmitglied',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Mitglied', 'verbose_name_plural': 'historical Mitglieder'},
        ),
        migrations.AlterModelOptions(
            name='historicalmitgliedamt',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Zuordnung Mitglied-Amt', 'verbose_name_plural': 'historical Zuordnungen Mitglied-Amt'},
        ),
        migrations.AlterModelOptions(
            name='historicalmitgliedmail',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Zuordnung Mitglied-Mail', 'verbose_name_plural': 'historical Zuordnungen Mitglied-Mail'},
        ),
        migrations.AddField(
            model_name='historicalmitglied',
            name='auto_checkliste',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mitglied',
            name='auto_checkliste',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='historicalmitglied',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalmitgliedamt',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalmitgliedmail',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]