# Generated by Django 2.1.5 on 2019-03-17 05:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stock', '0005_auto_20190316_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=200)),
                ('customer_phone_number', models.CharField(max_length=10)),
                ('customer_email', models.CharField(blank=True, max_length=200, null=True)),
                ('customer_address', models.TextField()),
                ('customer_area', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_list', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralServiceTestResults',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Working', 'Working'), ('Not_Working', 'Not_Working'), ('Replace', 'Replace')], max_length=20)),
                ('check_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.GeneralService')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('helmet', models.BooleanField(default=False)),
                ('vehicle_odo_reading', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('NEW', 'NEW'), ('LIVE', 'LIVE'), ('COMPLETED', 'COMPLETED'), ('DELIVERED', 'DELIVERED')], max_length=20)),
                ('spare_count', models.IntegerField()),
                ('service_in_date', models.DateTimeField()),
                ('delivery_date', models.DateTimeField()),
                ('is_rework', models.BooleanField(default=False)),
                ('rework_count', models.IntegerField(default=0)),
                ('customer_complaint', models.TextField()),
                ('labour_charge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_pickup', models.BooleanField(default=False)),
                ('pickup_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pickup_address', models.TextField()),
                ('delivery_address', models.TextField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Service')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=200)),
                ('is_general', models.BooleanField(default=False)),
                ('has_sub', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SpareCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('per_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('spare', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Spare')),
            ],
        ),
        migrations.CreateModel(
            name='SubService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_service_name', models.CharField(max_length=200)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.ServiceType')),
            ],
        ),
        migrations.CreateModel(
            name='SubServiceCost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Service')),
                ('sub_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.SubService')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_number', models.CharField(max_length=20)),
                ('vehicle_color', models.CharField(max_length=20)),
                ('vehicle_brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.Brand')),
                ('vehicle_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.BrandModel')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='services',
            field=models.ManyToManyField(to='service.ServiceType'),
        ),
        migrations.AddField(
            model_name='service',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Vehicle'),
        ),
        migrations.AddField(
            model_name='generalservicetestresults',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.Service'),
        ),
    ]
