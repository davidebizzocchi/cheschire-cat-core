from cat.mad_hatter.decorators import option
from cat.rabbit_hole import RabbitHole
from cat.agents.main_agent import MainAgent
from cat.looking_glass.white_rabbit import WhiteRabbit
from cat.log import log


@option(RabbitHole, priority=0)
class RabbitHoleDefault(RabbitHole):
    is_custom = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.warning("\n\n\nWELLAAA!!!!!!\n\n\n")

@option(WhiteRabbit, "WhiteRabbit", priority=0)
class WhiteRabbitDefault(WhiteRabbit):
    is_custom = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.warning("\n\n\nWELLAAA!!!!!!\n\n\n")

@option(MainAgent, priority=0)
class MainAgentDefault(MainAgent):
    is_custom = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.warning("\n\n\nWELLAAA!!!!!!\n\n\n")

