# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 10:43
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galerie_cms_integration', '0002_remove_localisation_geolocalisation'),
    ]

    operations = [
        migrations.AddField(
            model_name='localisation',
            name='geolocalisation',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=3857),
        ),
    ]
