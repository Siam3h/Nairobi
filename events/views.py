import json
from django import forms
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Event, Blog, CartItem, Profile
from .forms import CreateUserForm, LoginForm, BlogForm, EventForm, SearchForm
from django.shortcuts import render, redirect


class HomePageView(TemplateView):
    template_name = 'events/homepage.html'
    def get_context_data(self, **kwargs):
        events = Event.objects.filter(is_published=True)
        context = {'events': events}
        return context

class EventsPageView(TemplateView):
    template_name = 'events/events.html'
    def get_context_data(self, **kwargs):
        events = Event.objects.filter(is_published=True).order_by('-pub_date')
        context = {'events': events}
        return context
    
def event_single(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'events/event_single.html', {'event': event})


class AboutPageView(TemplateView):
    template_name = 'events/about.html'

class ContactPageView(TemplateView):
    template_name = 'events/contact.html'

class PrivacyPolicyPageView(TemplateView):
    template_name = 'events/policy.html'

class BlogPageView(TemplateView):
    template_name = 'events/blog.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_blogs = Blog.objects.all()
        context['latest_blogs'] = all_blogs.filter(category='latest').order_by('-pub_date')
        context['upcoming_events'] = all_blogs.filter(category='upcoming').order_by('-pub_date')
        context['tech_entertainment'] = all_blogs.filter(category='tech').order_by('-pub_date')
        context['past_event_reviews'] = all_blogs.filter(category='reviews').order_by('-pub_date')
        context['artists_corner'] = all_blogs.filter(category='artists').order_by('-pub_date')
        return context    

class SinglePostView(TemplateView):
    template_name = 'events/singlePost.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = kwargs['blog_id']
        blog = get_object_or_404(Blog, id=blog_id)
        category = blog.category
        next_post = Blog.objects.filter(category=category, pub_date__gt=blog.pub_date).order_by('pub_date').first()
        prev_post = Blog.objects.filter(category=category, pub_date__lt=blog.pub_date).order_by('-pub_date').first()
        latest_blogs = Blog.objects.exclude(id=blog.id).order_by('-pub_date')[:5]  
        context.update({
            'blog': blog,
            'next_post': next_post,
            'prev_post': prev_post,
            'latest_blogs': latest_blogs,
            'author_id': blog.author.id,
        })
        
        return context


class CheckOutPageView(TemplateView):
    template_name = 'events/checkout.html'

class PaymentPageView(TemplateView):
    template_name = 'events/payment.html'


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateUserForm
from .models import Profile

# views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateUserForm
from .models import Profile

# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateUserForm
from .models import Profile

# views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateUserForm
from .models import Profile

# views.py
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.gender = form.cleaned_data.get('gender')
            user.save()
            func = form.cleaned_data.get('func')
            profile = Profile.objects.create(user=user, func=func)
            return redirect(reverse("events:login"))
    else:
        form = CreateUserForm()
    context = {'registerform': form}
    return render(request, 'events/register.html', context=context)



from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import LoginForm  # Import your LoginForm here

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import LoginForm  # Import your LoginForm here

def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("events:profile"))
    context = {'loginform': form}
    return render(request, 'events/login.html', context=context)

@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse("events:login"))

@login_required
def profile(request):
    user = request.user
    blogs = Blog.objects.filter(author=user)
    events = Event.objects.filter(organizer=user)

    context = {
        'user': user,
        'blogs': blogs,
        'events': events,
        'profile':profile,
    }
    return render(request, 'events/profile.html', context)


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('events:profile'))  # Redirect to a success page
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'events/profile_update.html', {'form': form})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect("/blogs/")
    else:
        form = BlogForm()
    return render(request, 'events/create_blog.html', {'form': form})

@login_required
def update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user == blog.author:
        if request.method == 'POST':
            form = BlogForm(request.POST, instance=blog)
            if form.is_valid():
                form.save()
                return redirect("/blogs/")
        else:
            form = BlogForm(instance=blog)
        return render(request, 'events/update_blog.html/', {'form': form})
    else:
       return redirect(reverse("events:login"))

@login_required
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user == blog.author:
        blog.delete()
        return redirect("/blogs/")
    else:
       return redirect(reverse("events:login"))

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect("/events/")
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user == event.organizer:
        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('/events/')
        else:
            form = EventForm(instance=event)
        return render(request, 'events/update_event.html', {'form': form})
    else:
       return redirect(reverse("events:login"))

@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user == event.organizer:
        event.delete()
        return redirect('/events/')
    else:
        return redirect(reverse("events:login"))

