from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Register(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    father_name = models.CharField(max_length=50, null=False, blank=False)
    Username = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(default="example@gmail.com")
    password = models.CharField(max_length=100, null=True, blank=True)

class Text(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(default="example@gmail.com")
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()

class City(models.Model):
    city = models.CharField(max_length=50, null=True, blank=True, unique=True)

    def __str__(self):
        return self.city

class TouristSpot(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    yourname = models.CharField(max_length=100, null=True, blank=True, help_text="Name of the person who submitted this spot")
    image = models.ImageField(upload_to='spots/')
    extra_details = models.TextField(null=True, blank=True)
    location_url = models.URLField(help_text="Paste Google Maps location URL")

    def __str__(self):
        return self.name

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    location_url = models.URLField(blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    subtotal = models.FloatField(editable=False)
    trx_id = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)  # Useful for filtering

    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking for {self.hotel.name} in {self.city.name}"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('easypaisa', 'EasyPaisa'),
        ('jazzcash', 'JazzCash'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.BigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    card_no = models.CharField(max_length=16, blank=True, null=True)
    exp_date = models.CharField(max_length=7, blank=True, null=True)
    cvc = models.CharField(max_length=4, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    trx_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.method} - {self.amount}"


# models.py
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender_id": self.sender.id,
            "receiver_id": self.receiver.id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "edited": self.edited,
            "deleted": self.deleted,
        }
