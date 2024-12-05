from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Category model for dropdown (managed via admin)
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model for spending data (expenses)
class SpentData(models.Model):
    date = models.DateField(default=timezone.localdate)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name} - {self.price}"

# Model for credit data (income)
class CreditData(models.Model):
    date = models.DateField(default=timezone.localdate)
    money = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.money} on {self.date}"