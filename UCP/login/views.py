"""
Views file for Login App

contains views for the frontend pages of the Login App
"""

from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.views.generic import View


from discussion.functions import get_top_discussions
from discussion.models import Tag
from login.functions import login, register, forgot_password, reset_password, get_response_text, get_user_details, update_profile
from login.functions import get_user_profile, verify_email
from login.models import UserProfile
from news_event.functions import get_top_news, get_top_events
from result.functions import get_top_results
from schedule.functions import get_top_schedules
from news_event.models import Event
from UCP.constants import result
from UCP.functions import get_base_context


class Login(View):
    """
    This view class handles login of a user to the portal
    """
    def get(self, request):
        """
        returns the login/register page.
        If the user is already logged in then this returns the home page
        """
        context = {}
        context["is_login_page"] = True
        
        if request.user.is_authenticated() and UserProfile.objects.filter(user=request.user).exists():
            
            context = get_base_context(request)
            return render(request, 'home.html', context)
            
        return render(request, 'login-register.html', context)
        
        response = login(request)
        
        if response["result"] == result.RESULT_SUCCESS:
            context = get_base_context(request)
            return render(request, 'home.html', context)
        else:
            context["message"] = get_response_text(response)
        
            return render(request, 'login-register.html', context)
    
    def post(self, request):
        """
        endpoint for the login form submission
        """
        context = {}
        context["is_login_page"] = True
        
        if request.user.is_authenticated() and UserProfile.objects.filter(user=request.user).exists():
            context = get_base_context(request)
            return render(request, 'home.html', context)
        
        response = login(request)
        
        if response["result"] == result.RESULT_SUCCESS:
            context = get_base_context(request)
            return render(request, 'home.html', context)
        else:
            context["message"] = get_response_text(response)
        
            return render(request, 'login-register.html', context)


class Logout(View):
    
    def get(self, request):
        """
        Logs out the user using the django.contrib.auth.logout function
        """
        django_logout(request)
        return redirect('/user/login')


class Register(View):
    """
    Handles Users registration to the portal
    
    """
    def get(self, request):
        """
        Returns the login register page.
        If the user is already logged in, it returns the home page
        """
        context = {}
        if request.user.is_authenticated() and UserProfile.objects.filter(user=request.user).exists():
            context = get_base_context(request)
            return render(request, 'home.html', context)
        return render(request, 'login-register.html')
        
    def post(self, request):
        """
        endpoint for the user registeration form
        """
        context={}
        
        response = register(request)
        
        context["message"] = get_response_text(response)
        
        return render(request, 'login-register.html', context)


class ForgotPassword(View):
    
    def get(self, request):
        """
        recieves the email of the user as a GET parameter and sends a password reset email if the email 
        belongs to a valid user
        """
        context={}
        response = forgot_password(request)
        context["message"] = get_response_text(response)
        
        if(response["result"] == 0):
            context["is_login_page"] = True
            print context
            return render(request, 'login-register.html', context)
        if(response["result"] == 1):
            return render(request, 'reset-password.html', context)


class ResetPassword(View):

   def post(self, request):
       """
       Resets user password using a code mailed to the user
       """
       context={}
       response = reset_password(request)
       context["message"] = get_response_text(response)

       if(response["result"] == 1):
           context["is_login_page"] = True
           return render(request, 'login-register.html', context)
       if(response["result"] == 0):
           return render(request, 'reset-password.html', context)


class PendingEvents(View):
    
    def get(self, request):
        """
        Display a list of events pending for approval
        visible only to users with a moderator status
        """
        context = {}
        user = get_user_details(request)
        context["user"] = user
        
        if not user["is_moderator"]:
            return redirect('/user/login/')
            
        context["pending_events"] = Event.objects.pending()
        return render(request, 'pending-events.html', context)


class ApproveEvent(View):
    
    def get(self, request, pk):
        """
        Change status of a pending event with id pk to approved
        visible only to users with a moderator status
        """
        user = get_user_details(request)
        context = {}
        
        context["user"] = user
        
        if not user["is_moderator"]:
            return redirect('/user/login/')
        
        
        Event.objects.filter(pk = pk).update(is_approved = True)
        context["pending_events"] = Event.objects.pending()
        
        return render(request, 'pending-events.html', context)


class RejectEvent(View):
    
    def get(self, request, pk):
        """
        Change status of a pending event with id pk to rejected
        visible only to users with a moderator status
        """
        user = get_user_details(request)
        context = {}
        
        context["user"] = user
        
        if not user["is_moderator"]:
            return redirect('/user/login/')
        
        
        Event.objects.filter(pk = pk).update(is_rejected = True)
        context["pending_events"] = Event.objects.pending()
        
        return render(request, 'pending-events.html', context)


class EditProfile(View):
    
    def get(self, request):
        """
        returns the edit profile page for the user
        """
        context={}
        
        user = get_user_details(request)
        context["user"] = user
        if user["gender"] == "male":
            context["male"] = True
        else:
            context["male"] = False
            
        return render(request, 'edit-profile.html', context)
    
    def post(self, request):
        """
        end point for the edit profile form
        """
        context={}
        
        response = update_profile(request)
        
        user = get_user_details(request)
        context["user"] = user
        if user["gender"] == "male":
            context["male"] = True
        else:
            context["male"] = False

       
        context["response"] = response
        
        return render(request, 'edit-profile.html', context)


class Profile(View):
    
    def get(self, request, pk):
        """
        profile page for user with id pk
        """
        context=get_base_context(request)
        
        # As base context already has a key 'user' that contains the logged in user, the details of the user with id pk, whose profile page is
        # to be displayed is saved as other_user
        context['other_user'] = get_user_profile(pk)
        
        return render(request, 'profile.html', context)


class TagPage(View):
    """
    The page for a tag, that has a tabulated list of all items which have that tag
    """
    def get(self, request):
        """
        returns tag page for tag with id pk
        """
        context=get_base_context(request)
        tag = Tag.objects.get(name = request.GET["tag"])
        context["tag"] = tag
        results = get_top_results([tag])
        schedules = get_top_schedules([tag])
        context["results"] = results
        context["schedules"] = schedules
        context["events"] = get_top_events([tag])
        
        context["news_list"] = get_top_news([tag])
        context["discussions"] = get_top_discussions([tag])
        
        return render(request, 'tag_page.html', context)


class VerificationPage(View):
    """
    page for the verifying user's email id. the link to this page is send in the verificaion email
    """
    def get(self, request):
        
        context={}
        
        response = verify_email(request)
        
        context["response"] = response
        
        return render(request, 'email-verification.html', context)
        
        
        
        
