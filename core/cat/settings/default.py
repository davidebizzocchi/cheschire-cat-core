"""
These are the default settings for the Cat's whimsical world.
Tread carefully, down the rabbit hole we go!
"""
from types import FunctionType
from typing import Type
from cat.settings.base import SettingElement


# Type hint for things that can be a class, a singleton function, or just a string path
# Basically, anything that helps us find our way in Wonderland.
_class_or_singleton_type = FunctionType | Type | str


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# |       Agents of Whimsy       |
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FORM_AGENT = SettingElement(
    name="FORM_AGENT",
    default="cat.agents.form_agent.FormAgent",
    type_=_class_or_singleton_type
)
MAIN_AGENT = SettingElement(
    name="MAIN_AGENT",
    default="cat.agents.main_agent.MainAgent",
    type_=_class_or_singleton_type
)
MEMORY_AGENT = SettingElement(
    name="MEMORY_AGENT",
    default="cat.agents.memory_agent.MemoryAgent",
    type_=_class_or_singleton_type
)
PROCEDURES_AGENT = SettingElement(
    name="PROCEDURES_AGENT",
    default="cat.agents.procedures_agent.ProceduresAgent",
    type_=_class_or_singleton_type
)


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# |       Core Components of Madness         |
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MAD_HATTER = SettingElement(
    name="MAD_HATTER",
    default="cat.mad_hatter.mad_hatter.MadHatter",
    type_=_class_or_singleton_type
)
RABBIT_HOLE = SettingElement(
    name="RABBIT_HOLE",
    default="cat.rabbit_hole.RabbitHole",
    type_=_class_or_singleton_type
)
WHITE_RABBIT = SettingElement(
    name="WHITE_RABBIT",
    default="cat.looking_glass.white_rabbit.WhiteRabbit",
    type_=_class_or_singleton_type
)
CACHE_MANAGER = SettingElement(
    name="CACHE_MANAGER",
    default="cat.cache.cache_manager.CacheManager",
    type_=_class_or_singleton_type
)


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# |       Feline Entities        |
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CHESHIRE_CAT = SettingElement(
    name="CHESHIRE_CAT",
    default="cat.looking_glass.cheshire_cat.CheshireCat",
    type_=_class_or_singleton_type
)
STRAY_CAT = SettingElement(
    name="STRAY_CAT",
    default="cat.looking_glass.stray_cat.StrayCat",
    type_="class" # Just a blueprint for a cat, not the cat itself.
)
