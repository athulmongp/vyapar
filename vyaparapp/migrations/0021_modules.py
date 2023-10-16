# Generated by Django 4.2.3 on 2023-10-15 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vyaparapp', '0020_delete_company_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='modules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_invoice', models.IntegerField(default=0, null=True)),
                ('Estimate', models.IntegerField(default=0, null=True)),
                ('Payment_in', models.IntegerField(default=0, null=True)),
                ('sales_order', models.IntegerField(default=0, null=True)),
                ('Delivery_challan', models.IntegerField(default=0, null=True)),
                ('sales_return', models.IntegerField(default=0, null=True)),
                ('Purchase_bills', models.IntegerField(default=0, null=True)),
                ('Payment_out', models.IntegerField(default=0, null=True)),
                ('Purchase_order', models.IntegerField(default=0, null=True)),
                ('Purchase_return', models.IntegerField(default=0, null=True)),
                ('Bank_account', models.IntegerField(default=0, null=True)),
                ('Cash_in_hand', models.IntegerField(default=0, null=True)),
                ('cheques', models.IntegerField(default=0, null=True)),
                ('Loan_account', models.IntegerField(default=0, null=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vyaparapp.company')),
            ],
        ),
    ]
