from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, Self, TypeVar, get_args, cast

from pydantic import BaseModel, ConfigDict
from svgwrite.container import SVG, Group

from .graphics._graphics import (
    GraphicsContainer,
    BaseContainer,
)
from .graphics.properties import Properties

__all__ = [
    "BaseParams",
    "BaseGlyph",
    "EmptyParams",
    "EmptyGlyph",
]


class BaseParams(BaseModel):
    """
    Subclass this class to create parameters for a Glyph.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def desc(self) -> str:
        """
        Short description of params and values.
        """

        def parse_val(val: Any) -> str:
            if isinstance(val, type):
                return val.__name__
            elif isinstance(val, BaseParams):
                return val.desc
            elif isinstance(val, Iterable) and not isinstance(val, str):
                return f"_".join([parse_val(v) for v in val])
            else:
                return str(val).replace("=", "~").replace(".", "_")

        params = []

        for field in type(self).model_fields.keys():
            val: Any = getattr(self, field)
            val_desc = parse_val(val)

            params.append(f"{field}-{val_desc}")

        return "__".join(params)


class BaseGlyph[ParamsT: BaseParams](ABC, GraphicsContainer, BaseContainer):
    """
    Base class for a standalone or reusable glyph, sized in abstract
    (user) units.
    """

    params: ParamsT
    """
    Instance of params with type as specified by typevar.
    """

    DefaultParams: type[ParamsT] | None = None
    """
    Subclass of ParamsT to use as defaults for this particular Glyph,
    if no parameters provided during instantiation.
    """

    _params_cls: type[ParamsT]
    """
    Params class: the type parameter provided as ParamsT, or EmptyParams
    if no type parameter provided.
    """

    def __init__(
        self,
        *,
        glyph_id: str | None = None,
        params: ParamsT | None = None,
        properties: Properties | None = None,
        size: tuple[float, float] | None = None,
        parent: BaseGlyph | None = None,
        insert: tuple[float, float] | None = None,
    ):
        """
        :param parent: Parent glyph, or `None`{l=python} to create top-level glyph
        :param glyph_id: Unique identifier, or `None`{l=python} to generate one
        """

        # if parent not provided, ensure insert/size_inst not provided
        if parent is None:
            assert insert is None

        super().__init__(glyph_id, properties, size)

        # set params
        self.params = params or type(self).get_params_cls()()

        # invoke subclass's init (e.g. set properties based on params)
        self.init()

        # invoke post-init since size_canon may be set in init()
        self._init_post()

        # invoke subclass's drawing logic
        self.draw()

        if parent is not None:
            parent.insert_glyph(self, insert)

    def __init_subclass__(cls: type[BaseGlyph]):
        """
        Populate _params_cls with the class representing the parameters for
        this glyph. If not subscripted with a type arg by the subclass,
        _params_cls is set to EmptyParams.
        """

        # note: pyright is not yet aware that the new style
        #
        # class BaseGlyph[ParamsT: BaseParams](...): ...
        #
        #   is equivalent to
        #
        # ParamsT = TypeVar("ParamsT", bound=BaseParams)
        # class BaseGlyph(Generic[ParamsT], ...): ...
        #
        # since with the new style, Generic is not a base. Nonetheless
        # __orig_bases__ is indeed defined here.
        orig_bases = (
            cls.__orig_bases__  # pyright: ignore[reportGeneralTypeIssues]
        )

        # get_args() returns tuple[Any, ...], but we know the type param
        # should always be ParamsT
        args: tuple[type[ParamsT]] = cast(
            tuple[type[ParamsT]], get_args(orig_bases[0])
        )

        if len(args) > 0:
            assert len(args) == 1

            params_cls: type[ParamsT]

            if isinstance(args[0], TypeVar):
                # have a TypeVar, look up its bound
                type_var = cast(TypeVar, args[0])
                assert type_var.__bound__ is not None
                params_cls = type_var.__bound__
            else:
                # already have a class
                params_cls = args[0]

            cls._params_cls = params_cls
        else:
            # set _params_cls with EmptyParams
            cls._params_cls = EmptyParams

        assert issubclass(cls._params_cls, BaseParams)

    @property
    def glyph_id(self) -> str:
        """
        A meaningful identifier to associate with this glyph. Also used as
        base name (without extension) of file to write when no filename is
        provided.

        If no glyph_id is provided when created, it is derived from the
        class name.
        """
        return self._id_norm

    @classmethod
    def get_params_cls(cls) -> type[ParamsT]:
        """
        Returns the {obj}`BaseParams` subclass with which this class is
        parameterized, accounting for any default values provided by
        the subclass.
        """
        return cls.DefaultParams or cls._params_cls

    def insert_glyph(
        self,
        glyph: BaseGlyph,
        insert: tuple[float, float] | None = None,
    ) -> Self:
        self._nested_glyphs.append(glyph)

        # add group to self, using wrapper svg for placement
        wrapper_insert: SVG = self._drawing.svg(
            **glyph._get_elem_kwargs(suffix="wrapper-insert"),
            insert=insert,
        )

        wrapper_insert.add(glyph._group)
        self._svg.add(wrapper_insert)

        return self

    def init(self):
        ...

    @abstractmethod
    def draw(self):
        ...


class EmptyParams(BaseParams):
    pass


class EmptyGlyph(BaseGlyph[EmptyParams]):
    """
    Glyph to use as an on-the-fly alternative to subclassing
    {obj}`BaseGlyph`. It has an empty {obj}`BaseGlyph.draw`
    implementation; the user can then add graphics objects
    and other glyphs after creation.

    Example:

    ```python
    glyph1 = MyGlyph1()
    glyph2 = MyGlyph2()

    # create an empty glyph with unspecified size
    glyph = EmptyGlyph()

    # insert a glyph
    glyph.insert_glyph(glyph1)

    # insert another glyph in a different position
    glyph.insert_glyph(glyph2, (100, 100))
    ```
    """

    def draw(self):
        pass
