from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents
import stripe


# Create your views here.
def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There is nothing in your bag at the moment")
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_live_51JfVnHIDWRo1ggapt5AvHsFCy4xcmT9kCgs83qtZxI1HZA85dwIsBJn6dAC613sQKHiXJVWO4zEOJdVcBLGkWbGd00AQ34xmzs',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)

