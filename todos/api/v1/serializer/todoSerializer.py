import base64, uuid
import datetime

from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import serializers

from users.models import User
from ....models import Todo


# https://gist.github.com/yprez/7704036
# Custom image field - handles base 64 encoded images
class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            # base64 encoded image - decode
            format, imgstr = data.split(';base64,')  # format ~= data:image/X,
            ext = format.split('/')[-1]  # guess file extension
            id = uuid.uuid4()
            data = ContentFile(base64.b64decode(imgstr), name=id.urn[9:] + '.' + ext)
        return super(Base64ImageField, self).to_internal_value(data)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class TodoItemsSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    image = Base64ImageField()
    deadline = serializers.DateTimeField()
    days_left = serializers.SerializerMethodField('calculate_days')  # gets the number of days remaining to reach deadline

    class Meta:
        model = Todo
        fields = ['id', 'name', 'description', 'image', 'deadline', 'creation_date', 'days_left', 'author']
        read_only_fields = ['id', 'creation_date', 'days_left']
        extra_kwargs = {'description': {'required': False},}



    def calculate_days(self, instance):
        return (instance.deadline - timezone.now()).days

    def validate(self, attrs):
        if self.context['method'] not in ['update', 'partial_update']:
            if attrs['name'] in Todo.objects.all().values_list('name', flat=True):
                raise serializers.ValidationError({"message": "Todo with this name already exists."})
        if 'deadline' in attrs.keys():
            if attrs['deadline'] < timezone.now():
                raise serializers.ValidationError({"message": "Todo deadline isn't valid. This date has already passed."})
        return attrs

    def to_representation(self, instance):
        return super().to_representation(instance)
