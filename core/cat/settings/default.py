# This are default settings for the Cat application.
from types import FunctionType
from typing import Type
from cat.settings.base import SettingElement


_class_or_singleton_type = FunctionType | Type | str


CHESHIRE_CAT = SettingElement(
    name="CheshireCat",
    default="cat.looking_glass.cheshire_cat.CheshireCat",
    type_=_class_or_singleton_type
)

STRAY_CAT = SettingElement(
    name="StrayCat",
    default="cat.looking_glass.stray_cat.StrayCat",
    type_="class"
)

MAD_HATTER = SettingElement(
    name="MadHatter",
    default="cat.mad_hatter.mad_hatter.MadHatter",
    type_=_class_or_singleton_type
)