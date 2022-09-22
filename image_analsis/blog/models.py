from turtle import title
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()

    create_at = models.DateField(auto_now=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title} (id: {self.pk})'



class Comment(models.Model):
    user =  models.CharField(max_length=50)
    content = models.TextField()
    create_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.title} (id: {self.pk})'


