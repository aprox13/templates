import functools
import typing

import strawberry
from dependency_injector.wiring import Provide, inject
from strawberry.extensions import FieldExtension
from strawberry.field import StrawberryField
from strawberry.types import Info


# noinspection PyAbstractClass
class DependencyExtension(FieldExtension):
    def __init__(self):
        self.dependency_args: list[typing.Any] = []

    def apply(self, field: StrawberryField) -> None:
        # Remove dependency_injector provider arguments from the list that strawberry tries to resolve
        di_arguments = []
        keep_arguments = []
        for arg in field.arguments:
            if isinstance(arg.default, Provide):
                di_arguments.append(arg)
                continue
            keep_arguments.append(arg)

        field.arguments = keep_arguments
        self.dependency_args = di_arguments

    async def resolve_async(
        self,
        next_: typing.Callable[..., typing.Any],
        source: typing.Any,
        info: Info,
        **kwargs,
    ) -> typing.Any:
        res = await next_(source, info, **kwargs)
        return res


def query(**strawberry_kwargs):
    return _deco_impl(strawberry.field, **strawberry_kwargs)


def mutation(**strawberry_kwargs):
    return _deco_impl(strawberry.mutation, **strawberry_kwargs)


def _deco_impl(_strawberry_fun, **strawberry_kwargs):
    kws = strawberry_kwargs
    key = "extensions"
    ext = [] if key not in kws else kws[key]
    ext.append(DependencyExtension())
    kws[key] = ext

    def decorator(fun):
        @_strawberry_fun(**kws)
        @inject
        @functools.wraps(fun)
        def _inner(*args, **kwargs):
            return fun(*args, **kwargs)

        return _inner

    return decorator
