# Generated by Django 4.2.1 on 2023-11-09 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('array_bytes', models.BinaryField(editable=True, null=True)),
                ('is_client', models.BooleanField(default=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('last_time', models.DateTimeField(auto_now_add=True)),
                ('last_enter_time', models.DateTimeField(auto_now_add=True)),
                ('last_leave_time', models.DateTimeField(auto_now_add=True)),
                ('enter_count', models.IntegerField(default=0)),
                ('leave_count', models.IntegerField(default=0)),
                ('stay_time', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, upload_to='clients/')),
                ('last_image', models.ImageField(blank=True, upload_to='clients/')),
            ],
            options={
                'db_table': 'client',
            },
        ),
    ]
