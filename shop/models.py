from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    name= models.CharField(max_length= 25)

    def get_absolute_url(self):
        return reverse('home')

class Product(models.Model):
    image= models.ImageField(upload_to= "media")
    name= models.CharField(max_length=25)
    description= models.TextField()
    price= models.IntegerField()
    quantity= models.IntegerField(blank= True, null= True)
    category= models.TextField()
    commission= models.IntegerField(blank=True, null=True)
    discount= models.IntegerField(blank=True, null=True)
    date= models.DateTimeField(auto_now_add= True)

    def get_absolute_url(self):
        return reverse('home')

class Offer(models.Model):
    product= models.ManyToManyField(Product, blank= True)
    discount_percentage= models.IntegerField()
    valid_till= models.DateTimeField()

    def get_absolute_url(self):
        return reverse('home')

class Profile(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE)
    image= models.ImageField(upload_to= "media", blank=True, null=True)
    name= models.CharField(max_length=25)
    code= models.CharField(max_length=5)
    email= models.EmailField()
    telephone= models.CharField(max_length=14)
    earnings= models.IntegerField(default= 0)
    rec_by= models.ForeignKey(User, on_delete= models.CASCADE, related_name= "rec_by", null=True)
    recommendations= models.ManyToManyField(User, blank=True, related_name= "recs")
    joined= models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('home')

class Payment(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.CharField(max_length=25)
    quantity= models.IntegerField(default= 1, blank=True, null=True)
    amount= models.IntegerField()
    ref= models.CharField(max_length=7)
    email= models.EmailField(default= "None")
    transaction= models.CharField(max_length=25, default= "unconfirmed")
    date= models.DateField(auto_now_add= True)

class Bank(models.Model):
    user= models.OneToOneField(User, on_delete= models.CASCADE, null=True)
    transfer_amount= models.IntegerField(blank=True, null=True)
    transfer_note= models.TextField(blank=True, null=True)
    transfer_reference= models.CharField(max_length=25, blank=True, null=True)
    recipient_code= models.CharField(max_length=25, blank=True, null=True)
    bank_slug= models.CharField(max_length=25, blank=True, null=True)
    bank_code= models.CharField(max_length=25, blank=True, null=True)
    account_name= models.CharField(max_length=25, blank=True, null=True)
    account_number= models.IntegerField(blank=True, null=True)
    email= models.EmailField()

    def get_absolute_url(self):
        return reverse('home')

class Banks(models.Model):
    name= models.CharField(max_length=25)
    code= models.CharField(max_length=25)

    def get_absolute_url(self):
        return reverse('home')

class Transfer(models.Model):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    amount= models.IntegerField()
    recipient= models.CharField(max_length=50)
    transfer_code= models.CharField(max_length=7)
    bank_code= models.CharField(max_length=25)
    account_number= models.IntegerField()
    recipient_name= models.CharField(max_length=200)
    status= models.CharField(max_length=25, blank=True, null= True, default= "unconfirmed")
    date= models.DateTimeField(auto_now_add= True)

class Profit(models.Model):
    amount= models.IntegerField()

    # Singleton pattern to ensure only one entry
    def save(self, *args, **kwargs):
        if not self.pk and Profit.objects.exists():
            # Only allow one entry
            raise ValidationError('Only one PaystackKeys entry allowed')
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Profit'

    def get_absolute_url(self):
        return reverse('blog-page')

class PaystackKeys(models.Model):
    public_key = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=100)

    # Singleton pattern to ensure only one entry
    def save(self, *args, **kwargs):
        if not self.pk and PaystackKeys.objects.exists():
            # Only allow one entry
            raise ValidationError('Only one PaystackKeys entry allowed')
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Paystack Keys'

class About(models.Model):
    title= models.CharField(max_length=50)
    description= models.TextField()
    phone= models.TextField()
    email= models.EmailField()
    location= models.TextField()

    def get_absolute_url(self):
        return reverse('contact')