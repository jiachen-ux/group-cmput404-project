import uuid

def getUUID(stringUUID):
    if "/" in stringUUID:
        # We are dealing with a URL ID
        stringUUID = stringUUID.split("/")[-1]
    return uuid.UUID(stringUUID)


def getAuthorIDandPostIDFromLikeURL(url: str):
    arr = url.split("/")
    if "comment" in url:
        return arr[-5],arr[-3], arr[-1]
    return arr[-3], arr[-1], None