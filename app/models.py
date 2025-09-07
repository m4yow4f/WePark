"""
Definition of models.
"""

from django.db import models
from django.db.models import UniqueConstraint
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import AbstractBaseUser
from statistics import mean

###################### - Parking Space Models - ######################

#Model that defines the table that stores the information about a parking space
class ParkingSpace(models.Model):
    name = models.CharField(max_length=50,blank=False)
    description = models.TextField(blank=False)
    image = models.ImageField(null=True,upload_to="images/parking_spaces") 
    price = models.ForeignKey('Price',on_delete=models.CASCADE,null=True,blank=True)
    opening_hours = models.ForeignKey('OpeningHours',on_delete=models.CASCADE,null=True,blank=True) 
    location = models.OneToOneField('Location',on_delete=models.CASCADE,null=True,blank=True) 
    size = models.ForeignKey('Size',on_delete=models.CASCADE,null=True,blank=False) 
    type = models.ForeignKey('Type',on_delete=models.CASCADE,null=True,blank=False)
    features = models.ManyToManyField('Features',blank=False,db_table='ParkingSpaceFeatures') 
    reviews  = models.ManyToManyField('Review',blank=False,db_table='ParkingSpaceReviews')
    contact_information = models.ForeignKey('ContactInformation',on_delete=models.CASCADE,null=True,blank=True) 
    seller_account = models.ForeignKey('Account',on_delete=models.CASCADE,null=True,blank=False) 
    
    #returns all features for a parking space as a list 
    @property
    def features_list(self):
        return [feature for feature in self.features.all()]

    #returns all the reviews (depeding on the instance) as a list (in my __str__ format shown below)
    @property
    def reviews_list(self):
        return [review for review in self.reviews.all()]

    @property
    def average_review_rating(self):
        ratings_list = [review.rating for review in self.reviews.all()]
        try:
            average_rating = round( (mean(ratings_list)) * 2) / 2
        except:
            average_rating=0
        finally:
            return average_rating

# Model that defines table that stores the pricing information of a parking space
class Price(models.Model):
    
    hourly_price = MoneyField(default_currency="GBP",max_digits=19,decimal_places=2,null=True,blank=False) 
    daily_price = MoneyField(default_currency="GBP",max_digits=19,decimal_places=2,null=True,blank=True)
    weekly_price = MoneyField(default_currency="GBP",max_digits=19,decimal_places=2,null=True,blank=True)
    monthly_price = MoneyField(default_currency="GBP",max_digits=19,decimal_places=2,null=True,blank=True)

#Model that defines table that stores the opening hours of a parking space
class OpeningHours(models.Model):
    
    monday_open = models.TimeField(null=True,blank=False)
    monday_close = models.TimeField(null=True,blank=False)

    tuesday_open = models.TimeField(null=True,blank=False)
    tuesday_close = models.TimeField(null=True,blank=False)

    wednesday_open = models.TimeField(null=True,blank=False)
    wednesday_close = models.TimeField(null=True,blank=False)

    thursday_open = models.TimeField(null=True,blank=False)
    thursday_close = models.TimeField(null=True,blank=False)

    friday_open = models.TimeField(null=True,blank=False)
    friday_close = models.TimeField(null=True,blank=False)

    saturday_open = models.TimeField(null=True,blank=False)
    saturday_close = models.TimeField(null=True,blank=False)

    sunday_open = models.TimeField(null=True,blank=False)
    sunday_close = models.TimeField(null=True,blank=False)

#Model that defines table that stores the Location of a parking space
class Location(models.Model):
    address_number = models.CharField(max_length=10,blank=False) 
    address_street = models.CharField(max_length=100,blank=False)
    city = models.CharField(max_length=50,blank=False)
    county = models.CharField(max_length=100,blank=False)
    postcode = models.CharField(max_length=20,blank=False)
    country = models.CharField(max_length=100,blank=False)
    latitude= models.DecimalField(max_digits=18,decimal_places=15,blank=True,null=True,unique=True) 
    longitude= models.DecimalField(max_digits=18,decimal_places=15,blank=True,null=True,unique=True) 

#Model that defines the table that stores the sizes of a parking space 
class Size(models.Model):

    COMPACT = "CP" # parking space sizing for compact vehicles and motocycles  
    STANDARD = "SD" # parking space sizing for most vehicles
    OVERSIZED = "OS" # parking space sizing for large vehicles and machines
    SIZE_CATEGORY_CHOICES  = [ 
                    (COMPACT,"Compact"), 
                    (STANDARD,"Standard"), 
                    (OVERSIZED,"Oversized")
                    ]

    size_category = models.CharField(max_length = 2, choices= SIZE_CATEGORY_CHOICES, default=STANDARD, blank=False, null=True)

    def __str__(self):
        for code, display_name in self.SIZE_CATEGORY_CHOICES:
            if self.size_category == code:
                return display_name
        return self.size_category
    
#Model that defines the table that stores the type of parking space (where the parking space is located)
class Type(models.Model):

    STREET = "ST" 
    PARKINGKLOT = "PL" 
    PRIVATE = "PV" 
    TYPE_CATEGORY_CHOICES = [
                    (STREET,"Street Parking"),
                    (PARKINGKLOT, "Car Park"),  #used Car Park as user-friendly text as more commonly used
                    (PRIVATE, "Private Parking")
    ] 
    type_category = models.CharField(max_length=2,choices=TYPE_CATEGORY_CHOICES,blank =False,null=True)

    def __str__(self):
        for code, display_name in self.TYPE_CATEGORY_CHOICES:
            if self.type_category == code:
                return display_name
        return self.type_category 
  

