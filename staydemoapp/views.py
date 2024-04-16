from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse

from staydemo import settings
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth
from .models import Guest
from .models import Host,Guide,Review
from .forms import HostProfileForm, GuestProfileForm

from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .models import Property, PropertyType
from .forms import PropertyForm,PropertyImageForm
from django.forms import modelformset_factory
from django.http import Http404
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from staydemoapp.models import Property, PropertyImage,Booking
from datetime import datetime

# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Payment
from .models import Availability
from .forms import AvailabilityForm

from .models import WishlistItem
from django.http import JsonResponse

from django.views.decorators.cache import cache_control
from django.contrib.auth import logout
# from django.contrib import auth
#################################################
# from .models import Property, Booking , GuestBookingAvailability

from . import candy
def index(request):
    return candy.render(request, "index.html")


def registration(request):
    if request.method == "POST":
        guest_first_name = request.POST['guest_first_name']
        guest_last_name = request.POST['guest_last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if CustomUser.objects.filter(username=username).exists():
            messages.info(request, "Username already exists")
            return redirect('registration')
        elif CustomUser.objects.filter(email=email).exists():
            messages.info(request, "Email already exists")
            return redirect('registration')
        elif password != confirm_password:
            messages.error(request, "Password and confirmation password do not match")
            return redirect('registration')
        else:
            user = Guest.objects.create_user(
                guest_first_name=guest_first_name,
                guest_last_name=guest_last_name,
                email=email,
                username=username,
                password=password,
                is_guest=True,
                phone_number=phone_number
            )
            user.role = CustomUser.GUEST  # Set the role to GUEST
            user.save()
        return redirect('login')
    else:
        return candy.render(request, 'registration.html')


def registerproperty(request):
    if request.method == 'POST':
        host_first_name = request.POST['host_first_name']
        host_last_name = request.POST['host_last_name']
        property_name = request.POST['property_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        license_upload = request.FILES.get('license_upload')

        if Host.objects.filter(username=username).exists():
            messages.error(request, "User already registered")
            return render(request, "login.html")

        else:
            user = Host.objects.create_user(
                host_first_name=host_first_name,
                host_last_name=host_last_name,
                email=email,
                username=username,
                password=password,
                property_name=property_name,
            )
            
            user.role = CustomUser.HOST  # Set the role to HOST
            user.set_password(password)
            if license_upload:
                user.license_upload = license_upload
            user.save()

            messages.success(request, "Registration successful. You can now login.")
            return redirect("login")

    return candy.render(request, "registerproperty.html")


from .forms import GuideRegistrationForm

def guide_registration(request):
    if request.method == 'POST':
        form = GuideRegistrationForm(request.POST, request.FILES)


        if form.is_valid():
            guide = form.save(commit=False)
            guide.role = CustomUser.GUIDE  # Set the role to GUIDE
            guide.is_guide = True
            guide.set_password(form.cleaned_data['password'])  # Set the password
            guide.profilePicture = form.cleaned_data['profilePicture']
            guide.save()

            return redirect('login')  # Redirect to login after successful registration
        else:
            # Form is not valid, handle errors or display messages
            messages.error(request, "There are errors in the form. Please check.")
    else:
        form = GuideRegistrationForm()

    return candy.render(request, 'guide_registration.html', {'form': form})

    
from django.contrib.auth import authenticate, login as auth_login

    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username:", username)
        print("Password:", password)
        user = authenticate(request, username=username, password=password, backend='django.contrib.auth.backends.ModelBackend')

        print("User:", user)

        if user is not None:
            if user.role == CustomUser.GUEST:
                if hasattr(user, 'guest') and user.guest.is_guest:
                    # Redirect to the guest dashboard
                    auth_login(request, user)
                    request.session['username'] = username
                    return redirect('guest_dashboard')
                else:
                    messages.error(request, "Invalid role")
            elif user.role == CustomUser.HOST:
                if hasattr(user, 'host') and user.host.is_host:
                    # Check if the host is approved
                    if user.host.approved:
                        # Redirect to the host dashboard
                        auth_login(request, user)
                        request.session['username'] = username
                        return redirect('host_dashboard')
                    else:
                        # Host not approved yet
                        messages.error(request, "Your host account has not been approved yet.")
                else:
                    messages.error(request, "Invalid role")
            elif user.role == CustomUser.GUIDE:
                if hasattr(user, 'guide') and user.guide.is_guide:
                    # Redirect to the guide dashboard
                    auth_login(request, user)
                    request.session['username'] = username
                    return redirect('guide_dashboard')  # Adjust the URL for the guide dashboard
                else:
                    messages.error(request, "Invalid role")
            elif user.role == CustomUser.ADMIN:
                auth_login(request, user)
                request.session['username'] = username
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid role")
        else:
            # Display the "Invalid login credentials" message when authentication fails
            messages.error(request, "Invalid login credentials")

    response = render(request, 'login.html')
    response['Cache-Control'] = 'no-store, must-revalidate'
    return response

#----------------------------
    #         messages.error(request, "Invalid username or password")
    # return render(request, "login.html")

#def host_dashboard(request):
  #  if 'username' in request.session:
  #     response = render(request, 'host_dashboard.html')
  #     response['Cache-Control'] = 'no-store, must-revalidate'
  #     return response
  ##  else:
    #   return redirect('/')
    #return render(request,'host_dashboard.html')

@login_required
def guide_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'guide') and request.user.guide.is_guide and request.user.guide.approved:
        guide = request.user.guide

        # Fetch the required information
        services_added = AddService.objects.filter(guide=guide).count()
        total_bookings = ServiceBooking.objects.filter(service__guide=guide).count()
        # total_payments = Payment.objects.filter(booking__service__guide=guide).count()

        return render(request, 'guide_dashboard.html', {
            'services_added': services_added,
             'total_bookings': total_bookings,
            # 'total_payments': total_payments,
        })
    else:
        return redirect('/')


@login_required
def host_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'host') and request.user.host.is_host:
        host = request.user.host
        properties = Property.objects.filter(host=host)
        
        # If you have a specific property, you can pass it here
        property = properties.first()  # For example, taking the first property in the list
        
        return render(request, 'host_dashboard.html', {'property': property, 'properties': properties})
    else:
        return redirect('/')

