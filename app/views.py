from django.shortcuts import render,redirect
from datetime import datetime
from .forms import AddParkingSpaceForm,PriceForm,OpeningHoursForm,LocationForm,ContactInformationForm,AddReview
from app.models import Price,OpeningHours,ContactInformation,ParkingSpace,Features,AccountsPlannedParkingSpaces
from django.db.models import Avg,Sum

Year =  datetime.now().year

def home(request):
    return render(request,"home.html",{'year':Year})

def about(request):
    return render(request,"about.html",{'year':Year})

#-----------------------------account views--------------------------------------
def login(request):
    #do if-post statement and else return below
    return render(request,"accounts/login.html",{'year':Year})

def create_account(request):
    #do if-post statement and else return below
    return render(request,"accounts/create account.html",{'year':Year})
#-----------------------------parking views--------------------------------------
def rent_out_parking_space(request):
    return render(request,"parking/rent out parking spaces.html",{'year':Year})

def save_parking_space(add_parking_space_form,price_form,opening_hours_form,location_form,contact_information_form):
            # Save related models
            parking_space = add_parking_space_form.save(commit=False)
            # checking if form submitted data is in database already. So no data dublication
            try:
                price = Price.objects.get(**price_form.cleaned_data)
                print(" price aquired")
            except Price.DoesNotExist:
                print("price doesnt exist")
                price = price_form.save(commit=False)

            try:
                opening_hours = OpeningHours.objects.get(**opening_hours_form.cleaned_data)
                print(" opening_hours aquired")
            except OpeningHours.DoesNotExist:
                print("opening_hours doesnt exist")
                opening_hours = opening_hours_form.save(commit=False)

            location = location_form.save(commit=False) #location is one2one field so dublication allowed

            try:
                contact_information = ContactInformation.objects.get(**contact_information_form.cleaned_data)
                print(" contact_information aquired")
            except ContactInformation.DoesNotExist:
                print("contact_information doesnt exist")
                contact_information = contact_information_form.save(commit=False)
            
            #saving forms in repective tables
            price.save()
            opening_hours.save()
            location.save()
            contact_information.save()

            #saving form foreign keys to parking space object
            parking_space.price = price
            parking_space.opening_hours = opening_hours
            parking_space.location = location
            parking_space.contact_information = contact_information

            #saving parking space to table
            parking_space.save()
            add_parking_space_form.save_m2m() # Why the M2M features are saved to the table

#add login required
def upload_parking_space(request):
    if request.method == 'POST':
        
        #changing post data, so that it the field can be accessed when being saved
        new_post_data = request.POST.copy()
        new_post_data['address_street'] = new_post_data['address_street address-search']
        request.POST = new_post_data

        add_parking_space_form = AddParkingSpaceForm(request.POST, request.FILES)
        opening_hours_form = OpeningHoursForm(request.POST)
        price_form = PriceForm(request.POST)
        location_form = LocationForm(request.POST)
        contact_information_form = ContactInformationForm(request.POST)

        if add_parking_space_form.is_valid() and opening_hours_form.is_valid() and price_form.is_valid() and location_form.is_valid() and contact_information_form.is_valid():
            
            # Save related models
            save_parking_space(add_parking_space_form,price_form,opening_hours_form,location_form,contact_information_form)
            return redirect(home)
        
        else:
            forms = [add_parking_space_form,opening_hours_form,location_form,contact_information_form,price_form]
            for form in forms:
                if form.errors:
                    print("**********Errors**********")
                    print(form.errors.as_text)
                    print("**************************")

    else:
        add_parking_space_form = AddParkingSpaceForm()
        price_form = PriceForm()
        opening_hours_form = OpeningHoursForm()
        location_form = LocationForm()
        contact_information_form = ContactInformationForm()

    data = {
        'add_parking_space': add_parking_space_form,
        "opening_hours": opening_hours_form,
        'price':price_form,
        'location':location_form,
        'contact_information':contact_information_form,
        'year': Year
    }
    return render(request, "parking/upload parking space.html", data)

#login required!
def manage_parking_spaces(request):
    user_parking_spaces = ParkingSpace.objects.all()

    parking_spaces_data = user_parking_spaces.values('id','name','description','location__city','location__postcode','image') 

    data ={
        'parking_spaces':parking_spaces_data,
        'year': Year
    }
    return render(request,"parking/manage parking spaces.html",data)

def delete_managed_parking_space(request,pk):
    parking_space = ParkingSpace.objects.get(pk=pk)
    parking_space.delete()
    print(parking_space,"has been deleted")
    return redirect(manage_parking_spaces)

