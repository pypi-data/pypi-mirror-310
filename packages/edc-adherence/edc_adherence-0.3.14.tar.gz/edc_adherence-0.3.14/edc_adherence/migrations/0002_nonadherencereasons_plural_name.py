# Generated by Django 3.2.13 on 2022-09-13 18:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_adherence", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="nonadherencereasons",
            name="plural_name",
            field=models.CharField(max_length=250, null=True, verbose_name="Plural name"),
        ),
    ]
