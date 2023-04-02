from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderModelSerializer
from .forms import OrderForm
from cart.cart import Cart


@login_required()
def order_create_view(request):
    order_form = OrderForm()
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, _('You can not proceed to checkout page because your cart is empty.'))
        return redirect('product_list')

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order_obj = order_form.save(commit=False)
            order_obj.user = request.user
            order_obj.save()

            for item in cart:
                product = item['product_obj']
                OrderItem.objects.create(
                    order=order_obj,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )

            cart.clear()

            request.user.first_name = order_obj.first_name
            request.user.last_name = order_obj.last_name
            request.user.save()

            messages.success(request, _('Your order has successfully placed.'))

    return render(request, 'orders/order_create.html', {
        'form': order_form
    })


class GetAllData(APIView):
    def get(self, request):
        query = Order.objects.all().order_by('-datetime_created')
        serializers = OrderModelSerializer(query, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def all_data(request):
    if request.method == 'GET':
        query = Order.objects.all().order_by('-datetime_created')
        serializer = OrderModelSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetIsPaidData(APIView):
    def get(self, request):
        query = Order.objects.filter(is_paid=True)
        serializer = OrderModelSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateData(APIView):
    def get(self, request, pk):
        query = Order.objects.get(pk=pk)
        serializer = OrderModelSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        query = Order.objects.get(pk=pk)
        serializer = OrderModelSerializer(query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostModelData(APIView):
    def post(self, request):
        serializer = OrderModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def set_data(request):
    if request.method == 'POST':
        serializer = OrderModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchData(APIView):
    def get(self, request):
        search = request.GET['name']
        query = Order.objects.filter(first_name__contains=search)
        serializer = OrderModelSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteData(APIView):
    def delete(self, request, pk):
        query = Order.objects.get(pk=pk)
        query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
