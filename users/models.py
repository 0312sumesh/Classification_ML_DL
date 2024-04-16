from django.db import models


# Create your models here.
class UserRegistrationModel(models.Model):
    name = models.CharField(max_length=100)
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistrations'


class UserXRayModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    filename = models.FileField()
    croped = models.FileField()
    upper_image = models.FileField()
    lower_image = models.FileField()
    cdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'UserDentalResults'