from datetime import datetime
import random
import re
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.db import transaction
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Response, State, workers, users, ServiceCatogarys, Country, City, Feedback, ServiceRequests, Contact, ServiceTracking, Product, Shop, AdminRegistrationRequest
from .forms import stateform, ProductForm, AdminRegistrationForm, AdminEditForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.urls import reverse



class Commenlib:
    def __init__(self):
        self.DEFAULT_REDIRECT_PATH={'ROOT':'/choose-login/'}

common_lib = Commenlib()

# Create your views here.
@method_decorator(csrf_protect, name='dispatch')
class ChooseLogin(View):
    def get(self, request):
        return render(request, 'choose_login.html')

@method_decorator([csrf_protect, ensure_csrf_cookie], name='dispatch')
class Login(View):
    def get(self, request):
        login_type = request.GET.get('type', 'user')
        response = render(request, 'login.html', {'login_type': login_type})
        response.set_cookie('csrftoken', request.META.get('CSRF_COOKIE', ''), samesite='Lax')
        return response
        
    def post(self, request):
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        login_type = request.POST.get('login_type', 'user')
        
        if not username or not password:
            return render(request, 'login.html', {
                'error_msg': "Please provide both username and password.",
                'login_type': login_type
            })
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if login_type == 'admin' and user.is_superuser and user.is_staff:
                login(request, user)
                return HttpResponseRedirect('/admmin_home')
            elif login_type == 'worker' and user.is_staff and not user.is_superuser:
                login(request, user)
                return HttpResponseRedirect('/workers_home')
            elif login_type == 'user' and not user.is_staff and not user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'login.html', {
                    'error_msg': "Invalid login type for this user.",
                    'login_type': login_type
                })
        else:
            return render(request, 'login.html', {
                'error_msg': "Invalid username or password.",
                'login_type': login_type
            })

def logout_view(request):
    logout(request)
    return redirect('login_page')

def validate_phone_number(phone_number):
    # Remove any non-digit characters
    phone_number = re.sub(r'\D', '', phone_number)
    if len(phone_number) < 10 or len(phone_number) > 15:
        raise ValidationError('Phone number must be between 10 and 15 digits.')
    return phone_number

