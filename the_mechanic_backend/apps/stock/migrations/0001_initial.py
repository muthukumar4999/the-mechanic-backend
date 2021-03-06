# Generated by Django 2.1.5 on 2019-03-30 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BrandModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=200)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Brand')),
            ],
            options={
                'ordering': ['model_name'],
            },
        ),
        migrations.CreateModel(
            name='Spare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spare_name', models.CharField(max_length=200)),
                ('spare_local_name', models.CharField(max_length=200, null=True)),
                ('spare_id', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('buying_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('wholesaler_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('mechanic_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('customer_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('mrp_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('suppliers', models.CharField(max_length=200)),
                ('quality_class', models.CharField(max_length=100)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Brand')),
                ('brand_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.BrandModel')),
            ],
            options={
                'ordering': ['spare_name'],
            },
        ),
    ]
