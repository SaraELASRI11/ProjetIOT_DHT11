"""
from rest_framework.decorators import api_view

@api_view(["GET", "POST"])
def Dlist(request):
 if request.method == "GET":
     all_data = Dht11.objects.all()
     data_ser = DHT11serialize(all_data, many=True) # Les données sont sérialisées en JSON
     return Response(data_ser.data)
 elif request.method == "POST":
   serial = DHT11serialize(data=request.data)
 if serial.is_valid():
   serial.save()
   return Response(serial.data,status=status.HTTP_201_CREATED)
 else:
   return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)

from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import rest_framework
@api_view(['GET'])
def Dlist(request):
    all_data = Dht11.objects.all()
    data = DHT11serialize(all_data, many=True).data
    return Response({'data': data})

class Dhtviews(generics.CreateAPIView):

    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize
"""

from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import requests
# Définir la fonction pour envoyer des messages Telegram
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response
@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)

            if serial.is_valid():
                serial.save()
                derniere_temperature = Dht11.objects.last().temp
                print(derniere_temperature)

                if derniere_temperature > 23:
                    # Alert Email
                    subject = 'Alerte'
                    message = 'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['sara.elasri.24@ump.ac.ma']
                    send_mail(subject, message, email_from, recipient_list)

                    # Alert WhatsApp
                    account_sid = 'ACe5065958514f5cce666bdd69f02cc464'
                    auth_token = 'c16dfb5e0f081e529793dafd95fac2dd'
                    client = Client(account_sid, auth_token)
                    message_whatsapp = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body='La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation',
                        to='whatsapp:+212606432006'
                    )

                    # Alert Telegram
                    telegram_token = '7779251101:AAHi10scJN4p8rp1Jjmg8eyMGLzQSthPU0U'
                    chat_id = '7328625193'  # Remplacez par votre ID de chat
                    telegram_message = 'La température dépasse le seuil de 25°C, veuillez intervenir immédiatement pour vérifier et corriger cette situation'
                    send_telegram_message(telegram_token, chat_id, telegram_message)

                return Response(serial.data, status=status.HTTP_201_CREATED)

            else:
                return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)