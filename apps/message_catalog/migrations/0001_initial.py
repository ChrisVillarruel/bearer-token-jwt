# Generated by Django 4.1.1 on 2022-09-22 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OperationCatalog',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'OperationCatalog',
                'verbose_name_plural': 'OperationCatalog',
                'db_table': 'OperationCatalog',
            },
        ),
        migrations.CreateModel(
            name='MessageCatalog',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('code_error', models.IntegerField()),
                ('message', models.CharField(max_length=255)),
                ('method', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='message_catalog.operationcatalog')),
            ],
            options={
                'verbose_name': 'MessageCatalog',
                'verbose_name_plural': 'MessageCatalog',
                'db_table': 'MessageCatalog',
            },
        ),
    ]
