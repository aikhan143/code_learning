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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user} | Лайк курса: {self.course}'
    















































# from django.contrib.auth import get_user_model
# from django.db import models
# from applications.product.models import Music, Album

# User = get_user_model()


# class Like(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
#     music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='likes')
#     like = models.BooleanField(default=False)


# class Rating(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
#     music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='ratings')
#     rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)


# class Comment(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
#     music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='comments')
#     text = models.TextField()
#     created_ad = models.DateTimeField(auto_now_add=True)


# class Favourite(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
#     music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='favourites', null=True, blank=True)