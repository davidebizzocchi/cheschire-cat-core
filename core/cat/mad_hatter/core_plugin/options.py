from cat.mad_hatter.decorators import option
from cat.rabbit_hole import RabbitHole
from cat.agents.main_agent import MainAgent
from cat.looking_glass.white_rabbit import WhiteRabbit
from cat.log import log


@option("rabbit_hole", priority=0)
class RabbitHoleDefault(RabbitHole):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.warning("\n\n\nWELLAAA!!!!!!\n\n\n")

@option("white_rabbit", priority=0)
class WhiteRabbitDefault(WhiteRabbit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.warning("\n\n\nWELLAAA!!!!!!\n\n\n")

@option("main_agent", priority=0)
class MainAgentDefault(MainAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        log.warning("\n\n\nWELLAAA!!!!!!\n\n\n")