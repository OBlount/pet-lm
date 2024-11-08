# Ascii art source: https://www.asciiart.eu/
MAX_MSG_SIZE = 200
def dog(message: str) -> str:
    speech_bubble = f"< {message[0:MAX_MSG_SIZE]} >"
    response = f"""
      __
 (___()'`; {speech_bubble}
 /,    /`  
 \\\\"--\\\\
    """
    print(response)

def cat(message: str) -> str:
    speech_bubble = f"< {message[0:MAX_MSG_SIZE]} >"
    response = f"""
\    /\\
 )  ( ') {speech_bubble}
 (  /  )   
  \(__)|   
    """
    print(response)

def default_avatar(message: str) -> str:
    print(f"~~> {message[0:MAX_MSG_SIZE]}")
