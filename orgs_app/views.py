from django.shortcuts import redirect, render
import bcrypt
from django.contrib import messages
from .models import *
from django.db.models import Count


def index(request):
    return render(request, 'index.html')


def user_id(request, user_id):
    context = {
        'one_user': User.objects.get(id=user_id)
    }
    return render(request, 'index.html', context)


def create_user(request):
    if request.method =='POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect('/groups')
    return redirect('/')


def login(request):
    if request.method =='POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    if request.method == 'POST':
        users_with_email = User.objects.filter(email=request.POST['email'])
        if users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                print(request.method)
                request.session['user_id'] = user.id
                return redirect('/groups')
        messages.error(request, "Email or Password incorrect")
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')


def main_page(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'all_orgs': Org.objects.annotate(members=Count('user_who_joined')).order_by('-user_who_joined'),
        # Line below used to create a new key:value pair to connect a way to sort your "thing", in this case "members" = "liked_by" found in the Org Model class)
        # 'sorted_orgs': Org.objects.annotate(members=Count('user_who_joined')).order_by('-members')
    }
    return render(request, 'main_page.html', context)


def create_org(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method =='POST':
        errors = Org.objects.org_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/groups')
        else:
            current_user = User.objects.get(id=request.session['user_id'])
            each_org = Org.objects.create(name=request.POST['name'], desc=request.POST['desc'], added_by=User.objects.get(id=request.session['user_id']))
            each_org.user_who_joined.add(current_user)
            return redirect('/groups')
    return redirect('/groups')


def details(request, org_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user': User.objects.get(id=request.session['user_id']),
        'thisOrg': Org.objects.get(id=org_id),
        'all_orgs': Org.objects.all(),
    }
    return render(request, 'details.html', context)


def join(request, org_id):
    if 'user_id' not in request.session:
        return redirect('/')
    # if request.method == "POST":
    current_user = User.objects.get(id=request.session['user_id'])
    each_org = Org.objects.get(id=org_id)
    each_org.user_who_joined.add(current_user)
    return redirect(f'/groups/{org_id}')


def leave(request, org_id):
    if 'user_id' not in request.session:
        return redirect('/')
    # if request.method == "POST":
    current_user = User.objects.get(id=request.session['user_id'])
    each_org = Org.objects.get(id=org_id)
    each_org.user_who_joined.remove(current_user)
    return redirect(f'/groups/{org_id}')


def delete_org(request, org_id):
    if 'user_id' not in request.session:
        return redirect('/')
    org_to_delete = Org.objects.get(id=org_id)
    org_to_delete.delete()
    return redirect('/groups')
