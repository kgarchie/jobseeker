import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import AdvancedUser, UserCreationForm
from .models import User_data, Jobs, UserJobs
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    context = {}
    jobsL = Jobs.objects.all().values('location').distinct()
    if request.user:
        db_user = User_data.objects.filter(id=request.user.id)
        context = {
            'db_user': db_user,
        }
    new_context = {
        'jobs': jobsL,
    }
    context.update(new_context)
    return render(request, 'index.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('application:home')
        else:
            context = {
                'errors': "User does not exist",
            }
            return render(request, 'login.html', context)
    return render(request, 'login.html')


@login_required(login_url='application:login')
def profile(request):
    user_data_date_birth = datetime.datetime.now().strftime("%Y-%m-%d")
    user_data_date_grad = datetime.datetime.now().strftime("%Y-%m-%d")
    try:
        user_data = User_data.objects.get(user=request.user)
    except Exception as e:
        print(e)
        user_data = None
    if user_data is not None:
        if user_data.dog is not None:
            user_data_date_grad = user_data.dog.strftime("%Y-%m-%d")
        if user_data.dob is not None:
            user_data_date_birth = user_data.dob.strftime("%Y-%m-%d")
        context = {
            'user_data': user_data,
            'user_data_dog': str(user_data_date_grad),
            'user_data_dob': str(user_data_date_birth),
        }
        return render(request, 'profile.html', context)
    return render(request, 'profile.html')


def update_details(request):
    if request.method == 'POST':
        try:
            db_user = User_data.objects.get(id=request.user.id)
        except Exception as e:
            print(e)
            db_user = None

        city = request.POST['city']
        highQ = request.POST['highQ']
        institution = request.POST['institution']
        gender = request.POST['gender']
        dog = request.POST['dog']
        dob = request.POST['dob']
        cv = request.POST['cv']

        if db_user is not None:
            print('Got Em!')
            if cv:
                User_data.objects.filter(id=request.user.id).update(cv=cv)
            User_data.objects.filter(id=request.user.id).update(city=city, highQ=highQ, institution=institution,
                                                                gender=gender, dog=dog, dob=dob)
        else:
            user = User_data.objects.create(id=request.user.id, user=request.user, city=city, highQ=highQ,
                                            institution=institution, gender=gender, dog=dog)
            user.save()
    return redirect('application:profile')


def register(request):
    form = UserCreationForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = form.save(commit=False)
            if user is not None:
                User.objects.create_user(username=username, email=email, password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                return redirect('application:home')
    return render(request, 'registration/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('application:login')


def about(request):
    return render(request, 'about.html')


def jobs(request):
    job = Jobs.objects.all()
    context = {
        'jobs': job,
    }
    return render(request, 'jobs.html', context)


@login_required(login_url='application:login')
def applied_jobs(request):
    user_jobs = UserJobs.objects.get(id=request.user.id).job.all()
    if user_jobs:
        return render(request, 'user_jobs.html', {'jobs': user_jobs})
    if 'next' in request.POST:
        return redirect(request.POST['next'])
    return render(request, 'no-jobs.html')


def details(request, id):
    job = Jobs.objects.get(id=id)
    job_qualification = job.qualifications
    user_qualification = get_object_or_404(User, pk=request.user.id)
    if job_qualification == user_qualification:
        qualified = True
    else:
        qualified = False
    context = {
        'job': job,
        'qualified': qualified,
    }
    return render(request, 'details.html', context)


def search(request):
    if request.method == 'POST':
        q = request.POST['q-text']
        location = request.POST['location']

        result = Jobs.objects.all().filter(description__icontains=q)
        context = {
            'results': result
        }
        return render(request, 'result.html', context)
    return redirect(request, 'jobs.html')


def apply(request, id):
    if request.method == 'POST':
        user = request.user
        check_user_database = User_data.objects.filter(id=request.user.id)
        if check_user_database:
            user_qualifications = User_data.objects.get(id=user.id).highQ
            selected_job = Jobs.objects.get(id=id)
            if user_qualifications == selected_job.qualifications:
                user_jobs = UserJobs.objects.create(id=request.user.id, user=User_data.objects.get(id=request.user.id))
                user_jobs.job.add(selected_job)
                user_jobs.save()
                selected_job.applied = selected_job.applied + 1
                selected_job.vacancies = selected_job.vacancies - 1
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                return render(request, 'success.html')
            return render(request, 'failed.html')
        return redirect('application:profile')
    return render(request, 'failed.html')


def update_pic(request):
    if request.method == 'POST':
        try:
            user = User_data.objects.get(id=request.user.id)
            user.profile_pic = request.POST['pic']
            user.save()
        except Exception as e:
            print('Created')
            print(e)
            pic = User_data.objects.create(id=request.user.id, user=request.user, profile_pic=request.POST['pic'])
            pic.save()
            print(pic.url)
    return redirect('application:profile')


def upload_cv(request):
    if request.method == 'POST':
        try:
            user = User_data.objects.get(id=request.user.id)
            user.cv = request.POST['cv']
            user.save()
        except Exception as e:
            print(e)
            user = User_data.objects.create(id=request.user.id, user=request.user, cv=request.POST['cv'])
            user.save()
            return render(request, 'upload_success.html')
    return redirect('application:profile')


def all_users(request):
    if request.user.is_staff:
        users = User.objects.all()
        context = {
            'users': users,
        }
        return render(request, 'edit.html', context)
    return render(request, 'access_denied.html')


def filters(request):
    if request.user.is_staff:
        users = UserJobs.objects.all()
        if request.method == 'POST':
            gender_filter = request.POST['gender']
            if gender_filter == 'male':
                users = UserJobs.objects.all().filter(user__gender='Male')
            elif gender_filter == 'female':
                users = UserJobs.objects.all().filter(user__gender='Female')
            elif gender_filter == 'non-binary':
                users = UserJobs.objects.all().filter(user__gender='Non-Binary')
            context = {
                'users': users
            }
            return render(request, 'filters.html', context)
        context = {
            'users': users
        }
        return render(request, 'filters.html', context)
    return render(request, 'access_denied.html')
