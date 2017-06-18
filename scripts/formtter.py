

def format(image_response, audio_response):
    processed_data = {}
    processed_data["a"] = {emotion["tone_name"].lower() : emotion["score"] for emotion in audio_response}
    processed_data["v"] = {emotion[1].lower():emotion[0] for emotion in image_reponse['results']}
    return processed_data
    