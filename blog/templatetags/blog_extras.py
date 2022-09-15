from django import template
from django.db.models import Count
from ..models import Post, Category, Tag

register = template.Library()


# 包含标签返回页面上不经常变动的数据库数据
@register.inclusion_tag('blog/inclusions/recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num]
    }


@register.inclusion_tag('blog/inclusions/archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('created_time', 'month', order='DESC')
    }


@register.inclusion_tag('blog/inclusions/categories.html', takes_context=True)
def show_categories(context):
    # 这个Category.objects.annotate方法和Category.objects.all有点类似，它会返回数据库中全部
    # Category的记录，但同时它还会做一些额外的事情，在这里我们希望它做的额外事情就是去统计返回的
    # Category记录的集合中每条记录下的文章数。代码中的Count方法为我们做了这个事，它接收一个和
    # Categoty相关联的模型参数名（这里是Post，通过ForeignKey关联的），然后它便会统计
    # Category记录的集合中每条记录下的与之关联的Post记录的行数，也就是文章数，最后把这个值保存到
    # num_posts属性中。
    #
    # 此外，我们还对结果集做了一个过滤，使用filter方法把num_posts的值小于1的分类过滤掉。因为
    # num_posts的值小于1表示该分类下没有文章，没有文章的分类我们不希望它在页面中显示。
    category_list = Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'category_list': category_list,
    }


@register.inclusion_tag('blog/inclusions/tags.html', takes_context=True)
def show_tags(context):
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }
