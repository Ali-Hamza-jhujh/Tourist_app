from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from tourism.models import Register, Text, TouristSpot, City, Hotel, Booking, Payment
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.timezone import now
import uuid
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage, send_mail
from xhtml2pdf import pisa
import qrcode
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import datetime
import base64
from io import BytesIO
from django.http import HttpResponse, JsonResponse
import barcode
from barcode.writer import ImageWriter
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def home_page(request):
    return render(request, 'home.htm')

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        father_name = request.POST.get("father_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            Register.objects.create(user=user, father_name=father_name, password=password, Username=username)
            messages.success(request, 'Account created successfully!')
            return redirect('login_page')
    return render(request, 'register.htm')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard_page')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.htm')

def logout_page(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login_page')

def about_page(request):
    return render(request, 'about.htm')

def contact_page(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        Text.objects.create(name=name, subject=subject, email=email, message=message)
        messages.success(request, 'Feedback added successfully!')
        return redirect('contact_page')
    return render(request, 'contact.htm')

def tourist_page(request):
    cities = City.objects.all()
    if request.method == "POST":
        city = get_object_or_404(City, id=request.POST.get("city"))
        TouristSpot.objects.create(
            name=request.POST.get("name"),
            yourname=request.POST.get("yourname"),
            city=city,
            image=request.FILES.get("image"),
            extra_details=request.POST.get("extra_details"),
            location_url=request.POST.get("location_url")
        )
        messages.success(request, "Spot added successfully.")
        return redirect('tourist_page')
    return render(request, 'tourist.htm', {'cities': cities})

def galary_page(request):
    spots = TouristSpot.objects.filter(city__isnull=False).order_by('city__city', 'name')
    return render(request, 'galary.htm', {'spots': spots})

def dashboard_page(request):
    cities = [
        {'id': 4,'name': 'Lahore', 'image': 'images/lahore.jpg', 'url': '/lahore/'},
        {'id': 2,'name': 'Islamabad', 'image': 'images/islamabad.jpg', 'url': '/islamabad/'},
        {'id': 3,'name': 'Hunza', 'image': 'images/hunza.jpg', 'url': '/hunza/'},
        {'id': 5,'name': 'Karachi', 'image': 'images/karachi.jpg', 'url': '/karachi/'},
        {'id': 9,'name': 'Skardu', 'image': 'images/skardu.jpg', 'url': '/skardu/'},
        {'id': 7,'name': 'Kashmir', 'image': 'images/kashmir.jpg', 'url': '/kashmir/'},
        {'id': 17,'name': 'Murree', 'image': 'images/murree.jpg', 'url': '/murree/'},
        {'id': 10,'name': 'Swat', 'image': 'images/swat.jpg', 'url': '/swat/'},
        {'id': 6,'name': 'Naran', 'image': 'images/naran.jpg', 'url': '/naran/'},
        {'id': 8,'name': 'Kaghan', 'image': 'images/kaghan.jpg', 'url': '/kaghan/'},
        {'id': 14,'name': 'Gilgit', 'image': 'images/gilgit.jpg', 'url': '/gilgit/'},
        {'id': 18,'name': 'Multan', 'image': 'images/multan.jpg', 'url': '/multan/'},
        {'id': 13,'name': 'Peshawar', 'image': 'images/peshawar.jpg', 'url': '/peshawar/'},
        {'id': 12,'name': 'Quetta', 'image': 'images/quetta.jpg', 'url': '/quetta/'},
        {'id': 11,'name': 'Shigar', 'image': 'images/shigar.jpg', 'url': '/shigar/'},
        {'id': 19,'name': 'Bahawalpur', 'image': 'images/bahawalpur.jpg', 'url': '/bahawalpur/'},
    ]
    return render(request,'dashboard.htm',{'cities':cities})

def card_page(request, city_id):
    city = get_object_or_404(City, id=city_id)
    info_page_urls = {
        'Lahore': '/lahore/',
        'Islamabad': '/islamabad/',
        'Karachi': '/karachi/',
        'Skardu': '/skardu/',
        'Murree': '/murree/',
        'Swat': '/swat/',
        'Naran': '/naran/',
        'Kaghan': '/kaghan/',
        'Hunza': '/hunza/',
        'Gilgit': '/gilgit/',
        'Multan': '/multan/',
        'Quetta': '/quetta/',
        'Bahawalpur': '/bahawalpur/',
        'Peshawar': '/peshawar/',
        'Shigar': '/shigar/',
        'Kashmir': '/kashmir/',
    }
    visit_url = info_page_urls.get(city.city.strip().title(), '/')
    return render(request, 'card.htm', {
        'city': city,
        'visit_url': visit_url,
        'hotel_url': reverse('hostel_view', kwargs={'city_id': city.id})
    })

def hostel_page(request):
    cities = City.objects.all()
    if request.method == 'POST':
        name = request.POST.get("name")
        city = get_object_or_404(City, id=request.POST.get("city"))
        city_id = request.POST.get("city")
        number = request.POST.get("number")
        contact = request.POST.get("contact")
        description = request.POST.get("description")
        price = request.POST.get("price")
        location_url = request.POST.get("location_url")
        image = request.FILES.get("image")
        hostel = Hotel.objects.create(name=name,
                                      city=city,
                                      number=number,
                                      contact=contact,
                                      description=description,
                                      price=price,
                                      location_url=location_url,
                                      image=image)
        hostel.save()
        messages.success(request,'Hostel detail added successfully!')
        return redirect('hostel_view', city_id=city_id)
    return render(request,'hostel.htm', {'cities': cities})

def hostel_view(request, city_id):
    city = get_object_or_404(City, id=city_id)
    hotels = Hotel.objects.filter(city_id=city_id)
    return render(request,'hostel_list.htm', {'city': city, 'hotels': hotels})

def islamabad_page(request):
    return render(request,'islamabad.htm')

def lahore_page(request):
    return render(request,'lahore.htm')

from django.views.decorators.http import require_http_methods
@login_required
def booking_page(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == "POST":
        try:
            quantity = max(1, int(request.POST.get('quantity', 1)))
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity.")
            return redirect('booking_page', hotel_id=hotel_id)
        price_at_booking = hotel.price
        subtotal = quantity * price_at_booking
        trx_id = request.session.get('last_transaction_id') or str(uuid.uuid4())[:10]
        request.session['last_transaction_id'] = trx_id
        existing_booking = Booking.objects.filter(user=request.user, hotel=hotel, trx_id=trx_id).first()
        if existing_booking:
            existing_booking.quantity += quantity
            existing_booking.subtotal = existing_booking.price * existing_booking.quantity
            existing_booking.save()
        else:
            Booking.objects.create(
                user=request.user,
                hotel=hotel,
                city=hotel.city,
                price=price_at_booking,
                quantity=quantity,
                subtotal=subtotal,
                trx_id=trx_id
            )
        cart = request.session.get('cart')
        if not isinstance(cart, list):
            cart = []
        hotel_found = False
        for item in cart:
            if isinstance(item, dict) and item.get('hotel_id') == hotel.id:
                item['quantity'] = quantity
                hotel_found = True
                break
        if not hotel_found:
            cart.append({'hotel_id': hotel.id, 'quantity': quantity})
        request.session['cart'] = cart
        messages.success(request, "Hotel booking added to your cart.")
        return redirect('booking_cart_page')
    return render(request, 'booking_form.htm', {"hotel": hotel})

@login_required
def booking_cart_page(request):
    cart = request.session.get('cart', [])
    trx_id = request.session.get('last_transaction_id')
    hotels_with_qty = []
    for item in cart:
        if isinstance(item, dict) and 'hotel_id' in item and 'quantity' in item:
            try:
                hotel = get_object_or_404(Hotel, id=item['hotel_id'])
                hotels_with_qty.append((hotel, item['quantity']))
            except Hotel.DoesNotExist:
                continue  
    return render(request, 'booking_cart.htm', {
        "hotels_with_qty": hotels_with_qty,
        "trx_id": trx_id,
        "city_id": hotels_with_qty[0][0].city.id if hotels_with_qty else None
    })

@login_required
def delete_page(request, booking_id):
    booking = Booking.objects.filter(hotel_id=booking_id, user=request.user).last()
    if booking:
        cart = request.session.get('cart', [])
        cart = [item for item in cart if isinstance(item, dict) and item.get('hotel_id') != booking.hotel_id]
        request.session['cart'] = cart
        booking.delete()
        messages.success(request, "Booking removed from your cart.")
    else:
        messages.error(request, "Booking not found.")
    return redirect("booking_cart_page")

@login_required
def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'initial.htm')

    elif request.method == "POST":
        user = request.user
        payment_method = request.POST.get('payment_method')
        trx_id = request.session.get('last_transaction_id')

        if not trx_id:
            messages.error(request, "Transaction session expired. Please retry.")
            return redirect('booking_cart_page')

        bookings = Booking.objects.filter(user=user, trx_id=trx_id)
        if not bookings.exists():
            messages.error(request, "Transaction ID is incorrect for this payment.")
            return redirect('initiate_payment')

        total_amount = sum(float(b.subtotal or 0) for b in bookings)
        if total_amount == 0:
            messages.error(request, "Your booking total is zero. Please check your cart.")
            return redirect('booking_cart_page')

        if payment_method == 'easypaisa':
            ep_number = request.POST.get('ep_number')
            ep_trx = request.POST.get('ep_trx')
            if not ep_number or not ep_trx:
                messages.error(request, "Please fill all EasyPaisa fields.")
                return redirect('initiate_payment')

            payment = Payment.objects.create(
                user=user,
                method='easypaisa',
                amount=total_amount,
                mobile_number=ep_number,
                trx_id=ep_trx
            )
            request.session['last_transaction_id'] = ep_trx
            return redirect('payment_receipt', payment_id=payment.id)

        elif payment_method == 'jazzcash':
            jc_number = request.POST.get('jc_number')
            jc_trx = request.POST.get('jc_trx')
            if not jc_number or not jc_trx:
                messages.error(request, "Please fill all JazzCash fields.")
                return redirect('initiate_payment')

            payment = Payment.objects.create(
                user=user,
                method='jazzcash',
                amount=total_amount,
                mobile_number=jc_number,
                trx_id=jc_trx
            )
            request.session['last_transaction_id'] = jc_trx
            return redirect('payment_receipt', payment_id=payment.id)

        elif payment_method == 'card':
            try:
                stripe_amount = int(total_amount * 100)  # Convert PKR to paisa
                if stripe_amount <= 0:
                    messages.error(request, "Your booking total is zero. Please check your cart.")
                    return redirect('booking_cart_page')

                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'pkr',
                            'unit_amount': stripe_amount,
                            'product_data': {
                                'name': 'Tour Booking',
                            },
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/stripe/success/'),
                    cancel_url=request.build_absolute_uri('/stripe/cancel/'),
                )

                return render(request, 'initial.htm', {
                    'session_id': session.id,
                    'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
                })
            except Exception as e:
                messages.error(request, f"Stripe error: {str(e)}")
                return redirect('initiate_payment')

        else:
            messages.error(request, "Invalid payment method.")
            return redirect('initiate_payment')

    return render(request, 'initial.htm')

def stripe_success(request):
    return render(request, 'payment_success.htm')

def stripe_cancel(request):
    return render(request, 'payment_failed.htm')

@login_required
def payment_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    trx_id = payment.trx_id
    bookings = Booking.objects.filter(user=request.user, trx_id=trx_id)
    total_amount = sum(float(b.subtotal or 0) for b in bookings)
    request.session.pop('last_transaction_id', None)
    send_mail(
        'Booking Payment Receipt',
        f'Thank you {request.user.username}, your payment of Rs {total_amount} via {payment.method} has been received.',
        'oalihamza8@gmail.com',
        [request.user.email],
        fail_silently=True,
    )
    return render(request, 'receipt.htm', {
        'payment': payment,
        'total_amount': total_amount,
        'trx_id': trx_id,
        'bookings': bookings
    })

@login_required
def clear_cart(request):
    request.session['cart'] = []
    messages.success(request, "Cart cleared.")
    return redirect('booking_cart_page')

@login_required
def generate_base64_qr_code(data):
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def generate_base64_barcode(data):
    buffer = BytesIO()
    code = barcode.get('code128', str(data), writer=ImageWriter())
    code.write(buffer)
    return base64.b64encode(buffer.getvalue()).decode()

def generate_base64_image(image_field):
    if image_field and hasattr(image_field, 'path'):
        with open(image_field.path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None

@login_required
def download_receipt(request, trx_id):
    bookings = Booking.objects.filter(user=request.user, trx_id=trx_id)
    if not bookings.exists():
        return HttpResponse("No bookings found for this transaction ID.", status=404)
    total_amount = sum(b.subtotal for b in bookings)
    qr_data = f"Transaction: {trx_id} | User: {request.user.username} | Total: Rs {total_amount}"
    buffer = BytesIO()
    qrcode.make(qr_data).save(buffer, format="PNG")
    qr_image = base64.b64encode(buffer.getvalue()).decode()
    template = get_template('receipt_pdf_template.htm')
    html = template.render({
        'bookings': bookings,
        'user': request.user,
        'trx_id': trx_id,
        'qr_image': qr_image,
        'total_amount': total_amount
    })
    result = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)
    if pisa_status.err:
        return HttpResponse("Error generating receipt PDF.", status=500)
    email = EmailMessage(
        subject=f"Booking Receipt - {trx_id}",
        body=f"Thank you {request.user.username}, attached is your receipt.",
        from_email="oalihamza@gamil.com",
        to=[request.user.email],
    )
    email.attach(f"receipt_{trx_id}.pdf", result.getvalue(), "application/pdf")
    email.send(fail_silently=False)
    return HttpResponse(result.getvalue(), content_type='application/pdf')

@login_required
def receipt_preview(request, trx_id):
    bookings = Booking.objects.filter(user=request.user, trx_id=trx_id)
    if not bookings.exists():
        return HttpResponse("No bookings found for this transaction ID.", status=404)
    total_amount = sum(float(b.subtotal or 0) for b in bookings)
    qr_data = f"Transaction: {trx_id} | User: {request.user.username} | Total: Rs {total_amount}"
    qr = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_image = base64.b64encode(qr_buffer.getvalue()).decode()
    barcode_buffer = BytesIO()
    barcode_obj = barcode.get('code128', trx_id, writer=ImageWriter())
    barcode_obj.write(barcode_buffer)
    barcode_image = base64.b64encode(barcode_buffer.getvalue()).decode()
    return render(request, 'receipt.htm', {
        'bookings': bookings,
        'trx_id': trx_id,
        'user': request.user,
        'qr_image': qr_image,
        'barcode_image': barcode_image,
        'total_amount': total_amount,
        'now': now()
    })

@staff_member_required
def admin_transactions(request):
    payments = Payment.objects.all().order_by('-timestamp')
    users = User.objects.all()
    method = request.GET.get('method')
    user_id = request.GET.get('user')
    trx_id = request.GET.get('trx_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if method:
        payments = payments.filter(method=method)
    if user_id:
        payments = payments.filter(user_id=user_id)
    if trx_id:
        payments = payments.filter(trx_id__icontains=trx_id)
    if start_date:
        payments = payments.filter(timestamp__date__gte=start_date)
    if end_date:
        payments = payments.filter(timestamp__date__lte=end_date)
    return render(request, 'transactions.htm', {
        'payments': payments,
        'users': users,
    })

def start_card_payment(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required.'}, status=403)
    user = request.user
    trx_id = request.session.get('last_transaction_id')
    if not trx_id:
        return JsonResponse({'error': 'Transaction session expired. Please retry.'}, status=400)
    bookings = Booking.objects.filter(user=user, trx_id=trx_id)
    if not bookings.exists():
        return JsonResponse({'error': 'No valid bookings found.'}, status=400)
    try:
        total_amount = sum(float(b.subtotal or 0) for b in bookings)
        stripe_amount = int(total_amount * 100)  # Convert PKR to paisa
        if stripe_amount <= 0:
            return JsonResponse({'error': 'Total amount is zero.'}, status=400)
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'pkr',
                    'unit_amount': stripe_amount,
                    'product_data': {
                        'name': 'Tour Booking',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/stripe/success/'),
            cancel_url=request.build_absolute_uri('/stripe/cancel/'),
        )
        return JsonResponse({
            'session_id': session.id,
            'public_key': settings.STRIPE_PUBLISHABLE_KEY
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
def karachi_page(request):
    return render(request, 'karachi.htm')

def peshawar_page(request):
    return render(request, 'peshawar.htm')

def quetta_page(request):
    return render(request, 'quetta.htm')

def gilgit_page(request):
    return render(request, 'gilgit.htm')

def skardu_page(request):
    return render(request, 'skardu.htm')

def hunza_page(request):
    return render(request, 'hunza.htm')

def murree_page(request):
    return render(request, 'murree.htm')

def swat_page(request):
    return render(request, 'swat.htm')

def multan_page(request):
    return render(request, 'multan.htm')
def bahawalpur_page(request):
    return render(request, 'bahawalpur.htm')
def kashmir_page(request):
    return render(request,'kashmir.htm')
def naran_page(request):
    return render(request, 'naran.htm')

def kaghan_page(request):
    return render(request, 'kaghan.htm')

def shigar_page(request):
    return render(request, 'shigar.htm')

def chatbot_page(request):
    return render(request, 'chatbot.htm')

import json
from django.http import JsonResponse
import requests
import os
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY") 

def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message", "")

            # Call Hugging Face Inference API
            headers = {"Authorization": f"Bearer {HF_API_KEY}"}
            payload = {
                "inputs": message,
            }
            response = requests.post(
                "https://api-inference.huggingface.co/models/gpt2",
                headers=headers,
                json=payload,
            )
            result = response.json()

            # Extract generated text
            if isinstance(result, list) and "generated_text" in result[0]:
                reply = result[0]["generated_text"]
            else:
                reply = "Sorry, I couldn't generate a reply."

            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"reply": f"Error: {e}"})
    else:
        return JsonResponse({"reply": "POST method required"}, status=405)




from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Message
import json

@login_required
def chat_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, "chat_list.htm", {"users": users})

@login_required
def chat_page(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by("timestamp")
    return render(request, "chat.htm", {"receiver": receiver, "messages": messages})

# API for sending message
@login_required
def send_message(request):
    if request.method == "POST":
        content = request.POST.get("content")
        receiver_id = request.POST.get("receiver_id")
        receiver = get_object_or_404(User, id=receiver_id)

        msg = Message.objects.create(sender=request.user, receiver=receiver, content=content)

        return JsonResponse({
            "id": msg.id,
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp.strftime("%H:%M")
        })

@csrf_exempt
def edit_message(request, pk):
    if request.method == "POST":
        data = json.loads(request.body)
        msg = Message.objects.get(pk=pk)
        if request.user == msg.sender and not msg.deleted:
            msg.content = data.get("content")
            msg.edited = True
            msg.save()
            return JsonResponse({"status": "success", "content": msg.content, "edited": True})
    return JsonResponse({"status": "error"})

@csrf_exempt
def delete_message(request, pk):
    if request.method == "POST":
        msg = Message.objects.get(pk=pk)
        if request.user == msg.sender:
            msg.deleted = True
            msg.content = "This message was deleted"
            msg.save()
            return JsonResponse({"status": "success", "deleted": True})
    return JsonResponse({"status": "error"})
        
from django.http import JsonResponse
from django.utils import timezone

def fetch_messages(request, receiver_id):
    messages = Message.objects.filter(
        sender__in=[request.user.id, receiver_id],
        receiver__in=[request.user.id, receiver_id]
    ).order_by("timestamp")

    return JsonResponse([m.serialize() for m in messages], safe=False)