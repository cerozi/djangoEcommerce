from audioop import add
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from main_app.forms import CheckoutForm
from .models import Address, Item, OrderItem, Order
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.



class HomeTemplate(ListView):
    model = Item
    template_name = 'home-page.html'
    paginate_by = 1


class ProductTemplate(DetailView):
    model = Item
    template_name = 'product-page.html'


class CartSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                order = Order.objects.get(user=self.request.user)
            except:
                order = None

        context = {
            'order': order
        }

        return render(self.request, 'order-summary.html', context=context)

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()

        context = {
            'form': form
        }

        return render(self.request, 'checkout-page.html', context=context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST)
        print('TESTE 1')
        
        if Order.objects.filter(user=self.request.user).exists():
            print('TESTE 2')
            if form.is_valid():
                print('TESTE 3')
                # creates variables for the data form
                street = form.cleaned_data['rua']
                district = form.cleaned_data['bairro']
                number = form.cleaned_data['num']
                complement = form.cleaned_data['complemento']
                
                order = Order.objects.get(user=self.request.user)


                address_qs = Address.objects.filter(street=street, 
                                        district=district, 
                                        number=number, 
                                       complement=complement)

                # checks if this address object already exists 
                # and if the order already has a relation with the address

                if address_qs.exists():
                    address = address_qs[0]
                    if not address.order_set.filter(user=self.request.user).exists():
                        address.order_set.add(order)
                else:
                    # creates Address model instance
                    print('MODEL SAVED')
                    address_instance = Address(
                        street=street,
                        district=district,
                        number=number,
                        complement=complement
                    )
                    # associates the order with the new address
                    address_instance.save()
                    order.address = address_instance
                    order.save()
            else:
                messages.warning(self.request, 'Formulário inválido. ')

        else:
            messages.warning(self.request, 'Você não tem nenhum pedido em andamento. ')

        return render(self.request, 'checkout-page.html')

@login_required
def addToCart(request, slug):
    item = Item.objects.get(slug=slug)
    order_item = OrderItem.objects.get_or_create(item=item, user=request.user)
    order_qs = Order.objects.filter(user=request.user)
    # checks if the user already has an order
    if order_qs.exists():
        order = order_qs[0]
        # checks if user already has the order item in order; if not, then add it
        if not order.order_itens.filter(item=item).exists():
            order.order_itens.add(order_item[0].pk)
            order.save()
    else:
        # creates a order for the user and includes the order item
        order_instance = Order(user=request.user)
        order_instance.save()
        order_instance.order_itens.add(order_item[0].pk)
        order_instance.save()

    # increases the item order quantity by 1
    order_item[0].quantity += 1
    order_item[0].save()

    # display updated quantity message
    messages.info(request, "Item adicionado do carrinho. ")

    return redirect(reverse('cart-summary'))

@login_required
def removeFromCart(request, slug):
    # check if the current user has an order
    order_qs = Order.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        # check if the current user has an item order
        item = Item.objects.get(slug=slug)
        if order.order_itens.filter(item=item).exists():
            # decrease the quantity of the item order
            item_order = order.order_itens.get(item=item)
            item_order.quantity -= 1
            item_order.save()

            # if there is 0 quantity, remove the item order from the user order
            if item_order.quantity == 0:
                item_order.delete()


            # display updated quantity message
            messages.info(request, "Item retirado do carrinho. ")
        
        else:
            # display message saying there is no item of that type
            messages.info(request, "Você não tem nenhum item deste tipo no carrinho. ")
    else:
        # display message saying there is no item of that type
        messages.info(request, "Você não tem nenhum pedido em andamento. ")

    return redirect(reverse('cart-summary'))

@login_required
def removeCart(request, slug):
    item = Item.objects.get(slug=slug)
    order = Order.objects.get(user=request.user)
    order_item = order.order_itens.all().get(item__slug=item.slug)
    order_item.delete()

    return redirect(reverse('cart-summary'))