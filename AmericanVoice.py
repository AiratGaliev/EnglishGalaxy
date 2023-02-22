from enum import Enum

from Voice import Voice


class AmericanVoice(Enum):
    AUSTIN_HOPKINS = Voice('Austin Hopkins', 'ah', '6159a26cc4bd0c0019267736')
    SUSAN_COLE = Voice('Susan Cole', 'sc', '602d06b2b037c400194dffdf')
    SHARON_HUANG = Voice('Sharon Huang', 'sh', '6061d986ba8e010019928ca5')
    TIM_CALKNEY = Voice('Tim Calkney', 'tc', '61599b9dc4bd0c0019267734')
