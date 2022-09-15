from blog.models import User, Post
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(
        attrs={'placeholder': "用户名", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'placeholder': "密码"}))
    captcha = CaptchaField(label='验证码', required=True, error_messages={'required': '验证码不能为空'})


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=16, widget=forms.TextInput())
    password1 = forms.CharField(label='密码', max_length=256, widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码', max_length=256, widget=forms.PasswordInput())
    email = forms.CharField(label='邮箱地址', max_length=30, widget=forms.EmailInput())
    captcha = CaptchaField(label='验证码')


class Find_pwd(forms.Form):
    username = forms.CharField(label='用户名', max_length=16, widget=forms.TextInput())
    email = forms.CharField(label='邮箱', max_length=30, widget=forms.EmailInput())


class Commit_form(forms.Form):
    code = forms.CharField(label='邮箱验证码', widget=forms.TextInput())
    password = forms.CharField(label='新密码', widget=forms.TextInput())


# 处理文章的增删改
class Edit_post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'tag', 'category', 'body']
