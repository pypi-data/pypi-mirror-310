from moneyed import (
    Currency,
    CurrencyDoesNotExist,
    Money,
    get_currency,
)
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, Field, IntegerField
from rest_framework.serializers import Serializer
from typing import Dict, Literal, Optional, Union

__all__ = ("MoneyField", "MoneyRepresentation", "MoneySerializer")


MoneyRepresentation = Dict[Literal["amount", "currency"], Union[int, str]]


class MoneySerializer(Serializer):
    amount = IntegerField()
    currency = CharField()

    def validate_currency(self, value: str) -> Currency:
        try:
            return get_currency(code=value)
        except CurrencyDoesNotExist as e:
            raise ValidationError(str(e))

    def create(self, validated_data: Dict) -> Money:
        currency = validated_data["currency"]

        return Money(
            amount=validated_data["amount"] / currency.sub_unit, currency=currency
        )


class MoneyField(Field):
    @staticmethod
    def to_internal_value(
        data: Optional[Union[Money, MoneyRepresentation]]
    ) -> Optional[Money]:
        if data is None:
            return None

        if isinstance(data, Money):
            return data

        serializer = MoneySerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return serializer.save()

    @staticmethod
    def to_representation(value: Optional[Money]) -> Optional[MoneyRepresentation]:
        if value is None:
            return None

        return {
            "amount": value.get_amount_in_sub_unit(),
            "currency": value.currency.code,
        }
