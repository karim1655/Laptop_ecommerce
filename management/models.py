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
    description = models.CharField(max_length=200, blank=True, null=True)
    processor_brand = models.CharField(max_length=100)
    processor_model = models.CharField(max_length=100)
    ram = models.IntegerField()
    storage = models.IntegerField()
    display_inches = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='laptops/', blank=True, null=True)

    CATEGORY_CHOICES = (
        ('', 'Select Category'),
        ('BL', 'Budget laptop'),
        ('HE', 'High end laptop'),
        ('CO', 'Convertible or 2-in-1'),
        ('GA', 'Gaming'),
        ('EN', 'Enterprise'),
    )
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    seller = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    @property
    def avg_rating(self):
        laptop_reviews = self.laptopreview_set.all()
        if laptop_reviews.exist():
            return sum(laptop_review.rating for laptop_review in laptop_reviews) / laptop_reviews.count()
        return 0


class LaptopReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    description = models.TextField(max_length=200, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'laptop'),)

    def __str__(self):
        return f"{self.user}'s review for {self.laptop} by {self.laptop.seller}"


class SellerReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_reviews')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    description = models.TextField(max_length=200, blank=True)
    creation_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}'s review for {self.seller}"