# SPDX-FileCopyrightText: 2024 Zsbyqx20 <112002598+Zsbyqx20@users.noreply.github.com>
#
# SPDX-License-Identifier: Apache-2.0

import base64
import io
from typing import Any, NotRequired, TypedDict, Union, overload

from PIL import Image

from .base import BaseMessage, ContentType, ImageDetail, ImageFormat, Role
from .utils import is_valid_image_url

MessageDict = TypedDict(
    "MessageDict",
    {
        "content": Union[str, Image.Image],
        "role": NotRequired[str],
        "type": NotRequired[str],
        "format": NotRequired[str],
        "detail": NotRequired[str],
    },
)


class TextMessage(BaseMessage[str]):
    pass


class ImageMessage(BaseMessage[Image.Image]):
    def __init__(
        self,
        content: Image.Image | str,
        format: ImageFormat = ImageFormat.PNG,
        detail: ImageDetail = ImageDetail.AUTO,
    ):
        if isinstance(content, str):
            content_, format_ = is_valid_image_url(content)
            content = content_
            if format_ == ImageFormat.UNKNOWN:
                format = ImageFormat.PNG
        super().__init__(content, role=Role.USER, content_type=ContentType.IMAGE)
        self._format = format
        self._detail = detail

    @property
    def content(self) -> str:
        img_byte_arr = io.BytesIO()
        self._content.save(img_byte_arr, format=self._format.value)
        img_byte_arr = img_byte_arr.getvalue()
        return base64.b64encode(img_byte_arr).decode()

    @property
    def detail(self):
        return self._detail


@overload
def convert_to_message(msg: str) -> TextMessage: ...
@overload
def convert_to_message(msg: Image.Image) -> ImageMessage: ...
@overload
def convert_to_message(msg: dict[str, Any]) -> BaseMessage: ...


def convert_to_message(msg: str | Image.Image | dict[str, Any]) -> BaseMessage:
    if isinstance(msg, str):
        return TextMessage(content=msg, role=Role.USER)

    if isinstance(msg, Image.Image):
        if msg.format:
            format_ = ImageFormat[msg.format.upper()]
        else:
            format_ = ImageFormat.PNG
        return ImageMessage(content=msg, format=format_)

    if isinstance(msg, dict):
        msg_dict: MessageDict = {
            "content": msg["content"],
            "role": msg.get("role", "user"),
            "type": msg.get("type", "text"),
        }

        role = Role(msg_dict["role"])

        if msg_dict["type"] == ContentType.TEXT.value:
            if not isinstance(msg_dict["content"], str):
                raise ValueError("Invalid text message format")
            return TextMessage(content=msg_dict["content"], role=role)
        elif msg_dict["type"] == ContentType.IMAGE.value:
            if not isinstance(msg_dict["content"], (str, Image.Image)):
                raise ValueError("Image content must be either string or PIL.Image")
            return ImageMessage(
                content=msg_dict["content"],
                format=ImageFormat(msg.get("format", "png")),
                detail=ImageDetail(msg.get("detail", "auto")),
            )
        raise ValueError(f"Unsupported content type: {msg_dict['type']}")

    raise ValueError(f"Unsupported message type: {type(msg)}")
