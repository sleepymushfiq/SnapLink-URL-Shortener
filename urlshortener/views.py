import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortenedURL
import random
import string

def generate_short_code():
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=6))
        if not ShortenedURL.objects.filter(short_code=code).exists():
            return code

def index(request):
    short_url = None
    qr_code = None  
    
    if request.method == "POST":
        original = request.POST.get('original_url')
        obj, created = ShortenedURL.objects.get_or_create(original_url=original)
        
        if created:
            obj.short_code = generate_short_code()
            obj.save()
        
        short_url = request.build_absolute_uri('/') + obj.short_code
        
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(short_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code = base64.b64encode(buffer.getvalue()).decode()
         
        print("QR Code successfully generated!") 

    return render(request, 'urlshortener/index.html', {
        'short_url': short_url,
        'qr_code': qr_code
    })

def redirect_to_original(request, code):
    url_entry = get_object_or_404(ShortenedURL, short_code=code)
    url_entry.clicks += 1
    url_entry.save()
    return redirect(url_entry.original_url)
def analytics(request):
    
    all_urls = ShortenedURL.objects.all().order_by('-created_at')
    return render(request, 'urlshortener/analytics.html', {'all_urls': all_urls})