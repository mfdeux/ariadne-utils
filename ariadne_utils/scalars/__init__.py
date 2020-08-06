import json
import uuid

from ariadne import ScalarType
from dateutil.parser import parser as date_parser
from validator_collection import validators

datetime_scalar = ScalarType("DateTime")
date_scalar = ScalarType("Date")
uuid_scalar = ScalarType("UUID")
email_address_scalar = ScalarType("EmailAddress")
url_scalar = ScalarType("URL")
json_scalar = ScalarType("JSON")
currency_scalar = ScalarType("Currency")

scalars = [
    datetime_scalar,
    date_scalar,
    uuid_scalar,
    email_address_scalar,
    url_scalar,
    json_scalar,
    currency_scalar,
]


@date_scalar.serializer
def serialize_date(value):
    return value.isoformat()


@date_scalar.value_parser
def parse_date_value(value):
    if value:
        return date_parser.parse(value)


@date_scalar.literal_parser
def parse_date_literal(ast):
    value = str(ast.value)
    return parse_date_value(value)


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_value(value):
    if value:
        return date_parser.parse(value)


@datetime_scalar.literal_parser
def parse_datetime_literal(ast):
    value = str(ast.value)
    return parse_datetime_value(value)


@uuid_scalar.serializer
def serialize_uuid(value):
    return str(value)


@uuid_scalar.value_parser
def parse_uuid_value(value):
    if value:
        try:
            return uuid.UUID(value)
        except ValueError:
            raise Exception("invalid UUID")


@uuid_scalar.literal_parser
def parse_uuid_literal(ast):
    value = str(ast.value)
    return parse_uuid_value(value)


@email_address_scalar.serializer
def serialize_email_address(value):
    return str(value)


@email_address_scalar.value_parser
def parse_email_address_value(value):
    if value:
        return validators.email(value)


@email_address_scalar.literal_parser
def parse_email_address_literal(ast):
    value = str(ast.value)
    return parse_email_address_value(value)


@url_scalar.serializer
def serialize_url(value):
    return str(value)


@url_scalar.value_parser
def parse_url_value(value):
    if value:
        return validators.url(value)


@url_scalar.literal_parser
def parse_url_literal(ast):
    value = str(ast.value)
    return parse_url_value(value)


@json_scalar.serializer
def serialize_json(value):
    return value


@json_scalar.value_parser
def parse_json_value(value):
    if value:
        return json.loads(value)


@json_scalar.literal_parser
def parse_json_literal(ast):
    value = str(ast.value)
    return parse_json_value(value)
