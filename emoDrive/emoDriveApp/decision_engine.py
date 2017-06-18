import math
import audio_messager


ANGER_VIDEO_WEIGHT=1
SAD_VIDEO_WEIGHT=1
DISGUST_VIDEO_WEIGHT=1

ANGER_AUDIO_WEIGHT=1
SAD_AUDIO_WEIGHT=1
DISGUST_AUDIO_WEIGHT=1

SPEED_WEIGHT=1

MAX_SPEED=150


# THRESHOLDS
EMOTIONAL_THRESHOLD = 0.25;
ANGER_SPEED_THRESHOLD = 1
SAD_SPEED_THRESHOLD = 1
DISGUST_SPEED_THRESHOLD=1

# WARNINGS
ANGER_WITH_SPEED_STRING="Anger with speed alert!"
ANGER_STRING="Anger alert!"
SAD_WITH_SPEED_STRING="Sad with speed alert!"
SAD_STRING="Sad alert!"
DISGUST_WITH_SPEED_STRING="Disgust with speed alert!"
DISGUST_STRING="Anger alert!"
WEATHER_STRING="Weather alert!"



def anger_with_speed():
    return ANGER_WITH_SPEED_STRING,audio_messager.anger_with_speed()


def anger_without_speed():
    return ANGER_STRING, audio_messager.anger_without_speed()


def sad_with_speed():
    return SAD_WITH_SPEED_STRING, audio_messager.sad_with_speed()


def sad_without_speed():
    return SAD_STRING, audio_messager.sad_without_speed()


def disgust_with_speed():
    return DISGUST_SPEED_THRESHOLD, audio_messager.disgust_with_speed()


def disgust_without_speed():
    return DISGUST_WITH_SPEED_STRING, audio_messager.disgust_without_speed()


def weather_warning():
    return WEATHER_STRING, audio_messager.weather_warning()


def decide( processed_data ):

    if processed_data["weather"] == 1:
        return weather_warning()

    emotions = processed_data
    anger_score = emotions["v"]["angry"] * ANGER_VIDEO_WEIGHT + emotions["a"]["anger"] * ANGER_AUDIO_WEIGHT
    sad_score = emotions["v"]["sad"] * SAD_VIDEO_WEIGHT + emotions["a"]["sadness"] * SAD_AUDIO_WEIGHT
    disgust_score = emotions["v"]["disgust"] * DISGUST_VIDEO_WEIGHT + emotions["a"]["disgust"] * DISGUST_AUDIO_WEIGHT


    max_score = max(anger_score, sad_score, disgust_score)

    if max_score < EMOTIONAL_THRESHOLD:
        return

    if max_score == anger_score:
        total_score = max_score + get_speed_data(processed_data)
        if total_score > ANGER_SPEED_THRESHOLD:
            return total_score, anger_with_speed()
        else:
            return total_score, anger_without_speed()
    elif max_score == sad_score:
        total_score = max_score + get_speed_data(processed_data)
        if total_score > SAD_SPEED_THRESHOLD:
            return total_score, sad_with_speed()
        else:
            return total_score, sad_without_speed()
    else:
        if max_score + get_speed_data(processed_data) > DISGUST_SPEED_THRESHOLD:
            return total_score, disgust_with_speed()
        else:
            return total_score, disgust_without_speed()



def get_speed_data(processed_data):
    return processed_data["speed"] / MAX_SPEED
