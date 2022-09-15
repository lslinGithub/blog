from django import template
from ..forms import CommentsForm

register = template.Library()


@register.inclusion_tag('comments/inclusions/form.html', takes_context=True)
def show_comments_form(context, post, form=None):
    # 从定义可以看到，show_comment_form模板标签使用时会接受一个post（文章
    # Post模型的实例）作为参数，同时也可能传入一个评论表单CommentForm
    # 的实例form，如果没有接受到评论表单参数，模板标签就会新创建一个CommentForm的实例
    # （一个没有绑定任何数据的空表单）传给模板，否则就直接将接受到的评论表单实例直接传给模板，
    # 这主要是为了复用已有的评论表单实例（后面会看到其用法）。
    if form is None:
        form = CommentsForm()
    return {
        'form': form,
        'post': post,
    }


@register.inclusion_tag('comments/inclusions/comment_list.html', takes_context=True)
def show_comments_list(context, post):
    comment_list = post.comments_set.all().order_by('-created_time')
    # 返回的多模型调用count方法计算数量
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }
