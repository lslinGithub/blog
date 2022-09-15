import markdown
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# 引入django中的timezone它可以自动帮我们处理时区的问题，只要你在settings.py中设置过时区
from django.utils import timezone
from django.utils.html import strip_tags
from mdeditor.fields import MDTextField


class Category(models.Model):
    name = models.CharField(verbose_name='分类', max_length=100)

    class Meta:
        verbose_name_plural = u'分类'
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(verbose_name='标签', max_length=100)

    class Meta:
        verbose_name_plural = u'标签'
        verbose_name = verbose_name_plural

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(verbose_name='标题', max_length=70)
    # body = models.TextField(verbose_name='正文', )
    body = MDTextField(verbose_name='内容')
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modified_time = models.DateTimeField(verbose_name='修改时间', )
    excerpt = models.CharField(verbose_name='摘要', max_length=200, blank=True)
    category = models.ForeignKey(verbose_name='分类', to='Category', on_delete=models.CASCADE)
    tag = models.ManyToManyField(verbose_name='标签', to='Tag', blank=True)
    author = models.ForeignKey(verbose_name='作者', to=User, on_delete=models.CASCADE)
    view = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name_plural = '文章'
        verbose_name = verbose_name_plural


    # 写一个统计浏览次数的方法
    def increase_views(self):
        self.view += 1
        # 这里只指定更改views字段能提高效率
        self.save(update_fields=['views'])

    # 重写models.Model的save方法,让模型每次更改时都能自己获取当前时间
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # 设置保存模型时自动保存修改时间
        self.modified_time = timezone.now()
        # 设置不手动输入摘要时，自动截取内容前部分字符作为摘要,也可使用过滤器中的truncatechars:55
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
        ])
        # strip_tags 为django html截取字符函数
        self.excerpt = strip_tags(md.convert(self.body))[:55]
        super().save()

    def __str__(self):
        return self.title
