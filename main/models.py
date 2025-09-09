from django.db import models

# Create your models here.
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('goalkeeper', 'Goalkeeper'),
        ('center-back', 'Center-Back'),
        ('left-back', 'Left-Back'),
        ('right-back', 'Right-Back'),
        ('center-midfielder', 'Center-Midfielder'),
        ('attacking-midfielder', 'Attacking-Midfielder'),
        ('defensive-midfielder', 'Defensive-Midfielder'),
        ('left-winger', 'Left-Winger'),
        ('right-winger', 'Right-Winger'),
        ('striker', 'Striker'),
    ]
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    club = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    height = models.FloatField()

    def __str__(self):
        return self.name
