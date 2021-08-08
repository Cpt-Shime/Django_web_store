from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render


from store.models import Product
from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket': basket})

# funckcija za dodat u kosaricu
def basket_add(request):
    basket = Basket(request)  # uzmi session data
    if request.POST.get('action') == 'post': 

        # uzmimo product id i product qty u int iz requesta, productid iz single htmla ajax proslijedujemo
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))

        #uzmi product ili error 
        product = get_object_or_404(Product, id=product_id)
        #dodaj u basket product i produkt quantity
        basket.add(product=product, qty=product_qty)

        # pozovi funkciju za izracunat sumu item qty u koasrici
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        # vrati json resposne kolicine 
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
