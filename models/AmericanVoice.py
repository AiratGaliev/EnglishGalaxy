from enum import Enum

from models.Voice import Voice


class AmericanVoice(Enum):
    MALE: Voice = Voice('Male', 'a_v_m', '5ec777c2ae1afc001ace8fc3')
    FEMALE: Voice = Voice('Female', 'a_v_f', '5ec77831ae1afc001ace8fc9')
