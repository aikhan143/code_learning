from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Course 
from django.core.validators import *

User = get_user_model()



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES, null=True)

    def __str__(self):
        return f'{self.user} | Rating: {self.rating} for {self.course}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user} | Лайк курса: {self.course}'
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, through='CartCourse')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(course.price for course in self.courses.all())

    def clear_cart(self):
        self.courses.clear()

    def __str__(self):
        return f"Cart #{self.id} - User: {self.user.username}"

class CartCourse(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.course.price * self.quantity

    def __str__(self):
        return f"{self.quantity} - {self.course.title}"













































