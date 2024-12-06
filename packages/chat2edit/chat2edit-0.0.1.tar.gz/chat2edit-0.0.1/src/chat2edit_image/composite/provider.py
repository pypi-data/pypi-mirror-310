import io
from typing import Union

from PIL import Image
from pydantic import TypeAdapter

from chat2edit import Context, ContextProvider, File, FileObject
from chat2edit_image.composite.context.classes import (CompositeImage, Filter,
                                                       Font, Graphic,
                                                       ImageObject, ImageText,
                                                       RasterGraphic,
                                                       VectorGraphic)
from chat2edit_image.composite.context.exemplars import (
    IMAGE_EDITING_EN_EXEMPLARS, IMAGE_EDITING_VI_EXEMPLARS)
from chat2edit_image.composite.context.functions import (
    apply_filter, remove_graphics_from_image, replace_image_objects_by_prompt,
    response_to_user, segment_image_objects_by_label)
from chat2edit_image.composite.types import Language
from chat2edit_image.constants import (COMPOSITE_IMAGE_FILE_EXTENSION,
                                       COMPOSITE_IMAGE_FILE_MIME_TYPE)
from chat2edit_image.utils.image import image_to_data_url

OBJ_TYPE_TO_CTX_NAME = {
    "ImageText": "text",
    "ImageObject": "object",
    "CompositeImage": "image",
}


class CompositeImageEditingProvider(ContextProvider):
    def __init__(self, language: Language) -> None:
        super().__init__()
        self.language = language
        self.lang_to_exem_cycles = {
            "en": IMAGE_EDITING_EN_EXEMPLARS,
            "vi": IMAGE_EDITING_VI_EXEMPLARS,
        }

    def get_context(self) -> Context:
        exec_context = {
            "Graphic": Graphic,
            "Filter": Filter,
            "VectorGraphic": VectorGraphic,
            "RasterGraphic": RasterGraphic,
            "Font": Font,
            "ImageText": ImageText,
            "ImageObject": ImageObject,
            "CompositeImage": CompositeImage,
            "apply_filter": apply_filter,
            "segment_image_objects_by_label": segment_image_objects_by_label,
            "replace_image_objects_by_prompt": replace_image_objects_by_prompt,
            "remove_graphics_from_image": remove_graphics_from_image,
            "response_to_user": response_to_user,
        }
        exem_cycles = self.lang_to_exem_cycles[self.language]
        return Context(exec_context, exem_cycles)

    def load_file_obj(self, file: File) -> FileObject:
        obj = None

        if file.mimetype.startswith("image/"):
            image = Image.open(io.BytesIO(file.buffer))
            data_url = image_to_data_url(image)
            obj = CompositeImage(size=image.size, data_url=data_url)
            filename = f"{file.filename}{COMPOSITE_IMAGE_FILE_EXTENSION}"
            return FileObject(obj, filename)

        elif file.name.endswith(COMPOSITE_IMAGE_FILE_EXTENSION):
            loadable_type = Union[CompositeImage, ImageObject]
            obj = TypeAdapter(loadable_type).validate_json(file.buffer)
            return FileObject(obj, file.filename)

        raise ValueError("Invalid composite image file")

    def save_file_obj(self, obj: FileObject) -> File:
        filename = obj.filename
        mimetype = COMPOSITE_IMAGE_FILE_MIME_TYPE
        buffer = obj.model_dump_json().encode()
        return File(mimetype, filename, buffer)
