from api.models import User, Profile, Book, ReadingList, ReadingListItem
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('full_name', 'bio', 'image')
        
      
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(allow_null=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')
        

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('full_name', 'bio', 'image')
        
        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # These are claims, you can add custom claims
        token['full_name'] = user.profile.full_name
        token['username'] = user.username
        token['email'] = user.email
        token['bio'] = user.profile.bio
        token['image'] = str(user.profile.image)
        
        return token
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This email is already in use.")]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="This username is already taken.")]
    )
    
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'authors', 'genre', 'publication_date', 'description', 'book_file', 'cover_image', 'uploaded_by', 'created_at')
        read_only_fields = ('uploaded_by', 'created_at')
    
    def validate(self, data):
        # Ensure all required fields are present and not empty
        required_fields = ['title', 'authors', 'genre', 'publication_date', 'book_file', 'cover_image']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field: f"{field.replace('_', ' ').title()} is required."})
        return data
       
        
class ReadingListItemSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    book_details = BookSerializer(source='book', read_only=True)
    
    class Meta:
        model = ReadingListItem
        fields = ('id', 'book', 'order', 'book_details')


class ReadingListSerializer(serializers.ModelSerializer):
    items = ReadingListItemSerializer(many=True, read_only=True)

    class Meta:
        model = ReadingList
        fields = ('id', 'name', 'user', 'created_at', 'items')
        read_only_fields = ('user', 'created_at')