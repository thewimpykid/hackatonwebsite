from django.shortcuts import render, redirect
from .forms import RegisterForm, CompetitionForm, SubmissionForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Competition, Submission
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
import stripe

def home(request):
    return render(request, './html/home.html')

@login_required(login_url="/login")
def dashboard(request):
    
    submissions = Submission.objects.all()
    user_submissions = submissions.filter(user=request.user)
    competitions = Competition.objects.all()
    join_list = {}
    run = False
    for competition in competitions:
        run = False # {} {}
        for submission in user_submissions:
            if run:
                break
            if (submission.competition.title != competition.title):
                print(submission.competition.title, "then", competition.title)
                if competition.title in join_list == False:
                    join_list[competition.title].setdefault(False)
                    run = True
                    break
                else:
                    join_list.update({competition.title: False})
                    run = True
                    break
            elif (submission.competition.title == competition.title):
                print(submission.competition.title, "then", competition.title)
                if competition.title in join_list == False:
                    join_list[competition.title].setdefault(True)
                    run = True
                    break
                else:
                    join_list.update({competition.title: True})
                    run = True
                    break
        

    if request.method == "POST":
        competition_id = request.POST.get("competition-id")
        
        if competition_id:
            competition = Competition.objects.filter(id=competition_id).first()
            if competition:
                # competition_submissions = submissions.filter(competition=competition)
                # # data = Data.objects.create(title=competition.title)
                # data = Data(title=competition.title, submissions = competition_submissions.items())
                # data.save()
                # # for submission in competition_submissions:
                # #     data.submissions.add(data)
                competition.delete()
                return redirect('/dashboard')


    return render(request, './html/dashboard.html', {"competitions":competitions, "submissions": user_submissions, "join_list": join_list.items()})

def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')

    else:
        form = RegisterForm()
    
    return render(request, './html/sign_up.html', {"form": form})

@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/dashboard')

    else:
        form = CompetitionForm()
    
    return render(request, './html/create.html', {"form": form})

@login_required(login_url="/login")
def join(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.save()
            return redirect('/dashboard')
    else:
        form = SubmissionForm()

    return render(request, './html/join.html', {"form": form, "key": key})

# @login_required(login_url="/login")
def charge(request):
    if request.method == "POST":
        competition = request.POST.get("competition")
        project_desc = request.POST.get("project_desc")
        video = request.POST.get("video")
        submission = Submission(user=request.user, competition=competition, project_desc=project_desc, video=video)
        submission.save()
        charge = stripe.Charge.create(
            amount=500,
            currency="usd",
            description="Joined Competition",
            source=request.POST['stripeToken'],
            api_key=settings.STRIPE_SECRET_KEY
        )
        return redirect('/dashboard')
    

    return render(request, './html/charge.html', {})

@login_required(login_url="/login")
def data(request):
    competitions = Competition.objects.all()
    submissions = Submission.objects.all()
    return render(request, './html/data.html', {"competitions": competitions, "submissions": submissions})

