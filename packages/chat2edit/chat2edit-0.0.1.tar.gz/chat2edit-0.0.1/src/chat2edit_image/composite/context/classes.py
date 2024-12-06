from typing import List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, Field

from chat2edit.prompting.decorators import declare_pydantic_class
from chat2edit.utils.factories import uuid4_factory


@declare_pydantic_class
class Graphic(BaseModel):
    id: str = Field(default_factory=uuid4_factory)
    size: Tuple[int, int]
    position: Tuple[int, int] = Field(default=(0, 0))
    rotation: float = Field(default=0.0)
    scale: float = Field(default=1.0, ge=0.0, lt=5.0)

    def __hash__(self) -> int:
        return super().__hash__(self.id)

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Graphic) and value.id == self.id


@declare_pydantic_class
class Filter(BaseModel):
    name: Literal["brightness", "contrast", "saturation", "sharpness", "blur"]
    value: Optional[float] = Field(default=None, ge=-1.0, le=1.0)


@declare_pydantic_class
class RasterGraphic(Graphic):
    data_url: str
    filters: List[Filter] = Field(default_factory=list)


@declare_pydantic_class
class VectorGraphic(Graphic):
    fill: Tuple[int, int, int, int] = Field(default=(0, 0, 0, 1))


@declare_pydantic_class
class Font(VectorGraphic):
    family: Literal[
        "Times New Roman",
        "Georgia",
        "Helvetica",
        "Arial",
        "Roboto",
        "Open Sans",
        "Courier New",
        "Montserrat",
        "Poppins",
    ] = Field(default="Arial")
    size: int = Field(default=100)
    style: Literal["normal", "italic", "oblique"] = Field(default="normal")
    weight: Literal["normal", "light", "bold", "extra-light", "extra-bold"] = Field(
        default="normal"
    )


@declare_pydantic_class
class ImageObject(RasterGraphic):
    labels: List[str]
    scores: List[float]
    inpainted: bool = Field(default=False)


@declare_pydantic_class
class ImageText(VectorGraphic):
    text: str
    font: Font


@declare_pydantic_class
class CompositeImage(RasterGraphic):
    graphics: List[Union[ImageObject, ImageText]] = Field(default_factory=list)