class User_Register(View):
    def get(self, request):
        return render(request, 'user_register.html')

    def post(self,request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        contact_number = request.POST.get('contactnumber')
        address = request.POST.get('address')
        profile_pics = request.FILES.get('profile_pic')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Validate email
        try:
            validate_email(email)
            if User.objects.filter(email=email).exists():
                return render(request, 'user_register.html', {'msg': "Email already exists!"})
        except ValidationError:
            return render(request, 'user_register.html', {'msg': "Invalid email format!"})

        # Validate phone number
        try:
            contact_number = validate_phone_number(contact_number)
        except ValidationError as e:
            return render(request, 'user_register.html', {'msg': str(e)})

        # Check if passwords match
        if password == cpassword:
            new_user = User.objects.create(
                username=email,
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name,
                is_active=True,
                is_staff=False,
            )

            users.objects.create(
                admin=new_user, 
                Address=address, 
                gender=gender, 
                contact_number=contact_number,
                profile_pic=profile_pics
            )
            return render(request, 'login.html', {'msg': "Added successfully!"})
        else:
            return render(request, 'user_register.html', {'msg': "Passwords do not match!"})




class Worker_Register(View):
    def get(self, request):
        designations=ServiceCatogarys.objects.all()
        contaxt={
            'designations':designations,
        }
        return render(request, 'workers_registration.html',contaxt)

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contactnumber = request.POST.get('contactnumber')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        address = request.POST.get('address')
        designation = request.POST.get('designation')
        profile_pic = request.FILES.get('profile_pic')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Validate email
        try:
            validate_email(email)
            if User.objects.filter(email=email).exists():
                return render(request, 'workers_registration.html', {'msg': "Email already exists!"})
        except ValidationError:
            return render(request, 'workers_registration.html', {'msg': "Invalid email format!"})

        # Validate phone number
        try:
            contactnumber = validate_phone_number(contactnumber)
        except ValidationError as e:
            return render(request, 'workers_registration.html', {'msg': str(e)})

        # Check if passwords match
        if password == cpassword:
            new_user = User.objects.create(
                username=email,
                email=email,
                password=make_password(password),
                first_name=firstname,
                last_name=lastname,
                is_active=True,
                is_staff=True,
            )

            new_worker = workers(
                admin=new_user, 
                contact_number=contactnumber, 
                dob=dob, 
                Address=address, 
                city=city,
                gender=gender, 
                designation=designation, 
                profile_pic=profile_pic,
                acc_activation=False, 
                avalability_status=True
            )
            new_worker.save()

            return render(request, 'login.html', {'msg': "Added successfully!"})
        else:
            return render(request, 'workers_registration.html', {'msg': "Passwords do not match!"})




class home(LoginRequiredMixin, View):
    login_url = '/choose-login/'
    def get(self, request):
        services = ServiceCatogarys.objects.all()
        feedbacks = Feedback.objects.select_related('User').all()
        all_services = list(ServiceCatogarys.objects.all())  # Convert QuerySet to a list
        num_services = min(len(all_services), 3)  # Get either 3 or the total number of services, whichever is smaller
        selected_services = random.sample(all_services, num_services) if num_services > 0 else []
        print('services:', services)
        context = {
            'services': services,
            'feedbacks': feedbacks,
            'selected_services': selected_services,
        }
        return render(request, 'userpages/index.html', context)

class about(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        return render(request, 'userpages/about.html')
    
class services(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        services = ServiceCatogarys.objects.all()
        feedbacks = Feedback.objects.select_related('User').all()
        all_services = list(ServiceCatogarys.objects.all())  # Convert QuerySet to a list
         # Select 6 random services
        print('services:', services)
        context = {
            'services': services,
            'feedbacks': feedbacks,
        }
        return render(request,'userpages/service.html',context)
class bookservice(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,id):
        services = ServiceCatogarys.objects.get(id=id)
        city=City.objects.all()
        context = {
            'services': services,
            'city': city,
        }
        return render(request,'userpages/servicebook.html',context)
    
    def post(self,request,id):
        user_id = request.user.id
        try:
            # First try to get user profile
            user = users.objects.get(admin=user_id)
        except users.DoesNotExist:
            # If user profile not found, check if it's a worker
            try:
                worker = workers.objects.get(admin=user_id)
                return HttpResponse("Workers cannot book services. Please log in as a regular user to book services.")
            except workers.DoesNotExist:
                # If neither user nor worker found
                return HttpResponse("Profile not found. Please contact administrator.")

        services = ServiceCatogarys.objects.get(id=id)
        city_list = City.objects.all()
        
        # Get form data
        problem_description = request.POST.get('Problem_Description')
        address = request.POST.get('Address')
        city_id = request.POST.get('city')
        pin = request.POST.get('Pincode')
        house_no = request.POST.get('House_No')
        landmark = request.POST.get('landmark')
        contact = request.POST.get('contact')

        # Validate phone number
        try:
            # Remove any non-digit characters
            contact = re.sub(r'\D', '', contact)
            if len(contact) < 10 or len(contact) > 15:
                context = {
                    'services': services,
                    'city': city_list,
                    'error': 'Phone number must be between 10 and 15 digits.',
                    'form_data': request.POST  # Keep the form data
                }
                return render(request, 'userpages/servicebook.html', context)
        except Exception:
            context = {
                'services': services,
                'city': city_list,
                'error': 'Invalid phone number format.',
                'form_data': request.POST  # Keep the form data
            }
            return render(request, 'userpages/servicebook.html', context)

        # Validate city selection
        if not city_id:
            context = {
                'services': services,
                'city': city_list,
                'error': 'Please select a city',
                'form_data': request.POST  # Keep the form data
            }
            return render(request, 'userpages/servicebook.html', context)

        try:
            city = City.objects.get(id=city_id)
        except (City.DoesNotExist, ValueError):
            context = {
                'services': services,
                'city': city_list,
                'error': 'Invalid city selection',
                'form_data': request.POST  # Keep the form data
            }
            return render(request, 'userpages/servicebook.html', context)

        # Create a new ServiceRequests instance and save it
        service_request = ServiceRequests(
            user=user,
            Problem_Description=problem_description,
            service=services,
            Address=address,
            city=city,  # Use the city object directly
            pin=pin,
            House_No=house_no,
            landmark=landmark,
            contact=contact,
        )
        service_request.save()

        # Send email notifications
        # Email to admin
        admin_subject = f'New Service Booking: {services.Name}'
        admin_message = f"""
        New service booking received:
        
        Service: {services.Name}
        User: {user.admin.first_name} {user.admin.last_name}
        Contact: {contact}
        Problem Description: {problem_description}
        
        Address Details:
        House No: {house_no}
        Address: {address}
        City: {city.name}
        PIN: {pin}
        Landmark: {landmark}
        """
        
        send_mail(
            admin_subject,
            admin_message,
            settings.EMAIL_HOST_USER,  # From email
            [settings.EMAIL_HOST_USER],  # To email (admin's email)
            fail_silently=False,
        )

        # Send confirmation email to user
        user_subject = f'Service Booking Confirmation - {services.Name}'
        user_message = f"""
        Dear {user.admin.first_name} {user.admin.last_name},

        Thank you for booking our service. Your booking has been received successfully.

        Booking Details:
        Service: {services.Name}
        Problem Description: {problem_description}
        
        Address Details:
        House No: {house_no}
        Address: {address}
        City: {city.name}
        PIN: {pin}
        Landmark: {landmark}

        We will assign a service professional to your request shortly.
        You can track your service request in your account dashboard.

        Best regards,
        Home Services Team
        """
        
        send_mail(
            user_subject,
            user_message,
            settings.EMAIL_HOST_USER,  # From email
            [user.admin.email],  # To email (user's email)
            fail_silently=False,
        )

        # Redirect to a success page or any other page as needed
        return HttpResponseRedirect(reverse('index'))  # Change this to your success page URL

class admmin_home(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        total_requests = ServiceRequests.objects.count()
        completed_requests = Response.objects.filter(status=True).count()
        pending_requests = Response.objects.filter(status=False).count()
        total_users = users.objects.count()
        context = {
            'total_requests': total_requests,
            'completed_requests': completed_requests,
            'pending_requests': pending_requests,
            'total_users': total_users,
        }
        return render(request, 'adminpages/adminhompage.html',context)

class workers_home(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        total_requests = ServiceRequests.objects.count()
        completed_requests = Response.objects.filter(status=True).count()
        pending_requests = Response.objects.filter(status=False).count()
        total_users = users.objects.count()
        context = {
            'total_requests': total_requests,
            'completed_requests': completed_requests,
            'pending_requests': pending_requests,
            'total_users': total_users,
        }
        return render(request, 'workerpages/Workerhompage.html',context)
    
class contact(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        return render(request, 'userpages/contact.html')

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Create new contact message
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Send email notification
        email_subject = f'New Contact Form Submission: {subject}'
        email_message = f"""
        New contact form submission received:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message: {message}
        """
        
        # Send email to admin
        send_mail(
            email_subject,
            email_message,
            settings.EMAIL_HOST_USER,  # From email
            [settings.EMAIL_HOST_USER],  # To email (admin's email)
            fail_silently=False,
        )

        # Send confirmation email to user
        confirmation_subject = 'Thank you for contacting us'
        confirmation_message = f"""
        Dear {name},

        Thank you for contacting us. We have received your message and will get back to you shortly.

        Your message details:
        Subject: {subject}
        Message: {message}

        Best regards,
        Home Services Team
        """
        
        send_mail(
            confirmation_subject,
            confirmation_message,
            settings.EMAIL_HOST_USER,  # From email
            [email],  # To email (user's email)
            fail_silently=False,
        )

        return render(request, 'userpages/contact.html', {'success_message': 'Your message has been sent successfully! We will contact you soon.'})





class manageworker(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        workers_records=workers.objects.all()
        context={'workers_records':workers_records}
        return render(request,'adminpages/Manage_Workers.html',context)

class verify_worker(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request, action, id):
        btn = workers.objects.get(id=id)
        if action == 'active' and btn.acc_activation == False:
            workers.objects.filter(id=id).update(acc_activation=True)
            return HttpResponseRedirect('/manageworker')
        else:
            return HttpResponse("Something Went Wrong")
        
        return HttpResponseRedirect('/manageworker')

class manageusers(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        users_records=users.objects.all()
        context={'users_records':users_records}
        return render(request,'adminpages/View_Users.html',context)


class AddCountry(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self, request):
        return render(request, 'country.html')

    def post(self, request):
        country_name = request.POST.get('name')
        Country.objects.create(name=country_name)
        return HttpResponseRedirect('/ManageCountry')

class ManageCountry(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        Country_record=Country.objects.all()
        context={
            'Country_record':Country_record
        }
        return render(request,'adminpages/Manage_Country.html',context)
class DeleteCountry(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,id):
        data=Country.objects.get(id=id)
        data.delete()
        return HttpResponseRedirect('/ManageCountry')



class ManageState(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        State_record=State.objects.all()
        context={
            'State_record':State_record
        }
        return render(request,'adminpages/ManageState.html',context)

class AddState(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self, request):
        country_recorsd = Country.objects.all()
        return render(request, 'state.html', {'country_recorsd': country_recorsd})

    def post(self, request):
        form = stateform(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ManageState')
        else:
            # Handle the case where the form data is not valid
            country_records = State.objects.all()
            return render(request, 'state.html', {'form': form, 'country_records': country_records})

class DeleteState(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,id):
        data=State.objects.get(id=id)
        data.delete()
        return HttpResponseRedirect('/ManageState')

class managecity(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        city_records=City.objects.all()
        context={
            'city_records':city_records
        }
        return render(request,'adminpages/ManageCity.html',context)

class AddCity(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        states=State.objects.all()
        return render(request, 'city.html',{'state_recorsd':states})

    def post(self, request):
        city_name = request.POST.get('name')
        state=request.POST.get('state')
        City.objects.create(name=city_name,state=state)
        return HttpResponseRedirect('/managecity')
    
class DeleteCity(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,id):
        data=City.objects.get(id=id)
        data.delete()
        return HttpResponseRedirect('/managecity')



class AddServices(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        return render(request,'adminpages/ServiceCatogry.html')
    def post(self,request):
        Name = request.POST.get('Name')
        Description = request.POST.get('Description')
        img = request.FILES.get('img')
        ServiceCatogarys.objects.create(Name=Name,Description=Description,img=img)

        return HttpResponseRedirect("/ManageServices")



class ManageServices(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        service_records=ServiceCatogarys.objects.all()
        context= {
            'services':service_records,
        }
        return render(request,'adminpages/Manage_Services.html',context)
    

        # form = ServiceCatogoryForm(request.POST,request.FILES)
        # if form.is_valid():
        #     form.save()
        #     return HttpResponse("Ok")
        # else:
        #     return HttpResponse('wrong')

class DeleteServices(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,id):
        data = ServiceCatogarys.objects.get(id=id)
        data.delete()

        service_records=ServiceCatogarys.objects.all()
        context= {
            'services':service_records,
        }
        return render(request,'adminpages/Manage_Services.html',context)
    
class EditServices(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self, request, id):
        service = get_object_or_404(ServiceCatogarys, id=id)
        return render(request,'adminpages/ServiceCatogry.html',{'record':service})
    
    def post(self, request, id):
        service = get_object_or_404(ServiceCatogarys, id=id)
        Name = request.POST.get('Name')
        Description = request.POST.get('Description')
        img = request.FILES.get('img')

        # Update the service category fields
        service.Name = Name
        service.Description = Description
        if img:
            service.img = img
        service.save()
        return HttpResponse("Update Successful")
    
class feedback_form(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        worker = workers.objects.all()
        return render(request, 'userpages/feedback_form.html', {'workers': worker})
    def post(self,request):
        rating = int(request.POST['rating'])
        description = request.POST['description']
        user = request.user  # Get the currently logged-in user instance
        employ_id = request.POST['employ']
        employ = workers.objects.get(id=employ_id)
        date = datetime.now()

        # Create a new Feedback instance and assign the user, employ, and date
        feedback = Feedback.objects.create(Rating=rating, Description=description, User=user, Employ=employ, Date=date)
        feedback.save()

        return HttpResponse('feedback_success')

class viewfeedbacks(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        feedback_records=Feedback.objects.all()
        context= {
            'feedback_records':feedback_records,
        }
        return render(request,'adminpages/View_feedbacks.html',context)

class ViewRequests(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        request_records=ServiceRequests.objects.all()
        context={
            'request_records':request_records,
        }
        return render(request, 'adminpages/View_request.html', context)



class ViewColleagues(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        workers_records = workers.objects.all()
        context = {'workers_records': workers_records}
        return render(request, 'workerpages/View_colleagues.html', context)

# class WorkerViewRequests(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
#     def get(self,request):
#         worker=request.user.id
#         print("worker_id",worker)
        
#         request_records=ServiceRequests.objects.all()
#         Response_record=Response.objects.all()
#         wo=workers.objects.filter(admin=worker)
#         asss = Response.objects.filter(assigned_worker__admin__id=worker)
#         print(asss)
#         # =Response_record.filter
#         context={
#             'request_records':request_records,
#             'Response_record':Response_record,
#         }
#         return render(request, 'workerpages/View_request.html', context)

class WorkerViewRequests(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self, request):
        worker_id = request.user.id
        print("worker_id", worker_id)
        assigned_responses = Response.objects.filter(assigned_worker__admin__id=worker_id)
        service_ids = [response.requests.service.id for response in assigned_responses]
        request_records = ServiceRequests.objects.filter(service__id__in=service_ids)

        context = {
            'request_records': request_records,
            'assigned_responses': assigned_responses,
        }
        return render(request, 'workerpages/View_request.html', context)


class viewworkerfeedbacks(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        feedback_records=Feedback.objects.all()
        context= {
            'feedback_records':feedback_records,
        }
        return render(request,'workerpages/View_feedbacks.html',context)


class viewrequests(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        worker=request.user
        print("worker_id",worker)
        request_records=ServiceRequests.objects.all()
        context= {
            'request_records':request_records,
        }
        return render(request,'adminpages/View_request.html',context)
    
class acceptrequest(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,action,id):
        try:
            request_records = ServiceRequests.objects.get(id=id)
            
            if action == 'accept' and request_records.status == False:
                ServiceRequests.objects.filter(id=id).update(status=True)
                userid = request.user.id
                worker_id = workers.objects.get(admin=userid) 
                response = Response.objects.create(requests=request_records, assigned_worker=worker_id, status=False)
                return HttpResponseRedirect('/WorkerViewRequests')
            
            elif action == 'reject' and request_records.status == True:
                ServiceRequests.objects.filter(id=id).update(status=False)
                response = Response.objects.get(requests=request_records)
                response.delete()
                return HttpResponseRedirect('/WorkerViewRequests')
            
            return HttpResponseRedirect('/WorkerViewRequests')
            
        except ServiceRequests.DoesNotExist:
            # Handle the case when the service request doesn't exist
            messages.error(request, "The requested service does not exist.")
            return HttpResponseRedirect('/WorkerViewRequests')
        except Response.DoesNotExist:
            # Handle the case when trying to reject but response doesn't exist
            messages.error(request, "The response for this service request does not exist.")
            return HttpResponseRedirect('/WorkerViewRequests')
        except workers.DoesNotExist:
            # Handle the case when worker profile doesn't exist
            messages.error(request, "Worker profile not found.")
            return HttpResponseRedirect('/WorkerViewRequests')

class viewresponse(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        Response_records=Response.objects.all()
        context= {
            'Response_records':Response_records,
        }
        return render(request,'adminpages/view_response.html',context)
    
class workerviewresponse(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        worker_id = request.user.id
        print("worker_id", worker_id)
        assigned_responses = Response.objects.filter(assigned_worker__admin__id=worker_id)
        Response_records=Response.objects.all()
        context= {
            'Response_records':assigned_responses,
        }
        return render(request,'workerpages/viewpending_task.html',context)


class Viewappointment_history(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self, request):
            # Get the logged-in user's ID
            user_id = request.user.id

            # Query request data for the logged-in user
            requests_data = ServiceRequests.objects.filter(user__admin_id=user_id)

            # Initialize lists to store request and response data
            request_list = []
            response_list = []

            for request_data in requests_data:
                # Check if a response exists for the request
                response = Response.objects.filter(requests=request_data).first()

                if response:
                    # If a response exists, add it to the response list
                    response_list.append(response)
                else:
                    # If no response exists, add the request to the request list
                    request_list.append(request_data)

            context = {
                'requests': request_list,
                'responses': response_list,
            }

            return render(request, 'userpages/appointment_history.html', context)
    


class CancelRequest(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,id):
        if request.user.is_superuser:
            r_id=ServiceRequests.objects.get(id=id)
            r_id.delete()
            return HttpResponseRedirect('/ViewRequests')
        
        else:
            uid=request.user.id
            # admin=User.object.get(admin=uid)
            user=users.objects.get(admin=uid)
            user_id=user.id
            r_id=ServiceRequests.objects.get(Q(id=id) & Q(user=user_id))
            r_id.delete()
            return HttpResponseRedirect(reverse('index'))


class AssignWorker(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,id):
        req=ServiceRequests.objects.get(id=id)
        service=req.service.Name
        print(service)

        workers_records=workers.objects.filter(designation=service)
        # print(worker)
        context={
            'req':req,
            'workers_records':workers_records,
        }
        return render(request, 'adminpages/assign_worker.html', context)

    def post(self,request,id):
        ServiceRequests.objects.filter(id=id).update(status=True)
        worker = request.POST.get('assigned_worker')
        req=ServiceRequests.objects.get(id=id)
        print(worker)
        assigned_worker=workers.objects.get(id=worker)
        print(assigned_worker)
        worker_id=workers.objects.get(id=worker) 
        response=Response.objects.create(requests=req,assigned_worker=worker_id,status=False)

        # Send email notification to assigned worker
        worker_subject = f'New Service Assignment - {req.service.Name}'
        worker_message = f"""
        Dear {assigned_worker.admin.first_name} {assigned_worker.admin.last_name},

        You have been assigned a new service request.

        Service Details:
        Service Type: {req.service.Name}
        Problem Description: {req.Problem_Description}
        
        Customer Details:
        Name: {req.user.admin.first_name} {req.user.admin.last_name}
        Contact: {req.contact}
        
        Location Details:
        House No: {req.House_No}
        Address: {req.Address}
        City: {req.city.name}
        PIN: {req.pin}
        Landmark: {req.landmark}

        Please check your dashboard for more details and take necessary action.

        Best regards,
        Home Services Team
        """
        
        send_mail(
            worker_subject,
            worker_message,
            settings.EMAIL_HOST_USER,  # From email
            [assigned_worker.admin.email],  # To worker's email
            fail_silently=False,
        )

        # Send notification to user about worker assignment
        user_subject = f'Service Professional Assigned - {req.service.Name}'
        user_message = f"""
        Dear {req.user.admin.first_name} {req.user.admin.last_name},

        We are pleased to inform you that a service professional has been assigned to your request.

        Service Details:
        Service Type: {req.service.Name}
        Problem Description: {req.Problem_Description}
        
        Service Professional Details:
        Name: {assigned_worker.admin.first_name} {assigned_worker.admin.last_name}
        
        Your service professional will contact you shortly at the provided contact number: {req.contact}

        Location Details:
        House No: {req.House_No}
        Address: {req.Address}
        City: {req.city.name}
        PIN: {req.pin}
        Landmark: {req.landmark}

        You can track the status of your service request in your account dashboard.

        Best regards,
        Home Services Team
        """
        
        send_mail(
            user_subject,
            user_message,
            settings.EMAIL_HOST_USER,  # From email
            [req.user.admin.email],  # To user's email
            fail_silently=False,
        )

        return HttpResponseRedirect('/viewresponse')
        
class userprofile(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        id = request.user.id
        try:
            # First try to get user profile
            data = users.objects.get(admin=id)
            context = {
                'data': data,
                'is_worker': False
            }
        except users.DoesNotExist:
            try:
                # If user profile not found, try to get worker profile
                data = workers.objects.get(admin=id)
                context = {
                    'data': data,
                    'is_worker': True
                }
            except workers.DoesNotExist:
                # If neither found, return error
                return HttpResponse("Profile not found. Please contact administrator.")
        
        return render(request, 'userpages/user_profile.html', context)
    
class workerprofile(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request):
        user=request.user.id
        data=workers.objects.get(admin=user)
        context={
            'data':data,
        }
        return render(request,'workerpages/worker_profile.html',context)

class EditWorkerProfile(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    
    def get(self, request):
        user = request.user.id
        data = workers.objects.get(admin=user)
        context = {
            'data': data,
        }
        return render(request, 'workerpages/edit_worker_profile.html', context)
    
    def post(self, request):
        try:
            user = request.user
            worker = workers.objects.get(admin=user)
            
            # Update User model fields
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.username = request.POST.get('email')  # Update username to match email
            user.save()
            
            # Update worker model fields
            worker.contact_number = request.POST.get('contact_number')
            worker.gender = request.POST.get('gender')
            worker.Address = request.POST.get('address')
            worker.city = request.POST.get('city')
            
            # Handle profile picture update
            if 'profile_pic' in request.FILES:
                worker.profile_pic = request.FILES['profile_pic']
            
            worker.save()
            
            messages.success(request, 'Profile updated successfully!')
            return HttpResponseRedirect('/workerprofile')
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
            return HttpResponseRedirect('/edit_worker_profile')

class markcompleted(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self, request, action, id):
        try:
            if action == 'completed':
                Response.objects.filter(id=id, status=False).update(status=True)
                print("Response status updated successfully.")
            else:
                print("Action not 'completed' or status is already True.")

            return HttpResponseRedirect('/WorkerpendingTask')
        except Response.DoesNotExist:
            print(f"Response with id {id} does not exist.")
            return HttpResponse(status=404)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return HttpResponse(status=500)

class reject(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self,request,action,id):
        response_record = Response.objects.get(id=id)
        request_record = response_record.requests
        r_id=request_record.id
        ServiceRequests.objects.filter(id=r_id).update(status=False)
    
        response_record.delete()
        return HttpResponseRedirect('/WorkerpendingTask')

class DeleteWorker(LoginRequiredMixin, View):
    login_url = common_lib.DEFAULT_REDIRECT_PATH['ROOT']
    def get(self, request, id):
        worker = workers.objects.get(id=id)
        worker.delete()
        return redirect('manageworker')

@login_required
def update_service_tracking(request):
    """IEEE 802.11/802.15.4 compliant service tracking update endpoint"""
    if request.method == 'POST':
        try:
            response_id = request.POST.get('response_id')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            status_update = request.POST.get('status_update')
            battery_level = request.POST.get('battery_level')
            rssi = request.POST.get('rssi')  # IEEE 802.11 signal strength

            # Validate worker authorization
            response = Response.objects.get(id=response_id)
            if response.assigned_worker.admin != request.user:
                return JsonResponse({
                    'error': True,
                    'message': 'Unauthorized access'
                })

            # Create tracking update
            tracking = ServiceTracking.objects.create(
                response=response,
                latitude=latitude,
                longitude=longitude,
                status_update=status_update,
                battery_level=battery_level
            )

            # Update signal strength if provided
            if rssi:
                tracking.update_signal_strength(int(rssi))

            # Calculate and update ETA
            tracking.calculate_eta()

            return JsonResponse({
                'error': False,
                'message': 'Tracking updated successfully'
            })

        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': f'Error updating tracking: {str(e)}'
            })

    return JsonResponse({
        'error': True,
        'message': 'Invalid request method'
    })

class AddProductView(View):
    def get(self, request, category):
        form = ProductForm(initial={'category': category})
        return render(request, 'adminpages/add_product.html', {'form': form, 'category': category})

    def post(self, request, category):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.category = category
            product.save()
            return render(request, 'adminpages/add_product.html', {'form': ProductForm(initial={'category': category}), 'category': category, 'success': True})
        return render(request, 'adminpages/add_product.html', {'form': form, 'category': category})

class ProductListView(View):
    def get(self, request, category=None):
        if category:
            shops = Shop.objects.filter(category=category).prefetch_related('products')
            context = {'shops': shops, 'category': category}
        else:
            # Handle case where no category is specified, maybe list all shops
            shops = Shop.objects.all().prefetch_related('products')
            context = {'shops': shops, 'category': None}
        return render(request, 'adminpages/product_list.html', context)

class ProductEditView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, 'adminpages/edit_product.html', {'form': form, 'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'adminpages/edit_product.html', {'form': form, 'product': product})

class ProductDeleteView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'adminpages/delete_product.html', {'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('product_list')

class SalesCategoryView(View):
    def get(self, request, category):
        # Validate category
        valid_categories = ['grocery', 'electricals', 'plumbing']
        if category not in valid_categories:
            return HttpResponse('Invalid category', status=404)
        
        shops = Shop.objects.filter(category=category)
        return render(request, 'adminpages/sales_category.html', {'category': category, 'shops': shops})

class ShopView(View):
    def get(self, request):
        # Get all shops grouped by category
        grocery_shops = Shop.objects.filter(category='grocery')
        electricals_shops = Shop.objects.filter(category='electricals')
        plumbing_shops = Shop.objects.filter(category='plumbing')
        
        context = {
            'grocery_shops': grocery_shops,
            'electricals_shops': electricals_shops,
            'plumbing_shops': plumbing_shops,
        }
        return render(request, 'userpages/shop.html', context)

class ShopProductsView(View):
    def get(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        query = request.GET.get('q', '')
        products = Product.objects.filter(shop=shop)
        
        if query:
            products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
        
        context = {
            'shop': shop,
            'products': products,
            'query': query
        }
        return render(request, 'userpages/shop_products.html', context)

class AddShopView(View):
    def get(self, request, category):
        return render(request, 'adminpages/add_shop.html', {'category': category})

    def post(self, request, category):
        name = request.POST.get('name')
        owner_name = request.POST.get('owner_name')
        owner_phone_number = request.POST.get('owner_phone_number')
        image = request.FILES.get('image')
        
        error = None
        if not all([name, owner_name, owner_phone_number, image]):
            error = 'All fields are required.'
        elif Shop.objects.filter(owner_phone_number=owner_phone_number).exists():
            error = 'This phone number is already registered to another shop.'
        
        if not error:
            Shop.objects.create(
                name=name, 
                category=category, 
                image=image,
                owner_name=owner_name,
                owner_phone_number=owner_phone_number
            )
            return redirect(reverse('sales_category', args=[category]))
        
        return render(request, 'adminpages/add_shop.html', {
            'category': category, 
            'error': error
        })

class EditShopView(View):
    def get(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        return render(request, 'adminpages/edit_shop.html', {'shop': shop})

    def post(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        name = request.POST.get('name')
        owner_name = request.POST.get('owner_name')
        owner_phone_number = request.POST.get('owner_phone_number')
        image = request.FILES.get('image')
        
        error = None
        if not all([name, owner_name, owner_phone_number]):
            error = 'All fields are required.'
        elif Shop.objects.filter(owner_phone_number=owner_phone_number).exclude(pk=shop_id).exists():
            error = 'This phone number is already registered to another shop.'
        
        if not error:
            shop.name = name
            shop.owner_name = owner_name
            shop.owner_phone_number = owner_phone_number
            if image:
                shop.image = image
            shop.save()
            return redirect(reverse('sales_category', args=[shop.category]))
        
        return render(request, 'adminpages/edit_shop.html', {
            'shop': shop, 
            'error': error
        })

class AddProductToShopView(View):
    def get(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        form = ProductForm(initial={'category': shop.category})
        return render(request, 'adminpages/add_product.html', {'form': form, 'shop': shop})

    def post(self, request, shop_id):
        shop = get_object_or_404(Shop, pk=shop_id)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop = shop
            product.category = shop.category
            product.save()
            return redirect(f'/sales/{shop.category}/manage/')
        
        return render(request, 'adminpages/add_product.html', {'form': form, 'shop': shop})

class ManageShopsView(View):
    def get(self, request):
        shops = Shop.objects.all()
        return render(request, 'adminpages/manage_shops.html', {'shops': shops})

@method_decorator([csrf_protect, ensure_csrf_cookie], name='dispatch')
class AdminRegistration(View):
    def get(self, request):
        form = AdminRegistrationForm()
        return render(request, 'admin_registration.html', {'form': form})
    
    def post(self, request):
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            # Get the password from the form
            password = form.cleaned_data.get('password')
            
            # Save the registration request with hashed password
            registration_request = form.save(commit=False)
            registration_request.password = make_password(password)  # Hash the password
            registration_request.save()
            
            # Send email notification to super admin
            email_subject = f'New Admin Registration Request: {registration_request.first_name} {registration_request.last_name}'
            email_message = f"""
            A new admin registration request has been submitted:
            
            Name: {registration_request.first_name} {registration_request.last_name}
            Username: {registration_request.username}
            Email: {registration_request.email}
            Phone: {registration_request.phone_number}
            Address: {registration_request.address}
            
            To approve or reject this request, please visit the admin panel.
            """
            
            # Send email to super admin
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Super admin email
                fail_silently=False,
            )
            
            # Send confirmation email to applicant
            confirmation_subject = 'Admin Registration Request Received'
            confirmation_message = f"""
            Dear {registration_request.first_name} {registration_request.last_name},
            
            Thank you for submitting your admin registration request. We have received your application and will review it shortly.
            
            Your request details:
            Username: {registration_request.username}
            Email: {registration_request.email}
            
            You will receive an email notification once your request has been reviewed.
            
            Best regards,
            Home Services Team
            """
            
            send_mail(
                confirmation_subject,
                confirmation_message,
                settings.EMAIL_HOST_USER,
                [registration_request.email],
                fail_silently=False,
            )
            
            messages.success(request, 'Your admin registration request has been submitted successfully. You will be notified once it is reviewed.')
            return redirect('choose_login')
        else:
            return render(request, 'admin_registration.html', {'form': form})

@method_decorator([csrf_protect, ensure_csrf_cookie], name='dispatch')
class SuperAdminLogin(View):
    def get(self, request):
        return render(request, 'super_admin_login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return render(request, 'super_admin_login.html', {
                'error_msg': "Please provide both username and password."
            })
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return HttpResponseRedirect('/super_admin_dashboard')
        else:
            return render(request, 'super_admin_login.html', {
                'error_msg': "Invalid super admin credentials."
            })

@method_decorator([csrf_protect, ensure_csrf_cookie], name='dispatch')
class AdminLogin(View):
    def get(self, request):
        return render(request, 'admin_login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            return render(request, 'admin_login.html', {
                'error_msg': "Please provide both username and password."
            })
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff and not user.is_superuser:
            login(request, user)
            return HttpResponseRedirect('/admmin_home')
        else:
            return render(request, 'admin_login.html', {
                'error_msg': "Invalid admin credentials or insufficient permissions."
            })

class SuperAdminDashboard(LoginRequiredMixin, View):
    login_url = '/super-admin-login/'
    
    def get(self, request):
        if not request.user.is_superuser:
            return HttpResponseRedirect('/super-admin-login/')
        
        # Admin registration request statistics
        pending_requests = AdminRegistrationRequest.objects.filter(status='pending')
        approved_requests = AdminRegistrationRequest.objects.filter(status='approved')
        rejected_requests = AdminRegistrationRequest.objects.filter(status='rejected')
        
        # System statistics (same as admin dashboard)
        total_requests = ServiceRequests.objects.count()
        completed_requests = Response.objects.filter(status=True).count()
        pending_requests_count = Response.objects.filter(status=False).count()
        total_users = users.objects.count()
        
        context = {
            'pending_requests': pending_requests,
            'approved_requests': approved_requests,
            'rejected_requests': rejected_requests,
            'total_pending': pending_requests.count(),
            'total_approved': approved_requests.count(),
            'total_rejected': rejected_requests.count(),
            'total_requests': total_requests,
            'completed_requests': completed_requests,
            'pending_requests_count': pending_requests_count,
            'total_users': total_users,
        }
        return render(request, 'super_admin_dashboard.html', context)

class AdminRequestAction(LoginRequiredMixin, View):
    login_url = '/super-admin-login/'
    
    def get(self, request, request_id, action):
        if not request.user.is_superuser:
            return HttpResponseRedirect('/super-admin-login/')
        
        registration_request = get_object_or_404(AdminRegistrationRequest, id=request_id)
        
        if action == 'approve':
            registration_request.status = 'approved'
            registration_request.save()
            
            # Create the admin user with the stored password
            user = User.objects.create_user(
                username=registration_request.username,
                email=registration_request.email,
                password=registration_request.password,  # Use the stored hashed password
                first_name=registration_request.first_name,
                last_name=registration_request.last_name,
                is_staff=True,
                is_superuser=False
            )
            
            # Send approval email
            approval_subject = 'Admin Registration Approved'
            approval_message = f"""
            Dear {registration_request.first_name} {registration_request.last_name},
            
            Congratulations! Your admin registration request has been approved.
            
            Your login credentials:
            Username: {registration_request.username}
            Password: (Use the password you provided during registration)
            
            You can now login to the admin panel using your credentials.
            
            Best regards,
            Home Services Team
            """
            
            send_mail(
                approval_subject,
                approval_message,
                settings.EMAIL_HOST_USER,
                [registration_request.email],
                fail_silently=False,
            )
            
            messages.success(request, f'Admin registration for {registration_request.first_name} {registration_request.last_name} has been approved.')
            
        elif action == 'reject':
            registration_request.status = 'rejected'
            registration_request.save()
            
            # Send rejection email
            rejection_subject = 'Admin Registration Request Status'
            rejection_message = f"""
            Dear {registration_request.first_name} {registration_request.last_name},
            
            We regret to inform you that your admin registration request has not been approved at this time.
            
            If you have any questions, please contact us.
            
            Best regards,
            Home Services Team
            """
            
            send_mail(
                rejection_subject,
                rejection_message,
                settings.EMAIL_HOST_USER,
                [registration_request.email],
                fail_silently=False,
            )
            
            messages.warning(request, f'Admin registration for {registration_request.first_name} {registration_request.last_name} has been rejected.')
        
        return HttpResponseRedirect('/super_admin_dashboard')

class AdminEditView(LoginRequiredMixin, View):
    login_url = '/super-admin-login/'
    
    def get(self, request, request_id):
        if not request.user.is_superuser:
            return HttpResponseRedirect('/super-admin-login/')
        
        registration_request = get_object_or_404(AdminRegistrationRequest, id=request_id)
        form = AdminEditForm(instance=registration_request)
        
        context = {
            'form': form,
            'registration_request': registration_request,
        }
        return render(request, 'admin_edit.html', context)
    
    def post(self, request, request_id):
        if not request.user.is_superuser:
            return HttpResponseRedirect('/super-admin-login/')
        
        registration_request = get_object_or_404(AdminRegistrationRequest, id=request_id)
        form = AdminEditForm(request.POST, instance=registration_request)
        
        if form.is_valid():
            # Update the registration request
            registration_request = form.save()
            
            # Handle password change if provided
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                registration_request.password = make_password(new_password)
                registration_request.save()
                
                # Update the corresponding User object if it exists
                try:
                    user = User.objects.get(username=registration_request.username)
                    user.set_password(new_password)
                    user.save()
                except User.DoesNotExist:
                    pass  # User might not exist yet if not approved
            
            messages.success(request, f'Admin details for {registration_request.first_name} {registration_request.last_name} have been updated successfully.')
            return HttpResponseRedirect('/super_admin_dashboard')
        else:
            context = {
                'form': form,
                'registration_request': registration_request,
            }
            return render(request, 'admin_edit.html', context)

        