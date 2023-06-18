# Generated by Django 4.2.2 on 2023-06-18 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklisten', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalaufgabe',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Aufgabe', 'verbose_name_plural': 'historical Aufgaben'},
        ),
        migrations.AlterModelOptions(
            name='historicalcheckliste',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Checkliste', 'verbose_name_plural': 'historical Checklisten'},
        ),
        migrations.AlterModelOptions(
            name='historicalchecklisteaufgabe',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Zuordnung Checkliste-Aufgabe', 'verbose_name_plural': 'historical Zuordnungen Checkliste-Aufgabe'},
        ),
        migrations.AlterModelOptions(
            name='historicalchecklisterecht',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical Zuordnung Checkliste-Recht', 'verbose_name_plural': 'historical Zuordnungen Checkliste-Recht'},
        ),
        migrations.AlterField(
            model_name='historicalaufgabe',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalcheckliste',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalchecklisteaufgabe',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='historicalchecklisterecht',
            name='history_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
