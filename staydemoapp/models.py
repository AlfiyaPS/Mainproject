from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GUEST = 1
    HOST = 2
    ADMIN = 3
    GUIDE = 4
    
    ROLE_CHOICE = (
        (GUEST, 'guest'),
        (HOST, 'host'),
        (ADMIN, 'admin'),
        (GUIDE, 'guide'),
    )
    
    username = models.CharField(max_length=100, unique=True, default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, default=GUEST)
    
    # Common fields for both Guest and Host
    property_name = models.CharField(max_length=255, default='')

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

class Guest(CustomUser):
    is_guest = models.BooleanField(default=True)
    is_host = models.BooleanField(default=False)
    
    # Fields specific to guests
    guest_first_name = models.CharField(max_length=30)
    guest_last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.guest_first_name} {self.guest_last_name}"
    
class Host(CustomUser):
    is_guest = models.BooleanField(default=False)
    is_host = models.BooleanField(default=True)
    approved = models.BooleanField(null=True, default=False)
    
    host_first_name = models.CharField(max_length=100)
    host_last_name = models.CharField(max_length=100)
    license_upload = models.FileField(upload_to='licenses/')
    def __str__(self):
        return f"{self.host_first_name} {self.host_last_name}"
    #def __str__(self):
        #return self.username


class Guide(CustomUser):
    approved = models.BooleanField(default=False)
    is_guide = models.BooleanField(default=True) 
    is_host = models.BooleanField(default=False)
    guide_first_name = models.CharField(max_length=30)
    guide_last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    #email = models.EmailField(unique=True)
    profilePicture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    location = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices, default='male')
    bio = models.TextField(blank=True, null=True)
    languages_spoken = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.guide_first_name} {self.guide_last_name}"

    

    
class PropertyType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    property_name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    number_of_bedrooms = models.PositiveIntegerField()
    number_of_bathrooms = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    upload_datetime = models.DateTimeField(default=timezone.now)
    host = models.ForeignKey(
        Host,  # Reference the Host model directly
        on_delete=models.CASCADE,
        related_name='properties', #for adding multiple properties
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.property_name


    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    description = models.TextField(blank=True)  # Add a description field
    

    def __str__(self):
        return f"Image for {self.property.property_name}"

class Availability(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date = models.DateField()
    is_available = models.BooleanField(default=True)

class WishlistItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s wishlist item for {self.property.property_name}"





class Booking(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.IntegerField()
    total_price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    num_guests = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Create a Payment record for the booking
        Payment.objects.create(booking=self, amount=self.total_price)


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    payment_id = models.AutoField(primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(default=timezone.now)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.booking_id} - {self.amount}"


from django.utils.crypto import get_random_string

class Feature(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class VisitTime(models.Model):
    time = models.TimeField()
    am_pm = models.CharField(max_length=2, choices=[('AM', 'AM'), ('PM', 'PM')])

    def __str__(self):
        return self.get_formatted_time()

    def get_formatted_time(self):
        formatted_time = self.time.strftime('%I:%M%p')
        return formatted_time


class AddService(models.Model):
    TYPE_CHOICES = [
        ('adventurous', 'Adventurous'),
        ('picnic', 'Picnic'),
        ('cultural', 'Cultural'),
        ('music_concerts', 'Music/Concerts'),
    ]

    service_id = models.CharField(max_length=50, unique=True, editable=False)
    service_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # Duration in minutes
    place = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    service_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='adventurous')
    features = models.ManyToManyField(Feature, related_name='services', blank=True)
    visit_times = models.ManyToManyField(VisitTime, related_name='services', blank=True)
    images = models.ImageField(upload_to='service_images/', null=True, blank=True)
    capacity = models.IntegerField(default=1) 
    guide = models.ForeignKey(
        Guide,  
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.service_name
    
    def save(self, *args, **kwargs):
        # Generate a unique service ID if it doesn't exist
        if not self.service_id:
            unique_id = get_random_string(length=8)
            self.service_id = f'SRV-{unique_id}'
        super().save(*args, **kwargs)

    def get_available_times(self):
        return self.visit_times.all()

class ServicePayment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField('ServiceBooking', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    PAYMENT_STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('not_completed', 'Not Completed'),
    ]

    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='completed')
    def __str__(self):
        return f"Payment ID: {self.payment_id}, Booking ID: {self.booking.booking_id}, Amount Paid: {self.amount_paid}, Date: {self.payment_date}"
 
class ServiceBooking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    service = models.ForeignKey('AddService', on_delete=models.CASCADE) 
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    booking_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    additional_request = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Booking ID: {self.booking_id}, Service: {self.service.service_name}, Guests: {self.number_of_guests}, Date: {self.booking_date}"
class Review(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    service = models.ForeignKey('AddService', on_delete=models.CASCADE) 
    rating = models.IntegerField()  # Assuming rating is an integer field representing out of 5
    reviewcomment = models.TextField()
    
    def __str__(self):
        return f"Review by {self.guest} for Service ID: {self.service_id}"
   
# class ServiceBooking(models.Model):
#     booking_id = models.AutoField(primary_key=True)
#     service = models.ForeignKey('AddService', on_delete=models.CASCADE) 
#     guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
#     booking_date = models.DateField()
#     number_of_guests = models.PositiveIntegerField()
#     additional_request = models.TextField(blank=True, null=True)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     def create_payment(self):
#     # Create a payment record associated with this booking
#         ServicePayment.objects.create(booking=self, amount_paid=self.total_price)
#     def save(self, *args, **kwargs):
#         # Call the parent class's save method
#         super().save(*args, **kwargs)
        
#         # Create a payment record after saving the booking
#         self.create_payment()
#     def __str__(self):
#         return f"Booking ID: {self.booking_id}, Service: {self.service.service_name}, Guests: {self.number_of_guests}, Date: {self.booking_date}"
    