def search(request):
    form = SearchForm(request.GET)
    query = None
    users = events = blogs = None

    if form.is_valid():
        query = form.cleaned_data.get('query')
        users = User.objects.filter(username__icontains=query)
        events = Event.objects.filter(
            Q(title__icontains=query) |
            Q(organizer__username__icontains=query)  
        )
        blogs = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query)  
        )

    context = {
        'form': form,
        'query': query,
        'users': users,
        'events': events,
        'blogs': blogs
    }
    
    if users.exists():
        for user in users:
            user_blogs = Blog.objects.filter(author=user)
            context['user_blogs'] = user_blogs
            break

    return render(request, 'events/search_results.html', context)


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'events/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = Event.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('events:events')

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('events:view_cart')

def removeone_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total_price = cart_item.quantity * cart_item.product.price
        cart_item.save()
    else:
        cart_item.delete()
    return redirect(reverse('events:checkout'))


from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from .models import CartItem
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import CartItem

class CheckoutView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        mpesa_number = data.get('mpesa_number')
        total_price = data.get('total_price')

        result = self.lipa_na_mpesa_online(mpesa_number, total_price)
        
        if result == 'success':
            
            return JsonResponse({'success': True})
        
        else:
            return JsonResponse({'success': False, 'error': result}, status=400)
    

    def get(self, request):
        cart_items = CartItem.objects.all()
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        serialized_cart_items = [
            {
                'product_title': item.product.title,
                'quantity': item.quantity,
                'price': item.product.price
            }
            for item in cart_items
        ]
        

        context = {
            'cart_items': serialized_cart_items,
            'total_price': total_price,
        }
        return render(request, 'events/checkout.html', context)

    
def receipt(request, event_id):
    try:
        event_id = int(event_id)
    except ValueError:
        # Handle the case where event_id is not a valid integer
        # You may want to log this or render an error page
        return HttpResponse("Invalid event ID")

    event = get_object_or_404(Event, pk=event_id)
    
    return render(request, 'events/pdf.html', {'event': event, 'event_id': event_id})

    



from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from .models import Event  # Assuming your Event model is defined in the same app

import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from .models import Event

import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib import colors
from django.http import HttpResponse
from .models import Event

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse
from .models import Event

def generate_receipt_pdf(request, event_id):
    # Retrieve the event object
    event = Event.objects.get(pk=event_id)

    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{event.title}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    styles = getSampleStyleSheet()

    # Content for the PDF
    content = []

    # Add title
    title = Paragraph(f'<b>{event.title}</b>', styles['Title'])
    content.append(title)
    content.append(Paragraph("<br/><br/>", styles['Normal']))  # Add spacing

    # Add details
    details = [
        ['Date', str(event.date)],
        ['Time', str(event.time)],
        ['Location', event.location],
    ]

    for detail in details:
        detail_title = detail[0]
        detail_value = detail[1]
        detail_paragraph = Paragraph(f'<b>{detail_title}:</b> {detail_value}', styles['Normal'])
        content.append(detail_paragraph)

    content.append(Paragraph("<br/><br/>", styles['Normal']))  # Add spacing

    # Generate QR code with event details
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=4,
    )
    qr_data = f"Event: {event.title}\nLocation: {event.location}\nDate: {event.date}\nTime: {event.time}"
    qr.add_data(qr_data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img_buffer = BytesIO()
    qr_img.save(qr_img_buffer)
    qr_img_buffer.seek(0)

    qr_image = qr_img_buffer.getvalue()
    qr_image = Image(BytesIO(qr_image))
    qr_image.width = 80
    qr_image.height = 80
    content.append(qr_image)

    # Add price
    price = Paragraph(f'<b>Total Price: ${event.price}</b>', styles['Normal'])
    content.append(price)
    content.append(Paragraph("<br/><br/>", styles['Normal']))  # Add spacing

    # Add contact email
    contact_email = Paragraph(f'<b>Contact Email:</b> {event.contact_email}', styles['Normal'])
    content.append(contact_email)

    doc.build(content)

    return response


    

  




# views.py
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from .models import Blog

class AuthorProfileView(TemplateView):
    template_name = 'events/author_profile.html'

    def get_context_data(self, **kwargs):
        author_id = kwargs['author_id']
        author = get_object_or_404(User, pk=author_id)
        posts = Blog.objects.filter(author=author)
        categories = posts.values_list('category', flat=True).distinct()
        total_posts = posts.count()

        context = {
            'author': author,
            'total_posts': total_posts,
            'categories': categories,
        }
        return context
