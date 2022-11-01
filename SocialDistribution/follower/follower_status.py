from enum import Enum

class FollowRequestStatus(Enum):
    NO_REQUEST_SENT = -1
    THEY_SENT_YOU = 0
    YOU_SENT_THEM = 1

    