# def guest_dashboard(request):
#     if 'username' in request.session:
#         # Fetch properties along with their associated images
#         properties = Property.objects.all()
#         property_images = PropertyImage.objects.all()
#         return render(request, 'guest_dashboard.html', {'properties': properties, 'property_images': property_images})
#     else:
#         return redirect('/')
@login_required
def guest_dashboard(request):
    if 'username' in request.session:
        # Fetch properties along with their associated images
        properties = Property.objects.all()
        property_images = PropertyImage.objects.all()
        
        # Fetch all property types
        property_types = PropertyType.objects.all()

        # Get the selected property type from the query parameters
        selected_property_type = request.GET.get('property_type')

        # Filter properties based on the selected property type
        if selected_property_type:
            properties = properties.filter(property_type__name=selected_property_type)

        # Additional filters
        price_range = request.GET.get('price_range')
        num_bedrooms = request.GET.get('num_bedrooms')
        num_bathrooms = request.GET.get('num_bathrooms')
        capacity = request.GET.get('capacity')

        print("Price Range:", price_range)
         # Apply additional filters if provided
        if price_range:
        # Split the price_range into min and max values if the format is correct
            price_range_values = price_range.split('-')
            print("Price Range Values:", price_range_values)
            if len(price_range_values) == 2:
                min_price, max_price = map(int, price_range_values)
                print("Min Price:", min_price)
                print("Max Price:", max_price)
            # Add logic to filter properties based on the price range
                properties = properties.filter(price__range=(min_price, max_price))
        if num_bedrooms:
            properties = properties.filter(number_of_bedrooms=num_bedrooms)

        if num_bathrooms:
            properties = properties.filter(number_of_bathrooms=num_bathrooms)

        if capacity:
            properties = properties.filter(capacity=capacity)
        

        context = {
            'properties': properties,
            'property_images': property_images,
            'property_types': property_types,
            'selected_property_type': selected_property_type,
        }

        return render(request, 'guest_dashboard.html', context)
    else:
        return redirect('/')
    # return render(request,'guest_dashboard.html')


    # return render(request,'guest_dashboard.html')

