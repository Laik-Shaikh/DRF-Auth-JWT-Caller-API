from rest_framework import serializers
from . models import RegisterUser, ContactList

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        # fields = "__all__"
        fields = ['name', 'phone_number', 'email', 'password']

        def validate_phone_number(self, data):
            if RegisterUser.objects.filter(phone_number = data['phone_number']).exists():
                raise serializers.ValidationError({'phone_number': 'Phone Number has already been taken.'})
                
            return data

class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactList
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=500)

