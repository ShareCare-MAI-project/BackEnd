import re
from typing import Any, Callable

from pydantic_core import core_schema

PHONE_REGEX = r"^\+79[0-9]{9}$"


#  Пример кастомного типа, работающего с Pydantic+Swagger
class PhoneNumber(str):
    """Класс для валидации номера телефона."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema]
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(
                min_length=10,
                max_length=15,
                pattern=PHONE_REGEX
            ),
            serialization=core_schema.to_string_ser_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        if not re.match(PHONE_REGEX, v):
            raise ValueError('Неверный формат номера телефона')

        return v
