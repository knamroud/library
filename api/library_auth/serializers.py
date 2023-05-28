from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils.html import escape


class UserSerializer(serializers.ModelSerializer):
    is_librarian = serializers.SerializerMethodField(
        "get_is_librarian", read_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name",
                  "username", "email", "is_librarian")

    def get_is_librarian(self, obj):
        return obj.groups.filter(name='Librarian').exists()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if type(value) is str:
                data[key] = escape(value)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=10, validators=[
                                     UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=10)
    last_name = serializers.CharField(max_length=10)
    email = serializers.EmailField(validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    cpassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, attrs):
        if attrs["password"] != attrs["cpassword"]:
            raise serializers.ValidationError(
                {"password": "Passwords not matching."})
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )

        user.set_password(validated_data["password"])
        user.save()

        return user