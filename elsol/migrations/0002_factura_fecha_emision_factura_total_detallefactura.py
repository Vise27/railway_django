# Generated by Django 5.0 on 2024-11-24 22:47

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsol', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='fecha_emision',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='factura',
            name='total',
            field=models.FloatField(null=True),
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id_detalle', models.BigAutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.FloatField(null=True)),
                ('precio_total', models.FloatField(null=True)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='elsol.factura')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsol.producto')),
            ],
        ),
    ]