#Model that defines the table that stores the Contact informtation of an owner of a parking space
class ContactInformation(models.Model):

    email = models.EmailField(blank=False,null=True,)
    phone_number = PhoneNumberField(region="GB",blank=False,null=True) 
    website = models.URLField(max_length=350,blank=False,null=True) 

#Model that defines the table that stores the different features of a parking space
class Features(models.Model):

    EVCHARGING = "EVC" 
    DISABLEDACCESS = "DBA" 
    HEIGHTRESTRICTION ="HRS" 
    NOHEIGHTRESTRICTION = "NHR" 
    LIGHTING = "LIT" 
    SECUREGATE = "SGE" 
    COVEREDPARKING ="CVP" 
    VIDEOSURVEILLANCE = "CTV" 
    
    FEATURE_NAME_CHOICES = [
                    (EVCHARGING,"EV Charging"),
                    (DISABLEDACCESS,"Disabled Access"),
                    (HEIGHTRESTRICTION,"Height Restriction"),
                    (NOHEIGHTRESTRICTION,"No Height Restriction"),
                    (LIGHTING,"Lighting"),   
                    (SECUREGATE,"Securely Gated"),
                    (COVEREDPARKING,"Covered Parking"),
                    (VIDEOSURVEILLANCE,"CCTV")
    ]
    
    feature_name = models.CharField(max_length=3,choices=FEATURE_NAME_CHOICES,blank=False,null=True)

    def __str__(self):
        for code, display_name in self.FEATURE_NAME_CHOICES:
            if self.feature_name == code:
                return display_name
        return self.feature_name
    
#Model that defines the table that stores the reviews of a parking space users submit
class Review(models.Model):
    review_title = models.CharField(max_length=50,blank=False) 
    review_body = models.TextField(max_length = 1000,blank=False) 
    rating = models.IntegerField(blank=False) 
    date_modified = models.DateTimeField(auto_now=True) 
    date_created = models.DateTimeField(auto_now_add=True) 
    #review_account = models.ForeignKey('Account',on_delete=models.CASCADE,null=False,blank=False)

    def __str__(self):
        return f"{self.review_body} By: self.review_account.first_name"


###################### - Account and Settings Models - ######################

#Model that defines the table that stores the accounts of the users of the parking application 
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50,blank=False)
    last_name = models.CharField(max_length=50,blank=False)
    email = models.EmailField(max_length=100, blank=False,unique=True)
    phone_number = PhoneNumberField(region="GB",unique=True,blank=True,null=True)
    settings_id = models.OneToOneField('Settings', on_delete=models.CASCADE,null=True)
    USERNAME_FIELD  = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    is_active = models.BooleanField(default=True)

#Model that defines the table that stores the Account and the Parking Space an account has planned for future use
class AccountsPlannedParkingSpaces(models.Model): 
    # account = models.ForeignKey('Account',on_delete=models.CASCADE,null=False,blank=False) 
    parking_space = models.ForeignKey('ParkingSpace', on_delete=models.CASCADE,null=False,blank=False)
    planned_datetime = models.DateTimeField(blank=False, null=False)
    
    #making sure that there are no duplicate planned parking spaces by the same account
    # class meta:
    #     constraints = [
    #         UniqueConstraint(fields=['account', 'parking_space'], name='unique_account_parking_space')
    #     ]

#Model that defines the table that stores the settings of a User account
class Settings(models.Model):
    payment_settings_id = models.OneToOneField('PaymentSettings', on_delete=models.CASCADE,null=True,blank=False) 
    parking_search_options_id = models.ForeignKey('ParkingSearchOptions',on_delete=models.CASCADE,null=True,blank=False) 
#Model that defines the table that stores the Payment settings of a User account
class PaymentSettings(models.Model):
    default_payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE,blank=True,null=True)
    cardholder_name = models.CharField(max_length=50,blank=True,null=True)
    card_number = models.CharField(max_length=19,blank=True,null=True)
    expiry = models.DateField(blank=True,null=True)
    e_wallet_email = models.EmailField(blank=True,null=True,max_length=100)

#Model that defines table that stores the different possible Payment Methods
class PaymentMethod(models.Model):

    DEBITCARD = "DC" 
    CREDITCARD = "CC"
    EWALLET = "EW" 
    
    PAYMENT_METHOD_CHOICES = [
                    (DEBITCARD,"Debit Card"),            
                    (CREDITCARD,"Credit Card"),
                    (EWALLET,"E-Wallet")
    ]
        
    payment_method_name = models.CharField(max_length=2,choices=PAYMENT_METHOD_CHOICES,blank=True,null=True)

#Model that defines table that stores the parking search options of a user account
class ParkingSearchOptions(models.Model):
    sort_by_feature = models.ForeignKey('Features',on_delete=models.CASCADE,blank=True,null=True)
    sort_by_type = models.ForeignKey('Type',on_delete=models.CASCADE,blank=True,null=True)
    sort_by_size = models.ForeignKey('Size', on_delete=models.CASCADE,blank=True,null=True)
    sort_by_distance = models.BooleanField(blank=True,null=False)
    sort_by_lowest_price = models.BooleanField(blank=True,null=True)
    sort_by_rating = models.BooleanField(blank=True,null=True)




