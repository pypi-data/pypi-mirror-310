from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class GetBroadcastRevenueStats(TLObject):  # type: ignore
    """{schema}


    Details:
        - Layer: ``194``
        - ID: ``F788EE19``

    Parameters:
        peer (:obj:`InputPeer <pyrogram.raw.base.InputPeer>`):
            N/A

        dark (``bool``, *optional*):
            

    Returns:
        :obj:`stats.BroadcastRevenueStats <pyrogram.raw.base.stats.BroadcastRevenueStats>`
    """

    __slots__: List[str] = ["peer", "dark"]

    ID = 0xf788ee19
    QUALNAME = "functions.stats.GetBroadcastRevenueStats"

    def __init__(self, *, peer: "raw.base.InputPeer", dark: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.dark = dark  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBroadcastRevenueStats":
        
        flags = Int.read(b)
        
        dark = True if flags & (1 << 0) else False
        peer = TLObject.read(b)
        
        return GetBroadcastRevenueStats(peer=peer, dark=dark)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.dark else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        return b.getvalue()
