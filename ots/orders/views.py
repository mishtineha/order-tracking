from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Orders, OrderItem
from rest_framework.response import Response
from .serializers import OrderSerializer, ItemSerializer
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


class OrderAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        """

        :param request:
        :return: all orders data
        if user is admin then view all orders
        else view orders only created by the user
        """
        if request.user.profile.is_admin:
            orders = Orders.objects.all().prefetch_related('order_items').all()
        else:
            orders = Orders.objects.filter(user=request.user.profile).prefetch_related('order_items').all()
        data = OrderSerializer(orders, many=True).data
        return Response({'data': data})


    def post(self, request):
        """

        :param request:
        :return: a message if order is created or not
        new orders are created
        """
        data = request.data.get('data')
        data['user'] = request.user.profile.id
        data["status"]= Orders.CONFIRMED
        data['order_number'] = str(datetime.timestamp(datetime.now())).replace(".", "")+str(request.user.profile.id)+str(len(data['items']))
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            order = serializer.save()
            return Response({'order_number': order.order_number,
                             "status":"created"}, status=201)
        return Response(serializer.errors)

    def patch(self,request):
        """

        :param request: order_item_id, status
        :return:
        only admin has permission to update order, normal user can not update it after placing an order.
        only status update is allowed
        and only for line items
        """
        if request.user.profile.is_admin:
            try:
                order_item = OrderItem.objects.get(id=request.data.get('order_item_id'))
            except ObjectDoesNotExist:
                return Response({'message':'invalid item id'})
            serializer = ItemSerializer(instance=order_item, data=request.data, partial=True)
            if serializer.is_valid():
                item = serializer.save()
                return Response({'order_item_id': item.id,
                                 'status': 'updated'})
            return Response(serializer.errors)
        return Response({'message':'user has no permission'},status=401)


class OrderUser(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        """

        :param request:
        :param pk: primary key of profile table
        :return: all orders of a user
        only admin can view others orders
        """
        if request.user.profile.is_admin:
            orders = Orders.objects.filter(user__id=pk).prefetch_related('order_items').all()
            data = OrderSerializer(orders, many=True).data
            return Response({'data': data})
        return Response({'message': 'user has no permission to view others orders'},status=401)


class OrderStore(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk):
        """

        :param request:
        :param pk: primary key of profile table
        :return: all orders of a user
        only admin can view others orders
        """
        if request.user.profile.is_admin:
            orders = Orders.objects.filter(store__id=pk).prefetch_related('order_items').all()
            data = OrderSerializer(orders, many=True).data
            return Response({'data': data})
        return Response({'message': 'user has no permission to view others orders'}, status=401)












# Create your views here.
