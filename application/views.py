from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import AdvancedUser, UserCreationForm
from .models import User_data, Jobs, UserJobs
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    jobsL = Jobs.objects.all().values('location').distinct()
    context = {
        'jobs': jobsL
    }
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
    sys_user = request.user
    form = AdvancedUser()
    if request.method == 'POST':
        db_user = User_data.objects.get_or_create(id=sys_user.id)
        if db_user:
            print('Got Em!')
            city = request.POST['city']
            highQ = request.POST['highQ']
            institution = request.POST['institution']
            gender = request.POST['gender']
            dog = request.POST['dog']
            print(gender)

            if db_user is not None:
                User_data.objects.create(user=request.user, city=city, highQ=highQ, institution=institution,
                                         gender=gender, dog=dog)
                return render(request, 'profile.html', {'db_user': db_user})
    context = {
        'sys_user': sys_user,
        'form': form,
    }
    return render(request, 'profile.html', context)


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
    user_job = UserJobs.objects.filter()
    if user_job:
        if 'next' in request.POST:
            return redirect(request.POST['next'])
        return render(request, 'jobs.html', {'jobs': user_job})

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
        check_user_database = User_data.objects.get(user=user)
        if check_user_database:
            user_qualifications = User_data.objects.get(user=user).highQ
            selected_job = Jobs.objects.get(id=id)
            if user_qualifications == selected_job.qualifications:
                selected_job.applied += 1
                selected_job.vacancies -= 1
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                return render(request, 'success.html')
            return render(request, 'failed.html')
        return redirect('application:membership')
    return render(request, 'failed.html')


def update_pic(request):
    if request.method == 'POST':
        try:
            user = User_data.objects.get(id=request.user.id)
            user.profile_pic = request.POST['pic']
        except Exception:
            print('Created')
            User_data.objects.get_or_create(user=request.user, profile_pic=request.POST['pic'])
    return redirect('application:profile')
