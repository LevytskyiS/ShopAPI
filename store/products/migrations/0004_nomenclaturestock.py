# Generated by Django 5.0.6 on 2024-07-14 18:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_nomenclature_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='NomenclatureStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('nomenclature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nomenclature_stock', to='products.nomenclature')),
            ],
        ),
    ]
