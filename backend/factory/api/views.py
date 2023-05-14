import datetime

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from factory.api.serializers import FactorySerializers, FactoryMemberSerializers, ProductLineSerializers, \
    ProductLinePartSerializers, ShiftSerializers, ProductLinePart2Serializers, SettingsSerializers, \
    SettingsTypeSerializers
from factory.models import Factory, FactoryMember, Shift, ProductLine, ProductLinePart, ProductLinePart2, Settings, \
    SettingsType


class FactoryView(generics.ListCreateAPIView):
    queryset = Factory.objects.all()
    serializer_class = FactorySerializers
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        owner = self.request.query_params.get('owner')
        queryset = Factory.objects.filter(delete=None)
        if owner:
            queryset = queryset.filter(owner=owner)
        return queryset


class DetailFactoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Factory.objects.filter(delete=None)
    serializer_class = FactorySerializers
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        try:
            obj = Factory.objects.get(id=self.kwargs["id"])
            obj.delete = datetime.datetime.now()
            obj.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FactoryMemberView(generics.ListCreateAPIView):
    queryset = FactoryMember.objects.all()
    serializer_class = FactoryMemberSerializers
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        factory = self.request.query_params.get('factory')
        member = self.request.query_params.get('member')
        queryset = FactoryMember.objects.all()
        if factory:
            queryset = queryset.filter(factory=factory)
        if member:
            queryset = queryset.filter(member=member)
        return queryset


class DeleteFactoryMemberView(generics.RetrieveDestroyAPIView):
    queryset = FactoryMember.objects.all()
    serializer_class = FactoryMemberSerializers
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'


class ProductLineView(generics.ListCreateAPIView):
    queryset = ProductLine.objects.all()
    serializer_class = ProductLineSerializers
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        factory = self.request.query_params.get('factory')
        queryset = ProductLine.objects.all()
        if factory:
            queryset = queryset.filter(factory=factory)
        return queryset


class DetailProductLineView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductLine.objects.all()
    serializer_class = ProductLineSerializers
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'


class ProductLinePartView(generics.ListCreateAPIView):
    queryset = ProductLinePart.objects.all()
    serializer_class = ProductLinePartSerializers
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        product_line = self.request.query_params.get('product_line')
        factory = self.request.query_params.get('factory')
        queryset = ProductLinePart.objects.all()
        if product_line:
            queryset = queryset.filter(product_line=product_line)
        if factory:
            queryset = queryset.filter(product_line__factory=factory)
        return queryset


class DetailProductLinePart(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductLinePart.objects.all()
    serializer_class = ProductLinePartSerializers
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'


class ProductLinePart2View(generics.ListCreateAPIView):
    queryset = ProductLinePart2.objects.all()
    serializer_class = ProductLinePart2Serializers
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        product_line = self.request.query_params.get('product_line')
        factory = self.request.query_params.get('factory')
        queryset = ProductLinePart2.objects.all()
        if product_line:
            queryset = queryset.filter(product_line=product_line)
        if factory:
            queryset = queryset.filter(product_line__factory=factory)
        return queryset


class DetailProductLinePart2(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductLinePart2.objects.all()
    serializer_class = ProductLinePart2Serializers
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'


class ShiftView(generics.ListCreateAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializers
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        factory = self.request.query_params.get('factory')
        queryset = Shift.objects.all()
        if factory:
            queryset = queryset.filter(factory=factory)
        return queryset


class DetailShiftView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializers
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'


class SettingsView(generics.ListCreateAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializers
    permission_classes = [AllowAny, IsAuthenticated]

    def get_queryset(self):
        factory = self.request.query_params.get('factory')
        types = SettingsType.objects.all()
        queryset = Settings.objects.all()
        if factory:
            queryset = queryset.filter(factory=factory)
            queryset = queryset.order_by('-id')[:1]
        return queryset


class SettingsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializers
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'


class SettingsTypeView(generics.ListCreateAPIView):
    queryset = SettingsType.objects.all()
    serializer_class = SettingsTypeSerializers
    permission_classes = [AllowAny, IsAuthenticated]


class DetailSettingsTypeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SettingsType.objects.all()
    serializer_class = SettingsTypeSerializers
    permission_classes = [AllowAny, IsAuthenticated]
    lookup_field = 'id'
