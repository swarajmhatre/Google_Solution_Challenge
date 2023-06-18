from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from math import ceil
from .models import CustomUser, Contact, Adoption, lostandfound, Breed
from .forms import AdoptionForm,LAFform
import numpy as np
from PIL import Image
import tensorflow as tf
import numpy as np
from django.core.files.storage import FileSystemStorage
import io
from keras.models import load_model
# from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Create your views here.
def index(request):
    return render(request, 'index.html')

def predict(request):
    return render(request, 'predict.html')

def predict_image(request):
    if request.method == 'POST' and request.FILES['image']:
        # Get the image from the request
        image_file = request.FILES['image']
        print(type(image_file))

        # Preprocess the image
        img = Image.open(image_file)
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype('float32') / 255.0

        # Load the saved model
        model = load_model('model/my_pet_breeds_MobileNet.h5', compile=False)

        # Make a prediction on the image
        prediction = model.predict(img_array)
        breed_idx  = np.argmax(prediction, axis=1)

        # Map the prediction to a label
        # map the class index to the breed name
        class_map = {0: 'abyssinian', 1: 'American Shorthair', 2:'beagle',3:'boxer',4:'Bulldog',5:'chihuahua',6:'corgi',7:'dachshund',8:'German shepherd',9:'golden retriever',10:'husky',11:'labrador',12:'maine coon',13:'mumbai cat',14:'persian cat',15:'pomeranian',16:'pug',17:'ragdoll cat',18:'rottwiler',19:'shiba inu',20:'siamese cat',21:'sphynx', 22: 'yorkshire terrier'}
        prediction = tuple(breed_idx )
        pred_idx = prediction[0]
        predicted_breed = class_map[pred_idx]

        breed = Breed.objects.filter(name=predicted_breed)
        print(breed)
        print(breed[0].height)
        params = {'breed':breed[0]}

        print(predicted_breed)

        # Pass the prediction and image url to the template
        # , {'label': label, 'image_url': uploaded_image_url}
        # return render(request, 'prediction.html')

    return render(request, 'predict.html',params)

def lostandFound(request):
    cats = {item['breed'] for item in lostandfound.objects.values('breed')}
    allpets = []

    for cat in cats:
        pet = lostandfound.objects.filter(breed=cat)
        n = len(pet)
        if (n % 3 == 0):
            outer = int(n / 3)
        else:
            outer = n // 3 + 1

        pets_for_cat = [cat, range(outer), range(n), pet]
        allpets.append(pets_for_cat)

    params = {'allpets': allpets}


    return render(request, 'lost_find.html', params)

def adoption(request):
    cats = {item['breed'] for item in Adoption.objects.values('breed')}
    allpets = []

    for cat in cats:
        pet = Adoption.objects.filter(breed=cat)
        n = len(pet)
        if (n % 3 == 0):
            outer = int(n / 3)
        else:
            outer = n // 3 + 1

        pets_for_cat = [cat, range(outer), range(n), pet]
        allpets.append(pets_for_cat)

    params = {'allpets': allpets}


    return render(request, 'adopt.html', params)


def contact(request):
    return render(request, "contact.html")


