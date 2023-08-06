from typing import Any
import pip._vendor.requests as requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()

clientId = os.environ.get("clientId")
authKey = os.environ.get("authKey")

baseUrl = "https://api.teachmint.com"

headers = {"Content-Type": "application/json",
           "clientId": clientId, "authKey": authKey}


def printException(e: Exception):
    if e == requests.exceptions.HTTPError:
        print("HTTP Error....Please check the URL again")
    elif e == requests.exceptions.ConnectionError:
        print("Connection error")
    elif e == requests.exceptions.Timeout:
        print("Request Timeout")
    elif e == requests.exceptions.RequestException:
        print("Request Exception")
    else:
        print(e)


def printResponseWhenDebugMode(response: Any):
    if sys.gettrace():
        if response.content == b"" or response.content == "":
            print("Empty Response")
        else:
            print(response.json())


def addRoom(
    room_id: str,
    name: str,
    is_video_on: bool = False,
    is_mic_on: bool = False,
    video_quality: str = None,
    is_recording_on: bool = False,
    is_mute_blocked: bool = False,
    is_mic_blocked: bool = False,
    is_video_blocked: bool = False,
    is_chat_blocked: bool = False,
    is_front_camera: bool = False,
    is_portrait_vc: bool = False,
):
    json = {
        "room_id": room_id,
        "name": name,
        "settings": {
            "is_video_on": is_video_on,
            "is_mic_on": is_mic_on,
            "video_quality": video_quality,
            "is_recording_on": is_recording_on,
            "is_mute_blocked": is_mute_blocked,
            "is_mic_blocked": is_mic_blocked,
            "is_video_blocked": is_video_blocked,
            "is_chat_blocked": is_chat_blocked,
            "is_front_camera": is_front_camera,
            "is_portrait_vc": is_portrait_vc,
        },
    }
    try:
        response = requests.post(
            baseUrl + "/v2/rooms", headers=headers, json=json)
        printResponseWhenDebugMode(response)
        return response
    except:
        printException()


def getAllRoom():
    try:
        response = requests.get(baseUrl + "/v2/rooms",
                                headers=headers, json=None)
        printResponseWhenDebugMode(response)
        return response
    except:
        printException()


def getRoom(room_id: str):
    try:
        response = requests.get(
            baseUrl + "/v2/rooms/" + room_id, headers=headers, json=None)
        printResponseWhenDebugMode(response)
        return response
    except:
        printException()


def deleteRoom(room_id: str):
    try:
        response = requests.delete(
            baseUrl + "/v2/rooms/" + room_id, headers=headers, json=None)
        printResponseWhenDebugMode(response)
        return response

    except:
        printException()


def addUser(room_id: str, user_id: str, name: str, type: int):
    json = {"user_id": user_id, "name": name, "type": type}
    try:
        response = requests.post(
            baseUrl + "/v2/rooms/" + room_id + "/users", headers=headers, json=json)
        printResponseWhenDebugMode(response)
        return response
    except:
        printException()


def getRecordings(
    room_id: str = None,
    starting_after: str = None,
    ending_before: str = None,
    limit: int = None,
    status: list = None,
    recording_id: list = None,
    session_id: list = None,
):
    try:
        response = requests.get(
            baseUrl + "/v2/recordings",
            headers=headers,
            json=None,
            params={
                "room_id": room_id,
                "starting_after": starting_after,
                "ending_before": ending_before,
                "limit": limit,
                "status": status,
                "recording_id": recording_id,
                "session_id": session_id,
            },
        )
        printResponseWhenDebugMode(response)
        return response
    except:
        printException()


def deleteRecordings(UUIDs):
    json = {"videos": UUIDs}
    try:
        response = requests.delete(
            baseUrl + "/v2/recordings", headers=headers, json=json)
        printResponseWhenDebugMode(response)
        return response
    except Exception as e:
        printException(e)
