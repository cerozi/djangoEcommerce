from django import template
from ..models import Order

register = template.Library()


@register.simple_tag
def cart_quantity(user):
    if Order.objects.filter(user=user).exists():
        order = Order.objects.get(user=user)
        num_cart = 0
        for item in order.order_itens.all():
            num_cart += item.quantity

        return num_cart
    return 0