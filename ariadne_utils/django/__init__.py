import typing
import uuid

from ariadne.types import GraphQLResolveInfo
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from starlette.datastructures import UploadFile

from ..utils import merge_dict


async def convert_query_to_async(query: typing.Callable):
    return await database_sync_to_async(query)()


def get_limit_offset(pagination: typing.Dict) -> typing.Tuple[int, int]:
    if not pagination:
        pagination = {"limit": 25, "offset": 0}
    return pagination.get("offset", 0), pagination.get("limit", 25)


def standard_query(query, name, model, model_filter, user_field="owner"):
    async def resolve_item(obj: typing.Any, info: GraphQLResolveInfo, id: uuid.UUID):
        user = info.context["request"].scope["user"]
        item = model.objects.get(id=id, **{user_field: user})
        return item

    async def resolve_items(
        obj: typing.Any,
        info: GraphQLResolveInfo,
        pagination: typing.Dict = None,
        filter: typing.Dict = None,
    ):
        user = info.context["request"].scope["user"]
        offset, limit = get_limit_offset(pagination)
        initial_items = model.objects.filter(**{user_field: user})
        if hasattr(model, "created_by"):
            initial_items = initial_items.select_related("created_by")
        filtered_items = model_filter(
            queryset=initial_items, data=filter, request=info.context["request"]
        ).qs[offset:limit]
        return filtered_items

    return query.field(name)(resolve_item), query.field(f"{name}s")(resolve_items)


async def upload_to_content_file(file: UploadFile) -> ContentFile:
    file_contents = file.read()
    return ContentFile(file_contents, file.filename)


def standard_mutation(
    mutation,
    name,
    model,
    mutations: list = None,
    user_field="owner",
    file: bool = False,
):
    if not mutations:
        mutations = ["create", "update", "delete"]

    async def resolve_create_item(
        obj: typing.Any, info: GraphQLResolveInfo, input: typing.Dict
    ):
        user = info.context["request"].scope["user"]
        if file:
            for key, value in input.items():
                if isinstance(value, UploadFile):
                    input[key] = upload_to_content_file(value)
        item = model.objects.create(**{user_field: user}, **input)
        return item

    async def resolve_update_item(
        obj: typing.Any, info: GraphQLResolveInfo, slug: str, input: typing.Dict
    ):
        user = info.context["request"].scope["user"]
        if file:
            for key, value in input.items():
                if isinstance(value, UploadFile):
                    input[key] = upload_to_content_file(value)
        item = model.objects.get(**{user_field: user}, slug=slug)
        item = merge_dict(input, item)
        item.save()
        return item

    async def resolve_delete_item(obj: typing.Any, info: GraphQLResolveInfo, slug: str):
        user = info.context["request"].scope["user"]
        item = model.objects.get(**{user_field: user}, slug=slug)
        item.delete()
        return True

    return (
        mutation.field(f"create_{name}")(resolve_create_item)
        if "create" in mutations
        else None,
        mutation.field(f"update_{name}")(resolve_update_item)
        if "update" in mutations
        else None,
        mutation.field(f"delete_{name}")(resolve_delete_item)
        if "delete" in mutations
        else None,
    )
