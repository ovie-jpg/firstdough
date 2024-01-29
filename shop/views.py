from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Offer, Payment, Bank, Banks, Transfer, PaystackKeys, Profit, About
import uuid
from datetime import date
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ProductForm, ProductEdit
from django.urls import reverse
import requests
from django.contrib import messages
from decimal import Decimal
from django.core.mail import send_mail

# Create your views here.
def home(request, **kwargs):
    ref_by= str(kwargs.get("ref_by"))
    if About.objects.filter(pk=1).exists():
        about= About.objects.get(pk=1)
    else:
        about= None
    pasteries= Product.objects.filter(category= 'Pasteries')
    products= Product.objects.filter(category= 'Bread')
    # products= Product.objects.all()
    
    context= {
        'products': products,
        'pasteries': pasteries,
        'ref_by': ref_by,
        'about': about
    }
    return render(request, 'home.html', context)

def info(request, pk, **kwargs):
    ref_by= str(kwargs.get("ref_by"))
    if Profile.objects.filter(code=ref_by).exists():
        profile= Profile.objects.get(code=ref_by)
    else:
        profile= None
    product= Product.objects.get(pk=pk)
    ref= str(uuid.uuid4()).replace("-", "")[:7]
    offers= Offer.objects.all()
    offer= ''
    today= date.today()

    if Offer.objects.filter(product=product).exists():
        offer= Offer.objects.get(product=product)
        product.discount= product.price - (offer.discount_percentage/100 * product.price)
        product.save()
    elif Offer.objects.filter(product=product).exists() == False:
        product.discount= None
        product.save()

    if offer != '' and offer.valid_till == today:
        offer.delete()

    if request.method == 'POST':
        quantity= int(request.POST['quantity'])
        try:
            if product.discount:
                amount= product.discount*quantity
                payment= Payment.objects.create(user= request.user, product= product.name, quantity=quantity, amount= amount, ref= ref)
                payment.save()
                return redirect('init-payment', payment.pk)
            else:
                amount = product.price*quantity
                payment= Payment.objects.create(user= request.user, product= product.name, quantity=quantity, amount= amount, ref= ref, email= request.user.email)
                payment.save()
                return redirect('init-payment', payment.pk)
        except:
            messages.info(request, 'register on the website or login to purchase')

    context= {
        'product': product,
        'offers': offers,
        'offer': offer,
        'profile': profile
    }
    return render(request, "info.html", context)

def search(request, **kwargs):
    ref_by= str(kwargs.get("ref_by"))
    search= request.GET['search']
    products= Product.objects.filter(name__icontains=search)

    context= {
        'ref_by': ref_by,
        'search': search,
        'products': products
    }
    return render(request, 'search.html', context)


def offer_info(request, pk, pk2):
    product= Product.objects.get(pk=pk)
    offer= Offer.objects.get(pk= pk2)

    if request.method == 'POST':
        if product in offer.product.all():
            offer.product.remove(product)
            return redirect('info', product.pk)
        else:
            offer.product.add(product)
            return redirect('info', product.pk)
    context= {
        'product': product,
        'offer': offer
    }
    return render(request, 'offer-info.html', context)

class AddProduct(CreateView):
    model= Product
    template_name= "add-product.html"
    form_class= ProductForm

class EditProduct(UpdateView):
    model= Product
    template_name= "edit-product.html"
    form_class= ProductEdit

class DelProduct(DeleteView):
    model= Product
    template_name= "delete-product.html"
    success_url= reverse_lazy('home')

class AddOffer(CreateView):
    model= Offer
    template_name= "add-offer.html"
    fields= ('discount_percentage', 'valid_till')

class EditOffer(UpdateView):
    model= Offer
    template_name= "edit-offer.html"
    fields= ('discount_percentage', 'valid_till')

class DelOffer(DeleteView):
    model= Offer
    template_name= "delete-offer.html"
    success_url= reverse_lazy('home')

