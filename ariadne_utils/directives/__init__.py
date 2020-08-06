import typing

from ariadne import SchemaDirectiveVisitor
from ariadne.types import GraphQLResolveInfo
from graphql import default_field_resolver
from pytimeparse import parse as parse_duration

from .utils.rate_limit import RateLimit, TooManyRequests


class DateDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        date_format = self.args.get("format")
        original_resolver = field.resolve or default_field_resolver

        def resolve_formatted_date(obj, info, **kwargs):
            result = original_resolver(obj, info, **kwargs)
            if result is None:
                return None

            if date_format:
                return result.strftime(date_format)

            return result.isoformat()

        field.resolve = resolve_formatted_date
        return field


class AuthDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver

        def resolve_formatted_date(obj, info, **kwargs):
            if not info.context["request"].scope["user"].is_authenticated:
                raise Exception("unauthenticated user")

            result = original_resolver(obj, info, **kwargs)
            return result

        field.resolve = resolve_formatted_date

        return field


class PermissionsDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver

        def resolve_formatted_date(obj, info, **kwargs):
            if not info.context["request"].scope["user"].is_authenticated:
                raise Exception("unauthenticated user")

            result = original_resolver(obj, info, **kwargs)
            return result

        field.resolve = resolve_formatted_date

    def visit_object(self, object_type):

        return object_type


class RateLimitDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        max_ = self.args.get("max", 10)
        window = parse_duration(self.args.get("window", "10m"))
        message = self.args.get("message", "You are doing that too often.")
        original_resolver = field.resolve or default_field_resolver

        def resolve_rate_limited(obj: typing.Any, info: GraphQLResolveInfo, **kwargs):

            if info.context["request"]["user"].is_authenticated:
                client = info.context["request"].scope["user"].id
            else:
                ip_address, port = info.context["request"]["client"]
                client = ip_address

            try:
                with RateLimit(
                    resource=info.field_name,
                    client=client,
                    max_requests=max_,
                    expire=window,
                ):
                    result = original_resolver(obj, info, **kwargs)
                    return result
            except TooManyRequests:
                raise TooManyRequests(message)

        field.resolve = resolve_rate_limited
        return field


directives = {
    "date": DateDirective,
    "auth": AuthDirective,
    "permissions": PermissionsDirective,
    "rateLimit": RateLimitDirective,
}
