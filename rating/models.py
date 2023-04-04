from django.db import models
from django.contrib.auth import get_user_model

from product.models import Product

User = get_user_model()
# Create your models here.


class Rating(models.Model):
    RATING_CHOICES = (
        (1, 'Too Bad'), (2, 'Bad'), (3, 'Okay'), (4, 'Good'), (5, 'Perfect')
    )

    product = models.ForeignKey(Product, related_name='ratings', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'product']