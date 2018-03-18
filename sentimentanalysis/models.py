from django.db import models


class Result(models.Model):
    ASIN = models.CharField(max_length=10, unique=True)
    total_reviews_count = models.IntegerField()
    negative_reviews_count = models.IntegerField()
    positive_reviews_count = models.IntegerField()

    def __str__(self):
        return self.ASIN


class Feedback(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Message = models.CharField(max_length=1000)

    def __str__(self):
        return self.Email
