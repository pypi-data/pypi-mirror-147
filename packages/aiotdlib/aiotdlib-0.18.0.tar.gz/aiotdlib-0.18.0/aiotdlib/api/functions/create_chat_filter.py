# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import ChatFilter


class CreateChatFilter(BaseObject):
    """
    Creates new chat filter. Returns information about the created chat filter
    
    :param filter_: Chat filter
    :type filter_: :class:`ChatFilter`
    
    """

    ID: str = Field("createChatFilter", alias="@type")
    filter_: ChatFilter = Field(..., alias='filter')

    @staticmethod
    def read(q: dict) -> CreateChatFilter:
        return CreateChatFilter.construct(**q)
