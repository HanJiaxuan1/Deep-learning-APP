from django.db import models
import pickle
from werkzeug.security import generate_password_hash, check_password_hash


# Create your models here.
class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True, db_index=True)
    password_hash = models.CharField(max_length=64, default="123")
    password = models.CharField(max_length=32)
    last_login = models.DateTimeField(blank=True, null=True)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


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
