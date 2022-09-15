from random import Random

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail

from blog.models import Post
from .forms import LoginForm, RegisterForm, Find_pwd, Commit_form, Edit_post
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def login_(request):
    if request.session.get('is_login', None):
        messages.add_message(request, messages.SUCCESS, '你已登录，无需重复登录！', extra_tags='success')
        return redirect('blog:index')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # user = User.objects.get(username=name)
            user = authenticate(username=name, password=password)
            if user:
                messages.add_message(request, messages.SUCCESS, '登录成功！', extra_tags='success')
                request.session['is_login'] = True
                request.session['username'] = name
                request.session['password'] = password
                return redirect('blog:index')
            else:
                messages.add_message(request, messages.ERROR, '用户名或密码错误！', extra_tags='danger')
                return render(request, 'login.html', {'form': form})
    form = LoginForm()
    messages.add_message(request, messages.ERROR, '验证码或密码输入有误！', extra_tags='danger')
    return render(request, 'login.html', {'form': form})


def register(request):
    # if request.session.get('is_login', None):
    #     messages.add_message(request, messages.SUCCESS, '你已登录，无需注册！', extra_tags='success')
    #     return redirect('blog:index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            if password1 != password2:
                messages.add_message(request, messages.ERROR, '两次输入密码不一致！', extra_tags='danger')
                return render(request, 'login.html', locals())
            else:
                password = make_password(password1)
                same_user = User.objects.filter(username=name)
                if same_user:
                    messages.add_message(request, messages.ERROR, '该用户名已存在！', extra_tags='danger')
                    return render(request, 'login.html', locals())
                same_email = User.objects.filter(email=email)
                if same_email:
                    messages.add_message(request, messages.ERROR, '该邮箱已注册！', extra_tags='danger')
                    return render(request, 'login.html', locals())
                date = dict(username=name,
                            password=password1,
                            email=email,
                            is_staff=1,
                            is_superuser=0,
                            )
                user1 = User.objects.create_user(**date)
                user1.save()
                messages.add_message(request, messages.SUCCESS, '注册成功,请登录！', extra_tags='success')
                return redirect('more:login')
        else:
            messages.add_message(request, messages.ERROR, '验证码或密码错误！', extra_tags='danger')
            return render(request, 'register.html', {'form': form})
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    if not request.session.get('is_login', None):
        messages.add_message(request, messages.ERROR, '你还没有登录，请登录！', extra_tags='success')
        return redirect('more:login')
    request.session.flush()
    messages.add_message(request, messages.SUCCESS, '退出成功！', extra_tags='success')
    return redirect('blog:index')


#  邮箱验证码模块
# 随机生成验证码
def random_str(randomlength=4):
    str1 = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str1 += chars[random.randint(0, length)]
    return str1


def findpwd(request):
    if request.method == "POST":
        form = Find_pwd(request.POST)
        # Commit = Commit()
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            user = User.objects.get(username=username)
            if user.email == email:
                email_title = "找回密码"
                code = random_str()  # 随机生成的验证码
                request.session["code"] = code  # 将验证码保存到session
                request.session["commitusername"] = username
                email_body = "验证码为：{0}".format(code)
                send_status = send_mail(email_title, email_body, "653826174@qq.com", ["lsl18571156682@gmail.com", ])
                messages.add_message(request, messages.SUCCESS, '邮件发送成功，注意查收！', extra_tags='success')
                return redirect('more:commit')
            else:
                messages.add_message(request, messages.ERROR, '用户名与邮箱不匹配！', extra_tags='danger')
                return render(request, "findpwd.html", {'form': form, 'Commit': Commit, 'user': user})

    form = Find_pwd()
    # Commit = Commit()
    return render(request, "findpwd.html", {'form': form, 'Commit': Commit})


# 处理提交的邮箱验证码
def Commit(request):
    if request.method == 'POST':
        username = request.session["commitusername"]
        print(username)
        form = Commit_form(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get("code")  # 获取传递过来的验证码
            password = form.cleaned_data.get('password')
            user = User.objects.get(username=username)
            if code == request.session["code"]:
                user.set_password(password)
                user.save()
                print("保存成功")
                del request.session["code"]  # 删除session
                request.session.flush()
                messages.add_message(request, messages.SUCCESS, '重置密码完成，去登录！', extra_tags='success')
            return redirect('more:login')
        else:
            messages.add_message(request, messages.SUCCESS, '验证码输入错误，请重新输入！！', extra_tags='success')
            return render(request, 'commit_code.html', {'commit': commit})
    commit = Commit_form()
    return render(request, 'commit_code.html', {'commit': commit})


# 处理文章的增删改
def post_add(request):
    if request.method == 'POST':
        form = Edit_post(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get("body"))
            form.author = author
            form.save()

    return render(request, 'new.html', {'form': form})


def post_update(request, pk):
    # author = ?
    if request.method == 'POST':
        form = Edit_post(request.POST)
        if form.is_valid():
            form.author = author
            form.save()

    form = Edit_post()
    post = Post.objects.get(id=106)
    form = Edit_post(instance=post)
    return render((request, 'new.html', {'form': form}))


def post_delete(request, pk):
    print("??")
    post = get_object_or_404(Post, id=pk)
    print("???")
    # post.delete()
    messages.add_message(request, messages.SUCCESS, '删除文章成功！', extra_tags='success')
    # author = ?
    # author.delete
    return redirect('blog:index')
