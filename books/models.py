from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=20)
    author=models.CharField(max_length=20)
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    stock=models.PositiveIntegerField()
    cover_image=models.URLField(blank=True)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



    def __str__(self):
        return self.title

