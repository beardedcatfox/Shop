from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import validate_email
from django.forms import EmailField, inlineformset_factory
from django.shortcuts import get_object_or_404

from orders.models import Order, OrderItem

from .models import Book, Client


class ClientRegisterForm(UserCreationForm):
    email = EmailField(required=True, validators=[validate_email])

    class Meta:
        model = Client
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'address']


class UserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Client
        fields = ('address', 'email', 'first_name', 'last_name', 'birth_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('address', 'birth_date')  # 'first_name', 'second_name'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, book_id=None, max_quantity=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = None
        if book_id is not None:
            self.book = get_object_or_404(Book, id=book_id)
            max_quantity = self.book.quantity if self.book else 1
        if max_quantity is not None:
            self.fields['quantity'].widget.attrs['max'] = max_quantity

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if self.book is None or quantity > self.book.quantity:
            raise forms.ValidationError("The quantity not the available stock.")
        return quantity


class OrderForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=250, required=True)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity']
        widgets = {
            'book': forms.HiddenInput(),
        }


OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0, can_delete=False)
