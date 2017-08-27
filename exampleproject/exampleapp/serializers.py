from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers

from exampleapp.models import Article, Tag


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'email')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'text',)


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, allow_blank=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'tags', 'author')

    def validate_tags(self, tags_dict_list):
        tags_creators = []
        has_errors = False
        errors = []
        for tag_dict in tags_dict_list:
            if not tag_dict.get('id'):
                serializer = TagSerializer(data=tag_dict)
            else:
                instance = Tag.objects.get(id=tag_dict.get('id'))
                serializer = TagSerializer(instance, data=tag_dict)

            if serializer.is_valid():
                tags_creators.append(lambda: serializer.save())
                errors.append({})
            else:
                has_errors = True
                errors.append(serializer.errors)

        if has_errors:
            raise serializers.ValidationError(errors)

        return tags_creators

    def create(self, validated_data):
        tag_creators = validated_data.pop('tags', [])
        with transaction.atomic():
            tags = [tag_creator() for tag_creator in tag_creators]
            create_data = dict(
                validated_data,
                **{'user': self.context['request'].user}
            )
            article = super(ArticleSerializer, self).create(**create_data)
            article.tags.set(tags)
            return article

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        create_data = dict(
            validated_data,
            **{'user': self.context['request'].user}
        )
        for field_name in Article._meta.get_all_field_names():
            setattr(instance, field_name, create_data.get(field_name, getattr(instance, field_name)))

        instance.tags.set(tags)
        return instance