def logout(request):
    auth(request)
    return redirect('/')



# def services(request):
#     return render(request, 'inc/services.html')

def admin_dashboard(request):
    if 'username' in request.session:
        # Calculate the number of guests, hosts, and pending approvals
        number_of_guests = Guest.objects.count()
        number_of_hosts = Host.objects.count()
        number_of_pending_approvals = Host.objects.filter(approved=False).count()
        number_of_pending_guide_approvals = Guide.objects.filter(approved=False).count()

        return render(request, 'admin_dashboard.html', {
            'number_of_guests': number_of_guests,
            'number_of_hosts': number_of_hosts,
            'number_of_pending_approvals': number_of_pending_approvals,
            'number_of_pending_guide_approvals': number_of_pending_guide_approvals,
        })
    else:
        return redirect('/')
#guide approval
@login_required
def manage_guide_approvals(request):
    if request.method == 'POST':
        guide_id = request.POST.get('guide_id')
        action = request.POST.get('action')

        try:
            guide = Guide.objects.get(id=guide_id)
            if action == 'approve':
                guide.approved = True
                guide.is_guide = True  # Set the is_guide attribute upon approval
                guide.save()
                messages.success(request, f"{guide.guide_first_name} {guide.guide_last_name} has been approved.")
            elif action == 'reject':
                guide.approved = False
                guide.save()
                messages.success(request, f"{guide.guide_first_name} {guide.guide_last_name} has been rejected.")

        except Guide.DoesNotExist:
            messages.error(request, "Guide not found.")

    # Fetch unapproved guides for display
    unapproved_guides = Guide.objects.filter(approved=False)

    return render(request, 'manage_guide_approvals.html', {'unapproved_guides': unapproved_guides})

# Add a new view to manage host approvals
@login_required
@user_passes_test(lambda u: u.role == CustomUser.ADMIN)
def manage_host_approvals(request):
    if request.method == 'GET':
        # Fetch all unapproved hosts
        unapproved_hosts = Host.objects.filter(approved=False)
        context = {'unapproved_hosts': unapproved_hosts}
        return render(request, 'manage_host_approvals.html', context)

    if request.method == 'POST':
        host_id = request.POST.get('host_id')
        action = request.POST.get('action')

        # Approve or reject the host based on the action
        host = get_object_or_404(Host, id=host_id)
        if action == 'approve':
            host.approved = True
            host.save()
        elif action == 'reject':
            host.delete()
        return redirect('manage_host_approvals')
    return HttpResponse(status=405)

def view_hosts(request):
    hosts = Host.objects.all()
    return render(request, 'view_hosts.html', {'hosts': hosts})

def view_guests(request):
    guests = Guest.objects.all()
    return render(request, 'view_guests.html', {'guests': guests})


def view_guides(request):
    guides = Guide.objects.all()
    return render(request, 'view_guides.html', {'guides': guides})

def delete_guest(request, guest_id):
    try:
        guest = Guest.objects.get(id=guest_id)
        guest.delete()
        messages.error(request, 'Guest does not exist')
    except Guest.DoesNotExist:
        pass
    return redirect('view_guests')
def delete_host(request, host_id):
    try:
        host = Host.objects.get(id=host_id)
        host.delete()
        messages.error(request, 'Host Deleted Successfully')
    except Host.DoesNotExist:    
        pass
    return redirect('view_hosts')

def delete_guide(request, guide_id):
    try:
        guide = Guide.objects.get(id=guide_id)
        guide.delete()
        messages.success(request, 'Guide Deleted Successfully')  # Use 'success' instead of 'error'
    except Guide.DoesNotExist:    
        pass
    return redirect('view_guides')


