# Generated by Django 2.0 on 2017-12-28 18:16

import django.contrib.sites.managers
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("edc_registration", "0008_auto_20170810_1032"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="registeredsubject",
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.RemoveField(model_name="registeredsubject", name="study_site"),
        migrations.AddField(
            model_name="registeredsubject",
            name="site",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="sites.Site",
            ),
        ),
    ]
