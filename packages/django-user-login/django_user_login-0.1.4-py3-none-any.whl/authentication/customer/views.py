from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Customer

@login_required
def homepage(request, username):
    if request.user.username != username:
        return HttpResponseRedirect(reverse('authentication:customer:homepage', args=[request.user.username]))
    
    try:
        customer = Customer.objects.get(user=request.user)
    except:
        return redirect('/')
    
    return render(
        request,
        'customer/homepage.html',
        {
            "customer": customer
        }
    )