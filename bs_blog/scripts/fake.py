import os
import sys
import random

import django
import pathlib
from datetime import timedelta
import faker as faker
from django.utils import timezone
from bs_blog.settings import BASE_DIR


# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bs_blog.settings")
    django.setup()

    from blog.models import Category, Post, Tag
    from comments.models import Comments
    from django.contrib.auth.models import User

    print("脚本创建数据前，清理掉原来数据库数据")
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Comments.objects.all().delete()
    User.objects.all().delete()
    print("清理完成！")

    print("创建用户：")
    user = User.objects.create_superuser('admin', 'lslvirtualemail@gmail.com', 'admin')

    print("创建分类和标签：")
    category_list = ['Python学习笔记', '开源项目', '程序员生活感悟', 'Mysql', '算法']
    tag_list = ['django', 'Python', 'Pipenv', 'Docker', 'Nginx', 'Elasticsearch', 'Gunicorn', 'Supervisor']
    half_year_ago = timezone.now() - timedelta(days=182)
    three_month_ago = timezone.now() - timedelta(days=90)

    for cate in category_list:
        Category.objects.create(name=cate)

    for tag in tag_list:
        Tag.objects.create(name=tag)

    print("创建一篇简单文章：")
    Post.objects.create(
        title='Markdown基本语法',
        body=pathlib.Path(BASE_DIR).joinpath('scripts', 'md.sample').read_text(encoding='utf-8'),
        category=Category.objects.create(name='Markdown测试'),
        author=user,
    )

    # fake = faker.Faker()，要使用 Faker 自动生成数据，首先实例化一个 Faker 对象，然后我们可以在脚本中使用这个实例的一些方法生成需要的数据。Faker 默认生成英文数据，但也支持国际化。至于如何生成中文数据在下一段脚本中会看到。
    # order_by('?') 将返回随机排序的结果，脚本中这块代码的作用是达到随机选择标签(Tag) 和分类(Category) 的效果。

    # 这个方法将返回 2 个指定日期间的随机日期。三个参数分别是起始日期，终止日期和时区。我们在这里设置起始日期为 1 年前（-1y），终止日期为当下（now），时区为 get_current_timezone 返回的时区，这个函数是 django.utils.timezone 模块的辅助函数，它会根据 django 设置文件中 TIME_ZONE 的值返回对应的时区对象。
    # '\n\n'.join(fake.paragraphs(10))fake.paragraphs(10) 用于生成 10 个段落文本，以列表形式返回，列表的每个元素即为一个段落。要注意使用 2 个换行符连起来是为了符合 Markdown 语法，Markdown 中只有 2 个换行符分隔的文本才会被解析为段落。
    print("创建30篇随机文章：")
    fake = faker.Faker('zh_CN')
    for _ in range(30):  # Chinese
        tags = Tag.objects.order_by('?')
        tag1 = tags.first()
        tag2 = tags.last()
        cate = Category.objects.order_by('?').first()
        created_time = fake.date_time_between(start_date='-1y', end_date="now",
                                              tzinfo=timezone.get_current_timezone())
        post = Post.objects.create(
            title=fake.sentence().rstrip('.'),
            body='\n\n'.join(fake.paragraphs(10)),
            created_time=created_time,
            category=cate,
            author=user,
        )
        post.tag.add(tag1, tag2)
        post.save()

    print('创建随机评论：')
    # 要注意的是评论的发布时间必须位于被评论文章的发布时间和当前时间之间，这就是 delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd' 这句代码的作用。
    for post in Post.objects.all()[:20]:
        post_created_time = post.created_time
        delta_in_days = '-' + str((timezone.now() - post_created_time).days) + 'd'
        for _ in range(random.randrange(3, 15)):
            Comments.objects.create(
                name=fake.name(),
                email=fake.email(),
                url=fake.uri(),
                text=fake.paragraph(),
                created_time=fake.date_time_between(
                    start_date=delta_in_days,
                    end_date="now",
                    tzinfo=timezone.get_current_timezone()),
                post=post,
            )

    print('done!')
