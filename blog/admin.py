from django.contrib import admin
from .models import Post, Category, Tag


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    # 外围展示的字段
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']
    # 表单可编辑的字段
    fields = ['title', 'body', 'excerpt', 'category', 'tag']

    # 重写Model.admin资产save_model，实现谁创建文章谁就是作者
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
