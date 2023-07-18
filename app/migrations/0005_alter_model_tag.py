# Generated by Django 4.2.1 on 2023-07-18 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_comment_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='tag',
            field=models.CharField(choices=[('option1', 'Text Classification'), ('option2', 'Translator'), ('option3', 'Text Generation'), ('option4', 'Summarization'), ('option5', 'Question Answering'), ('option6', 'Fill Mask')], max_length=50),
        ),
    ]
