from enum import Enum

from models.Voice import Voice


class BritishVoice(Enum):
    MALE: Voice = Voice('Male', 'b_v_m', '60f66a0e051d090019bab6fd')
    FEMALE: Voice = Voice('Female', 'b_v_f', '60f66a95051d090019bab6fe')
