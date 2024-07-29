from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from rest_framework.validators import ValidationError

class RegisterSerializer(serializers.ModelSerializer) : 
    class Meta:
        model = User
        fields = ['full_name','email','password']

    def save (self):
        self.user = User.objects.create_user(**self.validated_data)
        return self.user
    
    def to_representation(self, instance):
        tokens = RefreshToken.for_user(user=self.user)
        data = {
            'refresh_token' : str(tokens),
            'access_token' : str(tokens.access_token),
        }
        return data
    

class LoginSerializer (serializers.Serializer) :
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        try :
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({
                'message' : 'invalid email'
            })
        
        if not self.user.check_password(password) : 
            raise ValidationError({
                'message' : 'invalid password'
            })

        return attrs
    
    def to_representation(self, *args, **kwargs):
        tokens = RefreshToken.for_user(self.user)
        data = {
            'refresh_token' : str(tokens),
            'access_token' : str(tokens.access_token),
        }
        return data
    
    def save(self, **kwargs):...
