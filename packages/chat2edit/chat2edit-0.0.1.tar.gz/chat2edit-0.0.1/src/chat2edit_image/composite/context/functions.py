from copy import deepcopy
from typing import List, Union

from PIL import Image

from chat2edit.execution.decorators import (feedback_invalid_argument,
                                            feedback_unassigned_value,
                                            feedback_unexpected_error,
                                            response)
from chat2edit.models.messages import ContextMessage
from chat2edit.prompting.decorators import declare_function
from chat2edit_image.composite.context.classes import (CompositeImage, Filter,
                                                       ImageObject, ImageText,
                                                       RasterGraphic)
from chat2edit_image.cv.registry import get_predictor
from chat2edit_image.utils.image import (data_url_to_image, image_to_data_url,
                                         image_to_mask)


@feedback_unassigned_value
@feedback_unexpected_error
@feedback_invalid_argument
@declare_function()
async def segment_image_objects_by_label(
    image: CompositeImage, label: str
) -> List[ImageObject]:
    objects = []

    async with get_predictor("GDinoPredictor") as predictor:
        scores, boxes = predictor(image, label)

    async with get_predictor("SAM2Predictor") as predictor:
        for score, box in zip(scores, boxes):
            mask = predictor(image, box=box)
            obj_box = mask.getbbox()
            obj_mask = mask.crop(obj_box)
            obj_image = Image.new("RGBA", obj_mask.size)
            obj_image.paste(image.crop(obj_box), mask=obj_mask)
            data_url = image_to_data_url(obj_image)
            obj = ImageObject(
                size=(obj_image.width, obj_image.height),
                position=(obj_box[0], obj_box[1]),
                data_url=data_url,
                labels=[label],
                scores=[score],
                inpainted=False,
            )
            objects.append(obj)

    image.graphics.extend(objects)

    return objects


@feedback_unassigned_value
@feedback_unexpected_error
@feedback_invalid_argument
@declare_function()
async def replace_image_objects_by_prompt(
    image: CompositeImage, objects: List[ImageObject], prompt: str
) -> CompositeImage:
    new_image = deepcopy(image)

    mask = Image.new("L", image.size)

    for obj in objects:
        obj_image = data_url_to_image(obj.data_url)
        obj_mask = image_to_mask(obj_image)
        mask.paste(obj_mask, obj.get_box(), obj_mask)

    pil_image = data_url_to_image(new_image.data_url)

    async with get_predictor("SDInpaintPredictor") as predictor:
        inpainted_pil_image = predictor(pil_image, mask, prompt)

    new_image.data_url = image_to_data_url(inpainted_pil_image)
    return new_image


@feedback_unassigned_value
@feedback_unexpected_error
@feedback_invalid_argument
@declare_function()
async def remove_graphics_from_image(
    image: CompositeImage, graphics: List[Union[ImageObject, ImageText]]
) -> CompositeImage:
    new_image = deepcopy(image)

    uninpainted_objects = _get_uninpainted_image_objects(graphics)
    await _inpaint_image_objects(new_image, uninpainted_objects)

    ids_to_remove = set(g.id for g in graphics)
    new_image.graphics = [g for g in image.graphics if g.id not in ids_to_remove]

    return new_image


@feedback_unexpected_error
@feedback_invalid_argument
@response
@declare_function()
def response_to_user(text: str, variables: List[RasterGraphic] = []) -> None:
    return ContextMessage(text=text, objs_or_paths=variables)


@feedback_unassigned_value
@feedback_unexpected_error
@feedback_invalid_argument
@declare_function()
def apply_filter(graphic: RasterGraphic, filt: Filter) -> RasterGraphic:
    new_graphic = deepcopy(graphic)

    for f in new_graphic.filters:
        if f.name == filt.name:
            if filt.value:
                f.value += filt.value

            return new_graphic

    new_graphic.filters.append(filt)
    return new_graphic


def _get_uninpainted_image_objects(objects: List[ImageObject]) -> List[ImageObject]:
    return [
        obj for obj in objects if isinstance(obj, ImageObject) and not obj.inpainted
    ]


async def _inpaint_image_objects(
    image: CompositeImage, objects: List[ImageObject]
) -> None:
    mask = Image.new("L", image.size)

    for obj in objects:
        obj_image = data_url_to_image(obj.data_url)
        obj_mask = image_to_mask(obj_image)
        mask.paste(obj_mask, obj.get_box(), obj_mask)

    pil_image = data_url_to_image(image.data_url)

    async with get_predictor("LaMaPredictor") as predictor:
        inpainted_pil_image = predictor(pil_image, mask)

    image.data_url = image_to_data_url(inpainted_pil_image)

    for obj in objects:
        obj.inpainted = True
