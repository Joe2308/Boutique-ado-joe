from django.shortcuts import render, redirect, reverse, HttpResponse, HttpResponseRedirect, get_list_or_404, get_object_or_404
from .models import Product, UserProfile, Wishlist, WishlistItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
# @login_required


def wishlist(request):
    """
    A view to render the users wishlist
    """
    wishlist = None
    profile = get_object_or_404(UserProfile, user=request.user)
    try:
        wishlist = Wishlist.objects.get(user=profile)
    except Wishlist.DoesNotExist:
        pass

    context = {
        'wishlist': wishlist,
    }

    return render(request, 'my_wishlist/wishlist.html', context=context)


@login_required
def add_to_wishlist(request, product_id):
    """
    Add a product from the store to the
    wishlist for the logged in user
    """
    product = get_object_or_404(Product, pk=product_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    wishlist, created = Wishlist.objects.get_or_create(user=profile)
    # Add product to the wishlist
    if WishlistItem.objects.filter(product=product).exists():
        messages.error(request,'Product already in wishlist!')
        return redirect(reverse('product_detail', args=[product.id]))
    else:

        wishlist.products.add(product)
        messages.success(request, 'product added to wishlist')
        return redirect(reverse('product_detail', args=[product.id]))


@login_required
def remove_from_wishlist(request, product_id):
    """
    Add a product from the store to the
    wishlist for the logged in user
    """
    product = get_object_or_404(Product, pk=product_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    wishlist, created = Wishlist.objects.get_or_create(user=profile)
    wishlist.products.remove(product)
    messages.success(request, 'product removed from wishlist')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    wishlist_count = Wishlist.objects.filter(user=profile).count()
    if wishlist_count == 0:
        Wishlist.remove(wishlist=wishlist, user=profile)
        messages.success(request, 'All products removed from wishlist!')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


# def add_to_wishlist(request, product_id):
#     profile = get_object_or_404(UserProfile, user=request.user)

#     wishlist = Wishlist.objects.get(user=profile)
#     product = get_object_or_404(Product, pk=product_id)

#     add = WishListItem.objects.get_or_create(WishlistItem, product=product)

#     wishlist.products.add(add)

    
#     return redirect(reverse('product_detail', args=[product.id]))



# def add_to_wishlist(request, product_id):
#     """ A view to add an item in the Wishlist """
#     redirect_url = request.POST.get('redirect_url')

#     user = get_object_or_404(UserProfile, user=request.user)
#     wishlist = Wishlist.objects.get_or_create(user=user)
#     wishlist_user = wishlist[0]

#     product = Product.objects.get(pk=product_id)
#     if request.POST:
#         test = WishlistItem.objects.filter(
#             wishlist=wishlist_user, product=product).exists()
#         if test:
#             messages.error(
#                 request,
#                 "Product already in Wish List. Go to My Account to view Wish List")
#             return redirect(redirect_url)

#         else:
#             added_item = WishlistItem(
#                 wishlist=wishlist_user, product=product)
#             added_item.save()
#             messages.success(
#                 request,
#                 "Product added to Wish List. Go to My Account to view Wish List")
#             return redirect(redirect_url)
#     else:
#         messages.error(request, "Click 'Add to Wish List' to add an item ")
#         return render(request, 'home/index.html')
