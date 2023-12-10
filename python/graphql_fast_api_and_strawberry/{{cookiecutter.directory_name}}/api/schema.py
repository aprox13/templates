"""Endpoints module."""
import strawberry

import loggers
from api.routes.notes import NotesQuery, NotesMutation

logger = loggers.get_logger("api.schema")

STRIP_PREFIXES = ["Query", "Queries", "Mutation", "Mutations"]


def include(cls, method_name=None):
    def get_name():
        if method_name is not None:
            return method_name
        name: str = cls.__name__
        for p in STRIP_PREFIXES:
            if name.endswith(p):
                name = name[: -len(p)]
                break
        if name[0].isupper():
            name = name[0].lower() + name[1:]
        return name

    def _inner(orig):
        @strawberry.field
        def fun(self) -> cls:
            return cls()

        m_name = get_name()
        logger.debug(f"Adding {m_name} to {orig} with return type {cls}")
        setattr(orig, m_name, fun)
        return orig

    return _inner


@strawberry.type
@include(NotesQuery)
class Query:
    pass


@strawberry.type
@include(NotesMutation)
class Mutation:
    pass


GraphQLApiSchema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)