def edit_host_profile(request):
    host = request.user.host  # Retrieve the host object of the logged-in user

    if request.method == 'POST':
        form = HostProfileForm(request.POST, instance=host)
        if form.is_valid():
            form.save()
            return redirect('host_profile')  # Redirect to the host profile after a successful update
    else:
        form = HostProfileForm(instance=host)

    context = {'form': form}
    return render(request, 'edit_host_profile.html', context)

@login_required
def edit_guest_profile(request):
    guest = request.user.guest

    if request.method == 'POST':
        form = GuestProfileForm(request.POST, instance=guest)
        if form.is_valid():
            form.save()
            return redirect('guest_profile')  # Redirect to the profile page
    else:
        form = GuestProfileForm(instance=guest)

    return render(request, 'edit_guest_profile.html', {'form': form})

def host_profile(request):
    host = request.user.host  # Retrieve the host object of the logged-in user
    context = {'host': host}
    return render(request, 'host_profile.html', context)
@login_required

def guest_profile(request):
    guest = request.user.guest
    return render(request, 'guest_profile.html', {'guest': guest})
        
# view and edit -guide profile
from .forms import GuideEditForm


@login_required
def view_guide_profile(request):
    guide = request.user.guide
    return render(request, 'view_guide_profile.html', {'guide': guide})

@login_required
def edit_guide_profile(request):
    guide = request.user.guide

    if request.method == 'POST':
        form = GuideEditForm(request.POST, request.FILES, instance=guide)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('view_guide_profile')
        else:
            print(form.errors)
            messages.error(request, "There are errors in the form. Please check.")
    else:
        # Initialize the form with the guide's data
        form = GuideEditForm(instance=guide)

    return render(request, 'edit_guide_profile.html', {'form': form})
# def edit_guide_profile(request):
#     guide = request.user.guide  # Retrieve the host object of the logged-in user

#     if request.method == 'POST':
#         form = GuideEditForm(request.POST, instance=guide)
#         if form.is_valid():
#             form.save()
#             return redirect('view_guide_profile')  # Redirect to the host profile after a successful update
#     else:
#         form = GuideEditForm(instance=guide)

#     context = {'form': form}
#     return render(request, 'edit_guide_profile.html', context)
# @login_required
# def add_property(request):
#     ImageFormSet = modelformset_factory(PropertyImage, form=PropertyImageForm, extra=5, max_num=6)

#     if request.method == 'POST':
#         form = PropertyForm(request.POST)
#         image_formset = ImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

#         if form.is_valid() and image_formset.is_valid():
#             property = form.save(commit=False)
#             property.host = request.user.host
#             property.save()

#             for idx, image_form in enumerate(image_formset):
#                 if image_form.cleaned_data:
#                     image = image_form.save(commit=False)
#                     image.property = property
#                     image.save()

#                     # Set the first uploaded image as the cover photo
#                     if idx == 0:
#                         property.cover_photo = image
#                         property.save()

#             return redirect('view_property', property_id=property.property_id)
#     else:
#         host = request.user.host
#         initial_data = {'property_name': host.property_name}
#         form = PropertyForm(initial=initial_data)
#         image_formset = ImageFormSet(queryset=PropertyImage.objects.none())

#     return render(request, 'add_property.html', {'form': form, 'image_formset': image_formset})


from django.urls import reverse  # Import the reverse function to generate URLs


from .models import Guide


from django.shortcuts import render, redirect
from .models import AddService
from .forms import AddServiceForm
@login_required
def add_service(request):
    if request.method == 'POST':
        form = AddServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service_instance = form.save(commit=False)
            service_instance.guide = request.user.guide
            service_instance.save()
            return redirect('view_services')
    else:
        form = AddServiceForm()

    return render(request, 'add_service.html', {'form': form})

@login_required
def view_services(request):
    services = AddService.objects.filter(guide=request.user.guide)
    return render(request, 'view_services.html', {'services': services})

