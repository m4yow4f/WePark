from django import forms
from app.models import ParkingSpace,Price,OpeningHours,Location,Size,Type,Features,ContactInformation,Review
from djmoney.forms.widgets import MoneyWidget
from django.forms.widgets import TimeInput,TextInput
from WePark.settings import CURRENCY_CHOICES

class AddParkingSpaceForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields="__all__"
        exclude = ["reviews", "seller_account"]
    
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'e.g. parking near football stadium'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'additional desciption of parking space and/or surrounding areas'}))
    size = forms.ModelChoiceField(queryset=Size.objects.all())
    type = forms.ModelChoiceField(queryset=Type.objects.all())
    features = forms.ModelMultipleChoiceField(queryset=Features.objects.all(),widget=forms.CheckboxSelectMultiple)
    
class OpeningHoursForm(forms.ModelForm):
     class Meta:
         model = OpeningHours
         fields = ["monday_open","monday_close","tuesday_open","tuesday_close","wednesday_open", "wednesday_close","thursday_open","thursday_close","friday_open", "friday_close","saturday_open", "saturday_close","sunday_open", "sunday_close"]
         widgets = {
             "monday_open": TimeInput(attrs={'type': 'time'}),
             "monday_close": TimeInput(attrs={'type': 'time'}),
             "tuesday_open": TimeInput(attrs={'type': 'time'}),
             "tuesday_close": TimeInput(attrs={'type': 'time'}),
             "wednesday_open": TimeInput(attrs={'type': 'time'}),
             "wednesday_close": TimeInput(attrs={'type': 'time'}),
             "thursday_open": TimeInput(attrs={'type': 'time'}),
             "thursday_close": TimeInput(attrs={'type': 'time'}),
             "friday_open": TimeInput(attrs={'type': 'time'}),
             "friday_close": TimeInput(attrs={'type': 'time'}),
             "saturday_open": TimeInput(attrs={'type': 'time'}),
             "saturday_close": TimeInput(attrs={'type': 'time'}),
             "sunday_open": TimeInput(attrs={'type': 'time'}),
             "sunday_close": TimeInput(attrs={'type': 'time'}),
         }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location 
        fields = ["address_number", "address_street", "city", "county","postcode", "country"] # rememember to add lat and long in algorithm view
        widgets = {
            "address_number": TextInput(attrs={'placeholder':' eg. "1", eg."1a"'}),
            "address_street": TextInput(attrs={'autocomplete':'address-line1'}),
            "city": TextInput(attrs={'autocomplete':'address-level2'}),
            "county": TextInput(attrs={'placeholder':'or state...'}),
            "postcode": TextInput(attrs={'autocomplete':'postal-code','placeholder':'or zipcode...'}),
            "country": TextInput(attrs={'autocomplete':'country-name'}),
        }

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = "__all__"

        widgets = {
           "hourly_price" : MoneyWidget(amount_widget=forms.TextInput(attrs={'class':'form-class','placeholder':'Enter Amount'}),currency_widget=forms.Select(attrs={'class':'form-control'},choices=CURRENCY_CHOICES)),
           "daily_price" : MoneyWidget(amount_widget=forms.TextInput(attrs={'class':'form-class','placeholder':'Enter Amount'}),currency_widget=forms.Select(attrs={'class':'form-control'},choices=CURRENCY_CHOICES)),
           "weekly_price" : MoneyWidget(amount_widget=forms.TextInput(attrs={'class':'form-class','placeholder':'Enter Amount'}),currency_widget=forms.Select(attrs={'class':'form-control'},choices=CURRENCY_CHOICES)),
           "monthly_price" : MoneyWidget(amount_widget=forms.TextInput(attrs={'class':'form-class','placeholder':'Enter Amount'}),currency_widget=forms.Select(attrs={'class':'form-control'},choices=CURRENCY_CHOICES))
        }

class ContactInformationForm(forms.ModelForm):
    class Meta:
        model = ContactInformation
        fields = "__all__"

class AddReview(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review_title", "review_body", "rating"]