def profile(request):
    profile= Profile.objects.get(user= request.user)
    transfer_code= str(uuid.uuid4()).replace("-", "")[:7]
    if Bank.objects.filter(user=request.user).exists():
        bank= Bank.objects.get(user=request.user)
    else:
        bank= None
    
    if request.method == 'POST':
        if bank is not None:
            transfer= Transfer.objects.create(user= request.user, amount= profile.earnings, recipient= bank.bank_slug, transfer_code= transfer_code, bank_code= bank.bank_code, account_number= bank.account_number, recipient_name= bank.account_name)
            transfer.save()
            return redirect('withdraw', transfer.pk)
        else:
            messages.info(request, 'upload bank details first')

    context= {
        'profile': profile,
        'bank': bank
    }
    return render(request, 'profile.html', context)

class ProfileEdit(UpdateView):
    model= Profile
    template_name= "edit-profile.html"
    fields= ('image', 'telephone')

def paystack_keys(request):
    paystack= PaystackKeys.objects.all()
    context= {
        'paystack':paystack
    }
    return render(request, 'paystack-keys.html', context)

class AddPK(CreateView):
    model= PaystackKeys
    template_name= 'add-pk.html'
    fields= '__all__'

class EditPK(UpdateView):
    model= PaystackKeys
    template_name= 'edit-pk.html'
    fields= '__all__'

def add_bank(request):
    paystack= PaystackKeys.objects.get(pk=1)
    paystack_secretkey= paystack.secret_key
    headers= {
        "Authorization": 'Bearer ' + paystack_secretkey,
        "Content-Type": 'application/json'
    }
    url= 'https://api.paystack.co/bank'
    response= requests.get(url, headers= headers)
    res_json= response.json()
    banks= Banks.objects.all()

    if request.method == 'POST':
        name= request.POST['name']
        code= request.POST['code']

        if Banks.objects.filter(name=name).exists():
            messages.info(request, 'bank already registered')
        else:
            banks= Banks.objects.create(name=name, code=code)
            return redirect(profile)

    context= {
        'banks': banks,
        'res_json': res_json
    }
    return render(request, 'add-bank.html', context)

class EditBank(UpdateView):
    model= Banks
    template_name= "edit-bank.html"
    fields= '__all__'

class DeleteBank(DeleteView):
    model= Banks
    template_name= "delete-bank.html"
    success_url= reverse_lazy('profile')


def bank_details_upload(request):
    banks= Banks.objects.all()

    if request.method == 'POST':
        bank_slug= request.POST['bank_slug']
        bank_code= request.POST['bank_code']
        account_name= request.POST['account_name']
        account_number= request.POST['account_number']

        if Bank.objects.filter(account_number=account_number).exists() and Bank.objects.filter(bank_slug= bank_slug).exists():
            messages.info(request, 'Details already exists')
        else:
            bank= Bank.objects.create(user= request.user, bank_slug=bank_slug, bank_code=bank_code, account_name=account_name, account_number=account_number, email= request.user.email)
            bank.save()
            return redirect('profile')
    
    context= {
        'banks': banks,
    }
    return render(request, "bank-details.html", context)

class BankEdit(UpdateView):
    model= Bank
    template_name= "bank-edit.html"
    fields= ('bank_code','bank_slug', 'account_name', 'account_number')

class BankDelete(DeleteView):
    model= Bank
    template_name= "bank-delete.html"
    success_url= reverse_lazy('profile')

class AddCat(CreateView):
    model= Category
    template_name= "add-cat.html"
    fields= ('name',)

    def get_absolute_url(self):
        return reverse('home')

class EditCat(UpdateView):
    model= Category
    template_name= "edit-cat.html"
    fields= ('name',)

class DelCat(DeleteView):
    model= Category
    template_name= "delete-cat.html"
    success_url= reverse_lazy('home')

def transaction_history(request):
    payments= Payment.objects.filter(user= request.user).order_by('-date')
    
    context= {
        'payments': payments
    }
    return render(request, 'trans-hist.html', context) 