@login_required
def service_details(request,service_id): 
    service = get_object_or_404(AddService, service_id=service_id)
    return render(request, "service_details.html", {'service': service})

@login_required
def delete_service(request):
    if request.method == 'GET':
        service_id = request.GET.get('service_id')
        service = get_object_or_404(AddService, service_id=service_id)
        service.delete()
    return redirect('view_services')

from .forms import AddServiceForm
@login_required
def edit_service_details(request, service_id):
    service = get_object_or_404(AddService, service_id=service_id)
    if request.method == 'POST':
        form = AddServiceForm(request.POST, request.FILES,instance=service)
        if form.is_valid():
            form.save()
            return redirect('view_services')
    else:
        form = AddServiceForm(instance=service)
    return render(request, 'edit_service_details.html', {'form': form, 'service': service})

@login_required
def guide_display(request):
    query = request.GET.get('q')
    guides = Guide.objects.filter(approved=True)
    
    if query:
        guides = guides.filter(Q(guide_first_name__icontains=query) | Q(guide_last_name__icontains=query) | Q(location__icontains=query))
    
    return render(request, 'guide_display.html', {'guides': guides})

@login_required
def guest_service_display(request, guide_id):
    guide = get_object_or_404(Guide, id=guide_id)
    services = AddService.objects.filter(guide=guide)
    context = {
        'guide': guide,
        'services': services,
    }
    return render(request, 'guest_service_display.html', context)
from django.db.models import Avg
def guest_service_view(request, service_id):
    service = get_object_or_404(AddService, service_id=service_id)
    # Calculate the average rating for the current service
    average_rating = Review.objects.filter(service=service).aggregate(Avg('rating'))['rating__avg']
    
    return render(request, 'guest_service_view.html', {'service': service, 'average_rating': average_rating})

from decimal import Decimal

from .models import AddService,ServiceBooking
from django.http import HttpResponse  
from django.urls import reverse
from .forms import ServiceBookingForm
from .models import Review
def service_booking(request, service_id):
    service = AddService.objects.get(service_id=service_id)
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid(): 
            booking = form.save(commit=False)
            booking.service = service
            booking.guest = request.user.guest
            booking.save()
            
            # Create a new ServicePayment object
            payment = ServicePayment.objects.create(
                booking=booking,
                amount_paid=booking.total_price,  # Assuming total_price is the amount to be paid
                status='completed'  # Assuming the payment is completed upon booking
            )
            
            return redirect('booking_status', booking_id=booking.booking_id)
        else:
            print(form.errors)
    else:
        form = ServiceBookingForm()

    return render(request, 'service_booking.html', {'service': service, 'form': form})

from django.shortcuts import get_object_or_404, render
from .models import ServiceBooking

def booking_status(request, booking_id):
    booking = get_object_or_404(ServiceBooking, booking_id=booking_id)
    amount_in_paise = booking.service.price_per_person * 100
    return render(request, 'booking_status.html', {'booking': booking, 'amount_in_paise': amount_in_paise})


def payment_success(request, booking_id):
    booking = ServiceBooking.objects.get(booking_id=booking_id)  # Filter by booking_id
    return render(request, 'payment_success.html', {'booking': booking})
def view_servicebookings(request):
    bookings = ServiceBooking.objects.filter(guest=request.user.guest)
    return render(request, 'view_servicebooking.html', {'bookings': bookings})

def guide_service_booking(request):
    # Fetch all bookings for the logged-in guide
    guide_bookings = ServiceBooking.objects.filter(service__guide=request.user.guide)

    context = {
        'guide_bookings': guide_bookings,
    }

    return render(request, 'guide_service_booking.html', context)
from .models import ServicePayment

