from django import forms
from .models import waiter,Reservation, MenuItem, SubCategory

class waiterForm(forms.ModelForm):
    class Meta:
        model = waiter
        fields = "__all__"
        
        labels = {
            'waiter_id': 'Id',
            'waiter_name': 'Name',
            'waiter_email': 'Email',
            'waiter_password': 'Password',
            'waiter_phone': 'Phone Number',
            'waiter_shift': 'Shift',
            }
        
        widgets = {
            'waiter_id': forms.HiddenInput(),
            'waiter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'waiter_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'waiter_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'waiter_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'waiter_shift': forms.Select(attrs={'class': 'form-control'}),
        }
        
class loginForm(forms.ModelForm):
    class Meta:
        model = waiter
        fields = ['waiter_email', 'waiter_password']
        
        widgets = {
            'waiter_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'waiter_password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        
        
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'
        
        widgets = {
            'cus_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'cus_email': forms.EmailInput(attrs={'class': 'form-comtrol'}),
            'res_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'res_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'num_people': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
# ---------- MENU UPLOADING FORM----------
class MenuItemForm(forms.ModelForm):
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.order_by('id'),
        empty_label="(e.g. appetizers)",
        label="Choose Tab"
    )

    class Meta:
        model = MenuItem
        fields = ['subcategory', 'name', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Item name',
                'class': 'input'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Item description',
                'class': 'textarea'
            }),
            'price': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': 'Price',
                'class': 'input'
            }),
        }  