from django.db import models
from django.utils import timezone


# Create your models here.
import blog.models


class Comments(models.Model):
    name = models.CharField(verbose_name='名字', max_length=50)
    email = models.EmailField(verbose_name='邮箱')
    url = models.URLField(verbose_name='网址', blank=True)
    text = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    post = models.ForeignKey(verbose_name='文章', to='blog.Post', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '评论'
        verbose_name = verbose_name_plural

    def __str__(self):
        return '{}:{}'.format(self.name, self.text[:20])