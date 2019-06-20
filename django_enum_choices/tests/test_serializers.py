from django.test import TestCase

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django_enum_choices.serializers import EnumChoiceField
from .testapp.models import StringEnumeratedModel
from .testapp.enumerations import IntTestEnum, CharTestEnum


class TestSerializerField(TestCase):
    def test_to_representation_returns_primitive_int_value(self):
        field = EnumChoiceField(enum_class=IntTestEnum)

        result = field.to_representation(IntTestEnum.FIRST)

        self.assertEqual(result, 1)

    def test_to_representation_returns_primitive_string_value(self):
        field = EnumChoiceField(enum_class=CharTestEnum)

        result = field.to_representation(CharTestEnum.FIRST)

        self.assertEqual(result, 'first')

    def test_to_internal_value_fails_when_value_not_in_enum_class(self):
        failing_value = 5
        field = EnumChoiceField(enum_class=IntTestEnum)

        with self.assertRaisesMessage(
            ValidationError,
            'Key 5 is not a valid IntTestEnum'
        ):
            field.to_internal_value(failing_value)

    def test_to_internal_value_returns_enum_value_when_value_is_int(self):
        field = EnumChoiceField(enum_class=IntTestEnum)

        result = field.to_internal_value(1)

        self.assertEqual(result, IntTestEnum.FIRST)

    def test_to_internal_value_returns_enum_value_when_value_is_string(self):
        field = EnumChoiceField(enum_class=CharTestEnum)

        result = field.to_internal_value('first')

        self.assertEqual(result, CharTestEnum.FIRST)


class SerializerIntegrationTests(TestCase):
    class Serializer(serializers.Serializer):
        enumeration = EnumChoiceField(enum_class=CharTestEnum)

    def test_field_value_is_serialized_correctly(self):
        serializer = self.Serializer({'enumeration': CharTestEnum.FIRST})

        result = serializer.data['enumeration']

        self.assertEqual(result, 'first')

    def test_field_is_deserialized_correctly(self):
        serializer = self.Serializer(data={'enumeration': 'first'})
        serializer.is_valid()

        result = serializer.validated_data['enumeration']

        self.assertEqual(result, CharTestEnum.FIRST)


class ModelSerializerIntegrationTests(TestCase):
    class Serializer(serializers.ModelSerializer):
        enumeration = EnumChoiceField(enum_class=CharTestEnum)

        class Meta:
            model = StringEnumeratedModel
            fields = ('enumeration', )

    def test_field_value_is_serialized_correctly(self):
        instance = StringEnumeratedModel.objects.create(
            enumeration=CharTestEnum.FIRST
        )

        serializer = self.Serializer(instance)

        result = serializer.data['enumeration']

        self.assertEqual(result, 'first')

    def test_field_is_deserialized_correctly(self):
        serializer = self.Serializer(data={'enumeration': 'first'})
        serializer.is_valid()

        result = serializer.validated_data['enumeration']

        self.assertEqual(result, CharTestEnum.FIRST)
