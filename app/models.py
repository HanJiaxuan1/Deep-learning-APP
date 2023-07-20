from django.db import models
import pickle
from werkzeug.security import generate_password_hash, check_password_hash
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=64, unique=True, db_index=True)
    password_hash = models.CharField(max_length=64, default="123")
    password = models.CharField(max_length=32)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Model(models.Model):
    model_id = models.AutoField(primary_key=True)
    CHOICES = [
        ('option1', 'Text Classification'),
        ('option2', 'Translator'),
        ('option3', 'Text Generation'),
        ('option4', 'Summarization'),
        ('option5', 'Question Answering'),
        ('option6', 'Fill Mask')
    ]
    tag = models.CharField(max_length=50, choices=CHOICES)
    upload_date = models.DateField()
    background = models.CharField(max_length=5000)
    model_name = models.CharField(max_length=50)
    input_des = models.CharField(max_length=500)
    output_des = models.CharField(max_length=500)
    task_des = models.CharField(max_length=500)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', default=3)
    views = models.IntegerField(default=0, verbose_name='the number of views')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class UserLikeNote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    note = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name='model')


class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    # 记录comment所属的用户
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    # 记录comment所属的note
    note_id = models.ForeignKey(Model, on_delete=models.CASCADE, verbose_name='note')
    content = models.TextField(verbose_name='note content')
    content_html = models.TextField(verbose_name='note content html version')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='create time')
    # 记录views的数量
    views = models.IntegerField(default=0, verbose_name='the number of views')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', default=2)
    views = models.IntegerField(default=0, verbose_name='the number of views')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


# 防止模型的参数过于复杂，直接分离reply和comment
class Reply(models.Model):
    rid = models.AutoField(primary_key=True)
    # 记录reply所属的用户
    uid = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    # 记录reply所属的comment
    cid = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='comment')
    # 记录这条reply是否为回复他人的reply
    # 这里直接记录target的id，可能会没有这个target_id因此不用外键
    target_id = models.IntegerField(default=-1, verbose_name="the id of the target user")
    content = models.TextField(verbose_name='note content')
    content_html = models.TextField(verbose_name='note content html version')
    create_time = models.DateTimeField(default=timezone.now, db_index=True, verbose_name='create time')
    # 记录views的数量
    views = models.IntegerField(default=0, verbose_name='the number of views')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])