from django.db import models
import pickle


# Create your models here.
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()


class Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    CHOICES = [
        ('option1', 'Text Classification'),
        ('option2', 'Translator'),
        ('option3', 'Text Generation'),
    ]
    tag = models.CharField(max_length=50, choices=CHOICES)
    upload_date = models.DateField()
    background = models.CharField(max_length=5000)
    model_name = models.CharField(max_length=50)
    input_des = models.CharField(max_length=500)
    output_des = models.CharField(max_length=500)
    task_des = models.CharField(max_length=500)
    model_data = models.BinaryField(default=b'\x00\x01\x02')
    tokenizer_data = models.BinaryField(default=b'\x00\x01\x02')
