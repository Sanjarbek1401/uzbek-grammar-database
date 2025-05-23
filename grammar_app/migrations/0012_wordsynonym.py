# Generated by Django 5.2 on 2025-04-16 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grammar_app', '0011_alter_uslubdata_badiiy_alter_uslubdata_ilmiy_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WordSynonym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grammatical_word', models.CharField(max_length=255, verbose_name="Grammatik so'z")),
                ('translations', models.TextField(blank=True, verbose_name='Tarjimalar')),
                ('identity', models.CharField(blank=True, max_length=255, verbose_name='Identifikator')),
                ('synonyms', models.TextField(blank=True, verbose_name='Sinonimlar')),
            ],
            options={
                'verbose_name': "So'z sinonimi",
                'verbose_name_plural': "So'z sinonimlari",
                'ordering': ['grammatical_word'],
            },
        ),
    ]