def initialize_payment(request, pk):
    payment= Payment.objects.get(pk=pk)
    # paystack_publickey= 'pk_test_0d607ce9950cf59c2862bad631607f4ac1f28a7a'
    paystack= PaystackKeys.objects.get(pk=1)
    paystack_publickey= paystack.public_key

    context= {
        'payment': payment,
        'public_key': paystack_publickey
    }
    return render (request, 'init-payment.html', context)

def verify_payment(request, ref):
    payment= Payment.objects.get(ref=ref)
    paystack= PaystackKeys.objects.get(pk=1)
    paystack_secretkey= paystack.secret_key
    headers= {
        "Authorization": 'Bearer ' + paystack_secretkey,
        "Content-Type": 'application/json'
    }
    url= 'https://api.paystack.co/transaction/verify/'
    response= requests.get(url + payment.ref, headers= headers)
    res_json= response.json()
    if res_json['status'] == True:
        payment.transaction= "successful"
        payment.save()
    else:
        payment.transaction= "unsuccessful"
        payment.save()

    profile= Profile.objects.get(user= request.user)
    product= Product.objects.get(name= payment.product)
    
    if payment.transaction == "successful":
        if Profile.objects.filter(recommendations= request.user).exists() and product.commission is not None:
            ref_profile= Profile.objects.get(recommendations= request.user)
            ref_profile.earnings += product.commission/100 * payment.amount
            ref_profile.save()
         
    context= {
        'response': response.json,
        'payment': payment
    }
    return render(request, 'verify.html', context)

def withdraw(request, pk):
    paystack_secretkey= 'sk_test_abb941d36e3e441e11a16f615028ef499028f5ff'
    transfer= Transfer.objects.get(pk=pk)
    headers= {
        "Authorization": 'Bearer ' + paystack_secretkey,
        "Content-Type": 'application/json'
    }
    payload = {
        'source': 'balance',
        'amount': transfer.amount * 100,  # Amount in kobo (1 NGN = 100 kobo)
        'recipient': transfer.recipient,
        'transfer_code': transfer.transfer_code,
        'bank_code': transfer.bank_code,
        'account_number': transfer.account_number,
        'recipient_name': transfer.recipient_name,
    }
    url= 'https://api.paystack.co/transfer'
    if request.method == 'POST':
        try:
            response= requests.post(url, json=payload, headers= headers)
            res_json= response.json()
            messages.info(request, res_json)
            if res_json['status'] == False:
                transfer.status= "Failed"
                transfer.save()
                return redirect('withdraw-history')
            else:
                transfer.status= "successful"
                transfer.save()
                return redirect('withdraw-history')
        except:
            messages.info(request, 'error: check if bank details are correct')
        
    context= {
        'transfer': transfer,
    }
    return render(request, 'withdraw.html', context)

def withdrawal_history(request):
    transfer= Transfer.objects.filter(user=request.user).order_by('-date')
    context= {
        'transfers': transfer
    }
    return render(request, 'withdraw-history.html', context)

def contact(request):
    if About.objects.filter(pk=1).exists():
        about= About.objects.get(pk=1)
    else:
        about= None

    context= {
        'about': about
    }
    return render(request, 'contact.html', context)

class AddContact(CreateView):
    model= About
    template_name= 'add-contact.html'
    fields= '__all__'

class EditContact(UpdateView):
    model= About
    template_name= 'add-contact.html'
    fields= '__all__'


def email_notifications(request):
    profiles= Profile.objects.all()
    if request.method== 'POST':
        subject= request.POST['subject']
        message= request.POST['message']
        from_email= request.user.email
        for profile in profiles:
            recipient_list= profile.email
            # subject = 'Hello, this is the subject'
            # message = 'This is the message body.'
            # from_email = 'your_email@example.com'
            # recipient_list = ['recipient@example.com']

            send_mail(subject, message, from_email, [recipient_list])
            messages.info(request, 'email sent')
    return render(request, 'email.html')