from .forms import ReviewForm
def get_user_reviews(request):
    if request.method == 'GET':
        service_id = request.GET.get('service_id')
        user_reviews = Review.objects.filter(guest=request.user.guest, service_id=service_id)
        reviews_data = []
        for review in user_reviews:
            review_data = {
                'rating': review.rating,
                'comment': review.reviewcomment
            }
            reviews_data.append(review_data)
        return JsonResponse(reviews_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
def viewmyservices(request):
    user_payments = ServicePayment.objects.filter(booking__guest=request.user.guest)
    form = ReviewForm()
    return render(request, 'viewmyservices.html', {'form': form, 'user_payments': user_payments})

def add_review(request, service_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = get_object_or_404(AddService, id=service_id)  # Retrieve the service object
            review.guest = request.user.guest
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('viewmyservices')
        else:
            messages.error(request, 'Failed to add review. Please check your inputs.')
            print(form.errors)  # Print form errors for debugging
    else:
        messages.error(request, 'Invalid request method.')

    return redirect('viewmyservices')


#add new prop
@login_required
def add_property(request):
    ImageFormSet = modelformset_factory(PropertyImage, form=PropertyImageForm, extra=5, max_num=6)

    if request.method == 'POST':
        form = PropertyForm(request.POST)
        image_formset = ImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.none())

        if form.is_valid() and image_formset.is_valid():
            property = form.save(commit=False)
            property.host = request.user.host
             # Extract latitude and longitude from the form or other sources
            latitude = request.POST.get('latitude')  # Change this based on your actual form structure
            longitude = request.POST.get('longitude')

            property.latitude = latitude
            property.longitude = longitude
            property.save()

            for idx, image_form in enumerate(image_formset):
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.property = property
                    image.save()

                    # Set the first uploaded image as the cover photo
                    if idx == 0:
                        property.cover_photo = image
                        property.save()

            return redirect('view_property', property_id=property.property_id)  # Redirect to view_property

    else:
        host = request.user.host
        initial_data = {'property_name': host.property_name}
        form = PropertyForm(initial=initial_data)
        image_formset = ImageFormSet(queryset=PropertyImage.objects.none())

    return render(request, 'add_property.html', {'form': form, 'image_formset': image_formset})

def view_property(request, property_id):
    property = get_object_or_404(Property, property_id=property_id)
    images = property.propertyimage_set.all()  # Retrieve all related images for the property
    return render(request, 'view_property.html', {'property': property, 'images': images})

def edit_property(request, property_id):
    property = get_object_or_404(Property, property_id=property_id)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        image_form = PropertyImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
        # Check if an image was provided before attempting to save it
        if 'image' in request.FILES:
            if image_form.is_valid():
                image = image_form.save(commit=False)
                image.property = property
                image.save()

        return redirect('view_property', property_id=property.property_id)
    else:
        form = PropertyForm(instance=property)
        image_form = PropertyImageForm()

    return render(request, 'edit_property.html', {'form': form, 'image_form': image_form, 'property': property})


@login_required
def add_availability(request, property_id):
    property = get_object_or_404(Property, pk=property_id, host=request.user)

    # Get the host properties
    host_properties = Property.objects.filter(host=request.user)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST, host=request.user, host_properties=host_properties)  # Pass the host and host_properties to the form
        if form.is_valid():
            form.instance.property = property
            form.save()
            return redirect('add_availability', property_id=property_id)
    else:
        form = AvailabilityForm(host=request.user, host_properties=host_properties, initial={'property': property})

    availabilities = Availability.objects.filter(property=property)
    return render(request, 'add_availability.html', {
        'property': property,
        'form': form,
        'availabilities': availabilities,
    })




