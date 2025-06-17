from enum import Enum, auto


class DialoguePhase(Enum):
    """
    Represents the distinct phases of a Fire Circle dialogue ceremony.
    Based on firecircle/docs/DESIGN.MD.
    """
    INITIALIZING = auto()
    CONVENING = auto()      # Added based on 36th Builder's ceremony description
    INTRODUCTION = auto()   # Added based on 36th Builder's ceremony description
    EXPLORATION = auto()    # Added based on 36th Builder's ceremony description
    DEEPENING = auto()      # Added based on 36th Builder's ceremony description
    SUMMARIZING = auto()
    VOTING = auto()
    RESOLUTION = auto()     # Added based on 36th Builder's ceremony description
    CONCLUDED = auto()
    INTEGRATION = auto()    # Added based on 36th Builder's ceremony description
    EXTENDING = auto()      # For follow-up or continued dialogue
    FAILED = auto()         # If the ceremony cannot proceed
