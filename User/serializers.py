from rest_framework import serializers
from .models import Snippets, CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=200)
#     body = serializers.CharField()
#     language = serializers.CharField(max_length=200)
#     created_at = serializers.DateTimeField()
#
#     def create(self, validated_data):
#         return Snippets.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.body = validated_data.get('body', instance.body)
#         instance.language = validated_data.get('language', instance.language)
#         instance.save()
#         return instance
#
# content = JSONRenderer().render(serializer.data)
# from django.utils.six import BytesIO
#
# stream = BytesIO(content)
# data = JSONParser().parse(stream)
# serializer = SnippetSerializer(data=data)
# serializer.is_valid()
# # True
# serializer.validated_data
# # OrderedDict([('title', ''), ('code', 'print "hello, world"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
# serializer.save()
# # <Snippet: Snippet object>

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippets
        fields = ('id', 'title', 'body', 'language')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'user_type', 'password')

    def create(self, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        user = get_user_model().objects.create(**validated_data)
        return user
