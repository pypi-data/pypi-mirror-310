# Generated by Django 3.0.4 on 2020-05-12 21:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("edc_registration", "0020_auto_20191024_1000"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="registeredsubject",
            options={
                "default_permissions": (
                    "add",
                    "change",
                    "delete",
                    "view",
                    "export",
                    "import",
                ),
                "get_latest_by": "modified",
                "ordering": ["subject_identifier"],
                "permissions": (
                    ("display_firstname", "Can display first name"),
                    ("display_lastname", "Can display last name"),
                    ("display_dob", "Can display DOB"),
                    ("display_identity", "Can display identity number"),
                    ("display_initials", "Can display initials"),
                ),
                "verbose_name": "Registered Subject",
            },
        ),
    ]
