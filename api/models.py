from django.db import models

# Create your models here.

class RegisterUser(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.name}: {self.phone_number}"


class ContactList(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name="user")
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}: {self.phone_number}"


class SpamNumber(models.Model):
    phone_number = models.CharField(max_length=15)
    spamCount = models.PositiveIntegerField(default=1)