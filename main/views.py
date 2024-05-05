from rest_framework.decorators import api_view
from jose import jwt
from django.shortcuts import render, redirect
from typing import Optional
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone('Asia/Kolkata')
SECRET_KEY_JWT = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"
import sys

from .forms import LoginForm

sys.path.append("..")

from vendor_profile_management.models import Vendor


# Create your views here.

@api_view(['GET'])
def home(request):
    try:
        token = request.COOKIES.get('access_token')
        if token is None:
            print('token absent')
            return redirect('login-page')
        else:
            payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
            print('token verified !')
    except jwt.ExpiredSignatureError:
        print('token expired !')
        return redirect('login-page')

    Vendors = Vendor.objects.filter()
    return render(request, 'home.html', {'Vendors': Vendors})


@api_view(['GET', 'POST'])
def login(request):
    loginform = LoginForm()

    try:
        token = request.COOKIES.get('access_token')
        if token is None:
            print('token absent')
        else:
            payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
            print('token verified !')
            return redirect('home-page')

    except jwt.ExpiredSignatureError:
        print('token expired !')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.data["password"] == 'password' and form.data["username"] == 'Admin':
            response = redirect('home-page')
            token_expires = timedelta(minutes=5)
            token = create_access_token(expires_delta=token_expires)
            response.set_cookie(key="access_token", value=token, httponly=True)
            print('token set successfully')
            return response
        else:
            print('wrong username or password')
            return render(request, 'login.html', {'form': loginform})
    else:
        return render(request, 'login.html', {'form': loginform})


def create_access_token(expires_delta: Optional[timedelta] = None):
    encode = {"sub": "Default_User"}
    if expires_delta:
        expire = datetime.now(IST) + expires_delta
    else:
        expire = datetime.now(IST) + timedelta(minutes=5)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY_JWT, algorithm=ALGORITHM)
