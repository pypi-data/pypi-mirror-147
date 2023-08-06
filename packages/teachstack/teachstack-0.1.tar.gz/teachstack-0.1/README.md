# Python SDK for teachstack APIs

## Description

This module can be used to call teachstack APIs by just using a function. The functions are explained later in this document.

### Requirements

- Python 3
- Teachstack `ClientID` and `AuthKey` (https://docs.teachmint.com/api)

### Installing

- pip3 install teachstack
- Create a .env file and enter the following values:
  ```
  clientId = YOUR_CLIENT_ID
  authKey = YOUR_AUTH_KEY
  ```

### Executing program

```py
from teachstack import *

"""
Example Usage:
--------------

import os
from teachstack import *

addRoom("ROOM_ID", "ROOM_NAME")
os.system("open \"\"" + addUser("ROOM_ID", "USER_ID", "USER_NAME", 1).json().get("data").get("url"))
"""

```

### Functions

- addRoom(room_id: str, name: str, is_video_on: bool = False, is_mic_on: bool = False, video_quality: str = None, is_recording_on: bool = False, is_mute_blocked: bool = False, is_mic_blocked: bool = False, is_video_blocked: bool = False, is_chat_blocked: bool = False, is_front_camera: bool = False, is_portrait_vc: bool = False)
- getAllRoom()
- getRoom(room_id: str)
- deleteRoom(room_id: str)
- addUser(room_id: str, user_id: str, name: str, type: int)
- getRecordings(
  room_id: str = None,
  starting_after: str = None,
  ending_before: str = None,
  limit: int = None,
  status: list = None,
  recording_id: list = None,
  session_id: list = None,
  )
- deleteRecordings(UUIDs)

Note: Function will log only when in debug mode

## Authors

Contributors names and contact info
[Parth Agrawal](parth@teachmint.com)

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details
