from django.utils.deprecation import MiddlewareMixin
from jose import jwt
from django.shortcuts import render , redirect
from typing import Optional
from datetime import datetime, timedelta
import pytz

IST = pytz.timezone('Asia/Kolkata')
SECRET_KEY_JWT = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"


class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # This method is called before the view
        # You can modify the request here
        print('Entered Request')
        try:
            token = request.COOKIES.get('access_token')
            if token is None and request.path != '/login':
                return redirect('login-page')
            else:
                payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=[ALGORITHM])
                print('token verified !')
        except jwt.ExpiredSignatureError:
            print('token expired !')
            if request.path != '/login':
                return redirect('login-page')

        return None

    def process_response(self, request, response):
        # This method is called after the view
        # You can modify the response here
        print('Exiting Request')
        return response



