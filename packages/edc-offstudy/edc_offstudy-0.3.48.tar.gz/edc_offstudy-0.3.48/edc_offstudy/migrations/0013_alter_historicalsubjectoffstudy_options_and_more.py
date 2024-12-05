# Generated by Django 4.1 on 2022-08-21 18:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            "edc_offstudy",
            "0012_rename_offstudy_reason_other_historicalsubjectoffstudy_other_offstudy_reason_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="historicalsubjectoffstudy",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical Subject Offstudy",
                "verbose_name_plural": "historical Subject Offstudy",
            },
        ),
        migrations.AlterModelOptions(
            name="subjectoffstudy",
            options={
                "default_permissions": ("add", "change", "delete", "view", "export", "import"),
                "get_latest_by": "modified",
                "ordering": ("-modified", "-created"),
                "verbose_name": "Subject Offstudy",
                "verbose_name_plural": "Subject Offstudy",
            },
        ),
    ]