#add login required!
def update_parking_space(request,pk):
    instance_parking_space = ParkingSpace.objects.get(pk=pk)
    instance_features = Features.objects.filter(parkingspace=pk)
    instance_parking_space.features.set(instance_features)
    instance_price = instance_parking_space.price
    instance_opening_hours = instance_parking_space.opening_hours
    instance_location = instance_parking_space.location
    instance_contact_information = instance_parking_space.contact_information

    if request.method == "POST":

        #changing post data, so that it the field can be accessed when being saved
        new_post_data = request.POST.copy()
        new_post_data['address_street'] = new_post_data['address_street address-search']
        request.POST = new_post_data

        add_parking_space_form = AddParkingSpaceForm(request.POST, request.FILES,instance=instance_parking_space)
        price_form = PriceForm(request.POST,instance=instance_price)
        opening_hours_form = OpeningHoursForm(request.POST,instance=instance_opening_hours)
        location_form = LocationForm(request.POST,instance=instance_location)
        contact_information_form = ContactInformationForm(request.POST,instance=instance_contact_information)

        if add_parking_space_form.is_valid() and opening_hours_form.is_valid() and price_form.is_valid() and location_form.is_valid() and contact_information_form.is_valid():
            # Saves edits to related objects
            save_parking_space(add_parking_space_form,price_form,opening_hours_form,location_form,contact_information_form)
            return redirect(home)
        
        else:
            forms = [add_parking_space_form,opening_hours_form,location_form,contact_information_form,price_form]
            for form in forms:
                if form.errors:
                    print("**********Errors**********")
                    print(form.errors.as_text)
                    print("**************************")

    else:
        add_parking_space_form = AddParkingSpaceForm(instance=instance_parking_space)
        price_form = PriceForm(instance=instance_price)
        opening_hours_form = OpeningHoursForm(instance=instance_opening_hours)
        location_form = LocationForm(instance=instance_location)
        contact_information_form = ContactInformationForm(instance=instance_contact_information)

    data ={
        'parking_space':instance_parking_space,
        'add_parking_space': add_parking_space_form,
        "opening_hours": opening_hours_form,
        'price':price_form,
        'location':location_form,
        'contact_information':contact_information_form,
        'year': Year
    }
    return render (request,"parking/update parking space.html",data)

def bookmarked_parking(request):
    all_user_parking_spaces = AccountsPlannedParkingSpaces.objects.all()

    #getting all bookmarked parking spaces that are after current day
    user_parking_spaces_in_future = all_user_parking_spaces.filter(planned_datetime__gte = datetime.now())
    
    #getting the bookmarked parking spaces ordered in an acending manner
    user_parking_spaces = user_parking_spaces_in_future.order_by("planned_datetime")

    parking_space_objects = ParkingSpace.objects.filter(accountsplannedparkingspaces__isnull=False,accountsplannedparkingspaces__planned_datetime__gte=datetime.now()).order_by("accountsplannedparkingspaces__planned_datetime") 

    #Using for loop to add features using my custom model function 
    features_list = [parking_space.features_list for parking_space in parking_space_objects]

    parking_spaces_data = user_parking_spaces.values('id','parking_space__id','parking_space__name','parking_space__price__hourly_price_currency','parking_space__price__hourly_price','parking_space__location__city','parking_space__location__postcode','parking_space__image','planned_datetime') 

    #used so I can iterate through both the parking_spaces_data and the features_list concurrently - so that I do not need to use django orm that creaets unncessary parking spaces to accomodate for multiple features for 
    full_parking_space_data = zip(parking_spaces_data,features_list)
    
    data ={
        'parking_spaces':full_parking_space_data,
        'year': Year
    }
    return render (request,"parking/bookmarked parking.html",data)

def remove_bookmarked_parking_space(request,pk):
    if request.method == "POST":
        parking_space = AccountsPlannedParkingSpaces.objects.get(parking_space=pk)
        parking_space.delete()
        print(parking_space," has been deleted")

    return redirect(request.META.get('HTTP_REFERER'))

def top_rated_spaces(request):
    parking_spaces = ParkingSpace.objects.annotate(is_review = Sum("reviews__id")).filter(is_review__gt=0) # had to add annotate so that parking spaces with no reviews are included in the calculations

    top_parking_spaces = parking_spaces.annotate(ratings=(Avg("reviews__rating"))).order_by("-ratings") 
    
    top_hundred_parking_spaces = top_parking_spaces[:99]
    
    parking_spaces_data = top_hundred_parking_spaces.values("id","name","image")

    reviews_ratings_data = [parking_space.average_review_rating for parking_space  in top_hundred_parking_spaces] 

    reviews_text_data = [parking_space.reviews_list for parking_space in top_hundred_parking_spaces] 

    full_parking_spaces_data = zip(parking_spaces_data,reviews_ratings_data,reviews_text_data)

    data ={
        'parking_spaces':full_parking_spaces_data,
        'year': Year
    }
    return render(request,"parking/top rated parking spaces.html",data)

def parking_space_information(request,name,pk):
    if request.method == "POST":
        parking_space = ParkingSpace.objects.get(pk=pk,name=name) 
        review_form = AddReview(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.save()

            parking_space.reviews = review
            parking_space.save()
    else:
        parking_space = ParkingSpace.objects.get(pk=pk,name=name) 
        review_form = AddReview()
        isBookmarked  = AccountsPlannedParkingSpaces.objects.filter(parking_space=parking_space).exists()

    data ={
        'parking_space':parking_space,
        'parking_space_isBookmarked':isBookmarked,
        'review_form':review_form,
        'year': Year
    }
    return render(request,'parking/parking space information.html',data)

def search_parking_spaces(request):
    return






