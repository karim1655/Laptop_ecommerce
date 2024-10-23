from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Acquirente'),
        ('seller', 'Fornitore'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)


class Laptop(models.Model):
    name = models.CharField(max_length=100)
    processor_brand = models.CharField(max_length=100)
    processor_model = models.CharField(max_length=100)
    ram = models.IntegerField()
    storage = models.IntegerField()
    display_inches = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='laptops/', blank=True, null=True)

    CATEGORY_CHOICES = (
        ('BL', 'Budget laptop'),
        ('HE', 'High end laptop'),
        ('CO', 'Convertible or 2-in-1'),
        ('GA', 'Gaming'),
        ('EN', 'Enterprise'),
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    # def __str__(self):    #    s = self.name + ", " + str(self.display_inches) + "'' , " + self.processor_brand + ", " + self.processor_model + ", " + str(self.ram) + ", " + str(self.storage) + ", " + str(self.price) + ", " + str(self.image)