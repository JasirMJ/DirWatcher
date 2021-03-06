# Generated by Django 4.0.4 on 2022-05-24 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DirectoryRecords',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Directory Record',
                'verbose_name_plural': 'Directory Records',
                'db_table': 'directory_records',
            },
        ),
    ]
