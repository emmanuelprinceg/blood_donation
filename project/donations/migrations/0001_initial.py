# Generated by Django 4.2.16 on 2024-10-18 15:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type_needed', models.CharField(max_length=3)),
                ('location', models.CharField(max_length=100)),
                ('request_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('waiting', 'Waiting for Response'), ('accepted', 'Accepted'), ('fulfilled', 'Fulfilled')], default='waiting', max_length=20)),
                ('fulfilled', models.BooleanField(default=False)),
                ('donor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.donorprofile')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.recipientprofile')),
            ],
        ),
        migrations.CreateModel(
            name='DonationAcceptance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('blood_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donations.bloodrequest')),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.donorprofile')),
            ],
        ),
    ]