def profile(request):
    if request.method == "POST":
        adoptionform = AdoptionForm(request.POST or None, request.FILES or None)
        lafform = LAFform(request.POST or None, request.FILES or None)
        # print(formset.errors)
        if adoptionform.is_valid():
            adoptionform.save()
        if lafform.is_valid():
            lafform.save()
        

    adoptionform = AdoptionForm()
    lafform = LAFform()

    allpets = []
    allpets2 = []
    owner = request.user.id
    print(owner)
    Userprods = Adoption.objects.values('owner')
    Userprods2 = lostandfound.objects.values('temp_owner')
    # print(Userprods)
    cats = {item['owner'] for item in Userprods}
    cats2 = {item['temp_owner'] for item in Userprods2}


    for cat in cats:
        # print(cat)
        if (cat == request.user.id):
            # print(request.user.id)
            pet = Adoption.objects.filter(owner=cat)
            # print(book)

            n = len(pet)
            # print(n)
            if (n % 3 == 0):
                outer = int(n / 3)
                # print(outer)
            else:
                outer = n // 3 + 1
            allpets.append([range(outer), range(n), pet])

            # allProds = Product.objects.all()
            # print(allProds)
            params = {'allpets':allpets ,'LAFform':lafform,'Aform':adoptionform}

        else:
            continue
    for cat in cats2:
        # print(cat)
        if (cat == request.user.id):
            # print(request.user.id)
            pet = lostandfound.objects.filter(temp_owner=cat)
            # print(book)

            n = len(pet)
            # print(n)
            if (n % 3 == 0):
                outer = int(n / 3)
                # print(outer)
            else:
                outer = n // 3 + 1
            allpets2.append([range(outer), range(n), pet])

            # allProds = Product.objects.all()
            # print(allProds)
            params = {'allpets2':allpets2,'allpets':allpets  ,'LAFform':lafform,'Aform':adoptionform}

        else:
            continue
        
    return render(request, 'profile.html', params)

def LSpage(request):
    return render(request, 'login.html')

def signup(request):
    message = False
    if request.method == "POST":
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        contact = request.POST.get('contact', '')
        age = request.POST.get('age', '')
        country = request.POST.get('country', '')
        city = request.POST.get('city', '')

        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                        last_name=last_name, contact=contact,  age=age, country=country, city=city)
        messages.success(request, 'Your account has been successfully created!')
        user.save()
    return redirect('website')

def logoutUser(request):
    logout(request)
    print("Logged out")
    return redirect('website')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            print("success login")
            return redirect('website')
        else:
            messages.error(request, "Error login")
            print("Error login")
            return redirect('website')

def listadoption(request):
    if request.method == "POST":
        print(request.FILES)
        pet_name = request.POST.get('pet_name')
        image = request.FILES.get('image')
        breed = request.POST.get('breed')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        owner = request.user
        color = request.POST.get('color')
        eating_habits = request.POST.get('eating_habits')
        alergies = request.POST.get('alergies')
        # provider = current_user.username
        adopt = Adoption(pet_name=pet_name, breed=breed, image=image, gender=gender, age=age, owner=owner, color=color, eating_habits=eating_habits, alergies=alergies)
        adopt.save()
        thank = True
    return render(request, 'profile.html', {'thank': thank})

def listlaf(request):
    if request.method == "POST":

        gender = request.POST.get('breed')
        distinctmarks = request.POST.get('breed')
        temp_owner = request.user
        image = request.FILES.get('image')
        breed = request.POST.get('breed')
        gender = request.POST.get('gender')
        color = request.POST.get('color')

        # provider = current_user.username
        laf = lostandfound(temp_owner=temp_owner, breed=breed, image=image, gender=gender,  color=color,  distinctmarks=distinctmarks)
        laf.save()
        thank = True

    return render(request, 'profile.html', {'thank': thank})
        
# def searchMatch(query, item):
#     print("Item to search is ", item.book_name)
#     if query in item.description.lower() or query in item.book_name:
#         print("Inside ifff")
#         return True
#     else:
#         return  False
# def search(request):
#     query = request.GET.get('search')
#     # print(query)
#     allProds = []
#     catprods = Book.objects.values('book_name')
#     print(catprods)
#     cats = {item['book_name'] for item in catprods}
#     for cat in cats:
#         prodtemp = Book.objects.filter(book_name=cat)
#         print(prodtemp)
#         prod = [item for item in prodtemp if searchMatch(query, item)]
#         # print(prod)
#         n = len(prod)

#         nSlides = n // 4 + ceil((n / 4) - (n // 4))
#         if len(prod) != 0:
#             allProds.append([prod,range(8), range(1, nSlides), nSlides])
#     params = {'allProds': allProds, "msg": ""}
#     print("params is :", params)
#     if len(allProds)==0 or len(query)<4:
#         params = {'msg': "Please make sure to enter relevant search query"}
    # return render(request, 'search.html', params)