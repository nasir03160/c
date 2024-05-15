from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# from . import models
from django.contrib.auth.decorators import login_required
from core.models import Profile
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from .models import ChatLogEntry


# Create your views here.
@login_required(login_url='signin')
def index(request):
 return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        student_id = request.POST.get('student_id', None)  # Handle optional field
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Validate data
        if not username:
            messages.info(request, 'Please enter a username.')
            return redirect('signup')
        if not email:
            messages.info(request, 'Please enter an email address.')
            return redirect('signup')
        if password != password2:
            messages.info(request, 'Passwords do not match.')
            return redirect('signup')

        # Check for existing email or username
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email is already taken.')
            return redirect('signup')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken.')
            return redirect('signup')

        # Create user and profile
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Log user in
        user_login = authenticate(username=username, password=password)
        login(request, user_login)

        # Create a profile object for the new user
        new_profile = Profile.objects.create(user=user, student_id=student_id)
        new_profile.save()

        return redirect('signin')
    else:
        return render(request, 'signup.html')
 
 
 

def signin(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user  = authenticate(username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else: 
      messages.info(request, 'Credentials Invalid')
      return redirect('/signin')
  else:
    return render(request,"signin.html")
  
@login_required(login_url='signin')
def Logout(request):
  logout(request)
  return redirect('signin')
@login_required(login_url='signin')
def Settings(request):
  return render(request, 'settings.html')


@login_required  # Require user to be logged in
def analyze_input(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        logged_in_user = request.user

        # Perform your analysis logic here based on user_input
        # Here's an example adding 3 to the user input
        analysis_result = f"Your input analyzed! The result is: {int(user_input) + 3}"

        # Save the entry to the database
        ChatLogEntry.objects.create(
            user=logged_in_user,
            user_input=user_input,
            analysis_result=analysis_result
        )

        # Format the output for display (optional)
        formatted_output = f"<p>Your input: {user_input}</p><p>Analysis: {analysis_result}</p>"

        return JsonResponse({'output': formatted_output})
    else:
        return HttpResponseBadRequest()