# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import OrderInfo


class ValidateOrderInfo(BaseObject):
    """
    Validates the order information provided by a user and returns the available shipping options for a flexible invoice
    
    :param chat_id: Chat identifier of the Invoice message
    :type chat_id: :class:`int`
    
    :param message_id: Message identifier
    :type message_id: :class:`int`
    
    :param order_info: The order information, provided by the user; pass null if empty
    :type order_info: :class:`OrderInfo`
    
    :param allow_save: Pass true to save the order information
    :type allow_save: :class:`bool`
    
    """

    ID: str = Field("validateOrderInfo", alias="@type")
    chat_id: int
    message_id: int
    order_info: OrderInfo
    allow_save: bool

    @staticmethod
    def read(q: dict) -> ValidateOrderInfo:
        return ValidateOrderInfo.construct(**q)
