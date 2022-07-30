from distutils.command.upload import upload
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

class Post(models.Model):
    # category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    # tags = models.ManyToManyField('Tag', blank=True)
    title = models.CharField('TITLE', max_length=50)
    image = models.ImageField('IMAGE', upload_to='community/', blank=True, null=True)
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True)
    update_dt = models.DateTimeField('UPDATE DT', auto_now=True)
    # like = models.PositiveSmallIntegerField('LIKE', default=0)

    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community')

@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     description = models.CharField('DESCRIPTION', max_length=100, blank=True)


# class Tag(models.Model):
#     name = models.CharField(max_length=50)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField('CONTENT')
    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True)
    update_dt = models.DateTimeField('UPDATE DT', auto_now=True)