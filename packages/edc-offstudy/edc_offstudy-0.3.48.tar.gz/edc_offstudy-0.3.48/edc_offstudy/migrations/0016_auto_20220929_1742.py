# Generated by Django 3.2.13 on 2022-09-29 14:42

from django.db import migrations, models
import edc_identifier.managers
import edc_sites.models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_offstudy", "0015_auto_20220925_0032"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="subjectoffstudy",
            managers=[
                ("on_site", edc_sites.models.CurrentSiteManager()),
                ("objects", edc_identifier.managers.SubjectIdentifierManager()),
            ],
        ),
        migrations.AddField(
            model_name="historicalsubjectoffstudy",
            name="report_datetime",
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name="subjectoffstudy",
            name="report_datetime",
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
