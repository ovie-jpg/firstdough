from django import forms 
from .models import Product, Category, Profile, Offer, Payment, Bank, Banks

choices= Category.objects.values_list('name', 'name')
choice_list= []

for item in choices:
    choice_list.append(item)



class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields= ('image', 'name', 'description', 'price', 'quantity', 'category', 'commission')

        widgets= {
            'category': forms.Select(choices= choice_list)
        }

        def get_absolute_url(self):
            return reverse('home')

class ProductEdit(forms.ModelForm):
    class Meta:
        model= Product
        fields= ('image','name', 'description', 'price', 'quantity', 'category', 'commission')

        widgets= {
            'category': forms.Select(choices= choice_list)
        }

