from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    contact = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    country = models.CharField(max_length=500, default='')
    city = models.CharField(max_length=500, default='')

class Adoption(models.Model):
    pet_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="static/", default="")
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.IntegerField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default="")
    color = models.CharField(max_length=100)
    eating_habits = models.CharField(max_length=100)
    alergies = models.CharField(max_length=100)

    def __str__(self):
        return self.pet_name
    
class lostandfound(models.Model):

    image = models.ImageField(upload_to="static", default="")
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    distinctmarks = models.CharField(max_length=200)
    temp_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  default="")
    lorf = models.CharField(max_length=10, default='')
    def __str__(self):
        return self.breed
    
class Contact(models.Model):
    query_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    subject = models.CharField(max_length=70)
    query = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
class Breed(models.Model):
    name = models.CharField(max_length=100)
    height = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    life_expect = models.CharField(max_length=100)
    coat_type = models.CharField(max_length=100)
    coat_colors = models.CharField(max_length=100)
    temperament = models.CharField(max_length=100)
    alergies = models.CharField(max_length=100)

    def __str__(self):
        return self.name