def guest_property_details(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    images = PropertyImage.objects.filter(property=property)
    
    # Initialize host information with default values
    host_first_name = "No Host Information Available"
    host_last_name = ""

    if property.host and property.host.is_host:
        host_first_name = property.host.host_first_name
        host_last_name = property.host.host_last_name

    context = {
        'property': property,
        'images': images,
        'host_first_name': host_first_name,
        'host_last_name': host_last_name,
    }
    return render(request, 'guest_property_details.html', context)

def search_properties(request):
    name = request.GET.get('name')
    location = request.GET.get('location')
    properties = Property.objects.filter(property_name__icontains=name, location__icontains=location)

    if not properties:
        no_results_message = "No results matching your search."
        return render(request, 'search_results.html', {'no_results_message': no_results_message})

    return render(request, 'search_results.html', {'properties': properties})


def add_to_wishlist(request, property_id):
    if request.user.is_authenticated:
        property = get_object_or_404(Property, property_id=property_id)
        user = request.user

        # Check if the property is not already in the user's wishlist
        if not WishlistItem.objects.filter(user=user, property=property).exists():
            wishlist_item = WishlistItem(user=user, property=property)
            wishlist_item.save()

            # Optionally, you can add a success message here
            # messages.success(request, 'Property added to your wishlist.')

        # You can redirect to the 'view_wishlist' view after adding to the wishlist.
        return redirect('view_wishlist')

    # Handle the case where the user is not authenticated
    # You can add your own logic for this case, such as redirecting to a login page.
    return redirect('login')  # Example: redirect to the login page

def view_wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist_items = WishlistItem.objects.filter(user=user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

from django.http import JsonResponse

def remove_from_wishlist(request, property_id):
    if request.user.is_authenticated:
        user = request.user
        property = get_object_or_404(Property, id=property_id)

        try:
            wishlist_item = WishlistItem.objects.get(user=user, property=property)
            wishlist_item.delete()
            return JsonResponse({'success': True})
        except WishlistItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Property is not in the wishlist'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'User is not authenticated'})



# def booking_page(request, property_id):
#     property = get_object_or_404(Property, pk=property_id)

#     context = {
#         'property': property,
#         'property_id': property_id,  # Add property_id to the context
#     }

#     return render(request, 'booking_page.html', context)
def booking_page(request, property_id):
    property = get_object_or_404(Property, pk=property_id)

    context = {
        'property': property,
        'property_id': property_id,  # Add property_id to the context
    }

    return render(request, 'booking_page.html', context)

# import razorpay
# from django.conf import settings
# from django.http import Http404


# def generate_razorpay_order(booking_id, total_price):
#     try:
#         payment = Payment.objects.get(booking_id=booking_id)
#     except Payment.DoesNotExist:
#         raise Http404("Payment not found for the given booking_id")

#     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#     data = {
#         'amount': int(total_price * 100),  # Amount in paise
#         'currency': 'INR',
#         'payment_capture': 1,
#     }
#     order = client.order.create(data=data)

#     # Update the existing payment record with the razorpay_order_id
#     payment.razorpay_order_id = order['id']
#     payment.save()

#     return order['id']

# def confirm_and_pay(request, property_id):
#     if request.method == 'POST':
#         property = get_object_or_404(Property, pk=property_id)

#         check_in_date_str = request.POST.get('check_in_date')
#         check_out_date_str = request.POST.get('check_out_date')
#         num_guests = int(request.POST.get('num_guests'))

#         # Convert date strings to datetime objects
#         check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
#         check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()

#         # Calculate the number of days
#         num_days = (check_out_date - check_in_date).days

#         # Validate number of guests against property capacity
#         if num_guests > property.capacity:
#             return HttpResponse("Number of guests exceeds property capacity.")

#         # Calculate total price dynamically
#         total_price = property.price * num_days

#         # Print total_price for debugging
#         print("Total Price:", total_price)


#          # Save booking details to the database
#                 # Save booking details to the database
#         booking = Booking.objects.create(
#             property=property,
#             check_in_date=check_in_date,
#             check_out_date=check_out_date,
#             num_guests=num_guests,
#             total_price=total_price
#         )
        
# # Generate Razorpay order
#         razorpay_order_id = generate_razorpay_order(booking.id, total_price * 100)

#         context = {
#         'property': property,
#         'booking': booking,
#         'check_in_date': check_in_date,
#         'check_out_date': check_out_date,
#         'num_guests': num_guests,
#         'total_price': total_price,
#         'razorpay_order_id': razorpay_order_id,
#         }

#         return render(request, 'confirmation_page.html', context)    

# def make_payment(request):
#     # Placeholder logic for payment processing
#     return HttpResponse("Your booking is confirmed!")
#========================================


from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 

def confirm_and_pay(request, property_id):
    # Fetch the Property instance using the provided property_id
    property = get_object_or_404(Property, property_id=property_id)

    if request.method == 'POST':
        check_in_date_str = request.POST.get('check_in_date')
        check_out_date_str = request.POST.get('check_out_date')
        num_guests = int(request.POST.get('num_guests'))

        # Convert date strings to datetime objects
        check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()

        # Calculate the number of days
        num_days = (check_out_date - check_in_date).days

        # Validate number of guests against property capacity
        if num_guests > property.capacity:
            return HttpResponseBadRequest("Number of guests exceeds property capacity.")

        # Calculate total price dynamically
        total_price = property.price * num_days

        # Save booking details to the database
        booking = Booking.objects.create(
            property=property,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            num_guests=num_guests,
            total_price=total_price
        )

        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(
            amount=int(total_price * 100),  # Convert total_price to paise
            currency='INR',
            payment_capture='0'
        ))

        # Order ID of the newly created order
        razorpay_order_id = razorpay_order['id']
        
        callback_url = 'http://127.0.0.1:8000/confirm_and_pay/{}/paymenthandler/'.format(property_id)



        # Pass these details to the frontend
        context = {
            'property': property,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
            'num_guests': num_guests,
            'total_price': total_price,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': settings.RAZOR_KEY_ID,
            'currency': 'INR',
            'callback_url': 'http://127.0.0.1:8000/confirm_and_pay/{}/paymenthandler/'.format(property_id),
            'property_id': property_id,
}
        return render(request, 'confirmation_page.html', context=context)
    return HttpResponseBadRequest("Invalid request method")
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request, property_id):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            total_price = float(request.POST.get('total_price', ''))
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = int(total_price * 100)
 # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    # update payment status to 'completed'
                    payment = Payment.objects.get(razorpay_payment_id=payment_id)
                    payment.status = 'completed'
                    payment.razorpay_order_id = razorpay_order_id
                    payment.razorpay_payment_id = payment_id
                    payment.save()
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymenthandler.html')
                except Exception as e:
                    print(e)
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except Exception as e:
            print(e)
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
@login_required
def booking_updates(request):
    # Retrieve bookings and related information for the logged-in user
    bookings = Booking.objects.filter(user=request.user)
    booking_data = []

    for booking in bookings:
        payment_status = Payment.objects.filter(booking=booking).values_list('status', flat=True).first()

        booking_info = {
            'booking_id': booking.id,  # Use booking.id instead of booking.booking_id
            'property_name': booking.property.property_name,
            'check_in_date': booking.check_in_date,
            'check_out_date': booking.check_out_date,
            'payment_status': payment_status,
        }

        booking_data.append(booking_info)

    context = {
        'booking_data': booking_data,
    }

    return render(request, 'booking_updates.html', context)

from django.http import JsonResponse

# Add this view to handle property activation
@login_required
def activate_property(request, property_id):
    if request.user.is_authenticated and hasattr(request.user, 'host') and request.user.host.is_host:
        host = request.user.host
        try:
            property = Property.objects.get(pk=property_id, host=host)
            property.status = 'Activate'
            property.save()
            return JsonResponse({'status': 'success'})
        except Property.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Property not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Authentication failed'})

# Add this view to handle property deactivation
@login_required
def deactivate_property(request, property_id):
    if request.user.is_authenticated and hasattr(request.user, 'host') and request.user.host.is_host:
        host = request.user.host
        try:
            property = Property.objects.get(pk=property_id, host=host)
            property.status = 'Deactivate'
            property.save()
            return JsonResponse({'status': 'success'})
        except Property.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Property not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Authentication failed'})

# views.py

# from django.shortcuts import render

# def paymentsuccess(request):
#     return render(request, 'paymentsuccess.html')
