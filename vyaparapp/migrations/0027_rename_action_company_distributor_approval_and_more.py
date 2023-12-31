# Generated by Django 4.2.3 on 2023-10-28 05:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vyaparapp', '0026_alter_staff_details_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='Action',
            new_name='Distributor_approval',
        ),
        migrations.AddField(
            model_name='company',
            name='superadmin_approval',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.CreateModel(
            name='Distributors_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distributor_id', models.CharField(blank=True, max_length=100, null=True)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='image/distributor')),
                ('start_date', models.DateField(blank=True, max_length=255, null=True)),
                ('End_date', models.DateField(blank=True, max_length=255, null=True)),
                ('payment_terms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vyaparapp.payment_terms')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='Distributors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vyaparapp.distributors_details'),
        ),
    ]
