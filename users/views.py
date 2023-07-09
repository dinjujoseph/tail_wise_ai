from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .detector import classify_dog_breed #Do breed detector
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm,ImageUploadForm
from django.conf import settings
from .models import UploadedImage
from django.http import JsonResponse
from django.core.mail import send_mail
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        uploaded_image = UploadedImage.objects.create(image=image)
        # You can perform additional operations with the uploaded image
        return render(request, 'success.html')
    return render(request, 'upload.html')
def home(request):
    return render(request, 'users/home.html')


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            #Sending welcome mail
            email = form.cleaned_data.get('email')
            send_mail(
            "Welcome to Tail WISE AI",
            "Here is the message.",
            "mailtotailwise@gmail.com",
            [email]            
            )    

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')           
            return redirect(to='users-profile')
    else:
        
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def dog_profile_edit(request):
    if request.method == 'POST':
        profile_id=request.POST.get("profile_id", "")
        profile_id_edit=UploadedImage.objects.all().filter(id=profile_id)
        profile_name=''
        profile_id=''
        profile_age=''
        data={}
        for item in profile_id_edit:

            print(item.id)
            print(item.name)
            print(item.age)
            data['profile_name']=item.name
            data['profile_age']=item.age
            data['profile_id']=item.id

            # exit('asdasds')
        return JsonResponse(data)    
        # return render(request, 'users/dog_profile.html', {'name': profile_name,'age':profile_age,'id':profile_id})
        # return {'name':images.name}
        # print(images)

@login_required
def delete_dog_profile(request):
    data={}
    data['deleted']=False
    if request.method == 'POST':
        profile_id=request.POST.get("profile_id", "")
        if profile_id:
            UploadedImage.objects.filter(id=profile_id).delete()
            data['deleted']=True
            

    return JsonResponse(data)        

@login_required
def watch_my_dog(request):
    return render(request, 'users/watch_my_dog.html', {})
    # data={}
    # data['deleted']=False
    # if request.method == 'POST':
    #     profile_id=request.POST.get("profile_id", "")
    #     if profile_id:
    #         UploadedImage.objects.filter(id=profile_id).delete()
    #         data['deleted']=True
            

    # return JsonResponse(data) 


@login_required
def dog_profile(request):
    if request.method == 'POST':
        profile_id=request.POST.get("edit_id", "")
        if profile_id:
            if request.FILES:
                old_image = UploadedImage.objects.get(id=profile_id)
                form = ImageUploadForm(request.POST, request.FILES, instance=old_image)
                if form.is_valid():
                    # form.save()
                    portfolio = form.save(commit=False)
                    portfolio.save()
                    image_path_temp=settings.MEDIA_ROOT+'/'+str(portfolio.image)
                    print(image_path_temp)


                # print(classify_dog_breed(image_path_temp))
                    breed_detected=classify_dog_breed(image_path_temp)
                    if breed_detected:
                        breed_detected=breed_detected.replace('_',' ')
                        breed_detected=breed_detected.title()
                        t = UploadedImage.objects.get(id=portfolio.id)
                        t.name=request.POST.get("name", "")
                        t.age=request.POST.get("age", "")
                        t.breed = breed_detected  # change field

                        t.save() # this will update only
                    else:
                        #No breed detected
                        t = UploadedImage.objects.get(id=portfolio.id)
                        t.name=request.POST.get("name", "")
                        t.age=request.POST.get("age", "")
                        t.breed = 'Unknown'  # change field
                        t.save() # this will update onl

                    # image_path = old_image.image_document.path
                    # if os.path.exists(image_path):
                    #     os.remove(image_path)

            else:
                print('File not foun')    
           

            # print(request.POST.get("name", ""))
                t = UploadedImage.objects.get(id=profile_id)
                t.name=request.POST.get("name", "")
                t.age=request.POST.get("age", "")
            # t.image=request.POST.get("image", "")
                t.save()
            messages.success(request, 'Your Data is updated successfully')
            return redirect(to='dog-profile')



        else:
            
        # print(request.POST)
            form = ImageUploadForm(request.POST, request.FILES)
            # messages.info(request, "Detecting Dog Breed please hold on....")
            # print(form.is_valid())
            if form.is_valid():
                # print(form)
                # form.save()
                portfolio = form.save(commit=False)
                # print(request.FILES)
                portfolio.user = request.user  # The logged-in user
                
                # print(portfolio.id)
                # print(portfolio.image)
                portfolio.save()
                # print(settings.MEDIA_ROOT+str(portfolio.image))
                image_path_temp=settings.MEDIA_ROOT+'/'+str(portfolio.image)
                print(image_path_temp)
                # print(classify_dog_breed(image_path_temp))
                breed_detected=classify_dog_breed(image_path_temp)
                if breed_detected:
                    breed_detected=breed_detected.replace('_',' ')
                    breed_detected=breed_detected.title()
                    t = UploadedImage.objects.get(id=portfolio.id)
                    t.breed = breed_detected  # change field
                    t.save() # this will update only
                else:
                    #No breed detected
                    t = UploadedImage.objects.get(id=portfolio.id)
                    t.breed = 'Unknown'  # change field
                    t.save() # this will update only
                        
                # if breed_detected:
                #     portfolio.breed=breed_detected
                # else:
                #     portfolio.breed='Unable_to_detect'    

                
                
                # verification = ImageUploadForm.objects.get(id=portfolio.id)
                # print(verification)
                # return HttpResponseRedirect(reverse_lazy('home', kwargs={'pk': pk}))
            messages.success(request, 'Your Image is updated successfully')           

            # context = self.get_context_data(form=form)
            # return self.render_to_response(context)     
            return redirect(to='dog-profile')
    else:

        images=UploadedImage.objects.all().filter(user_id=request.user.id).order_by('-uploaded_at')
        # images= UploadedImage(instance=request.user)
        # print(images)
        # profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/dog_profile.html', {'images': images})
