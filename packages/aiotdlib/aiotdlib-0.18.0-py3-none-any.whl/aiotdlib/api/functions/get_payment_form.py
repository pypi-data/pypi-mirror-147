# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from ..base_object import BaseObject
from ..types import ThemeParameters


class GetPaymentForm(BaseObject):
    """
    Returns an invoice payment form. This method must be called when the user presses inlineKeyboardButtonBuy
    
    :param chat_id: Chat identifier of the Invoice message
    :type chat_id: :class:`int`
    
    :param message_id: Message identifier
    :type message_id: :class:`int`
    
    :param theme: Preferred payment form theme; pass null to use the default theme
    :type theme: :class:`ThemeParameters`
    
    """

    ID: str = Field("getPaymentForm", alias="@type")
    chat_id: int
    message_id: int
    theme: ThemeParameters

    @staticmethod
    def read(q: dict) -> GetPaymentForm:
        return GetPaymentForm.construct(**q)
