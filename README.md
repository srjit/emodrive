# Emodrive (AngelHack Global Hackathon Series: Boston)

Emodrive: Driver monitoring system that continuously monitors the emotion of the driver, speech in the vehicle and a few external conditions to quantify the safety of driving

Emotions which we consider are critical - Anger, Disgust and Fear. 

## APIs used:
1. IBM Watson speech recognition API
2. Algorithmia Image Analysis

The project was developed using Django Web framework in Python.

## Results
By feeding the image and Audio of the driver. We generate a safety score which is a measure of the combined emotions such as
Anger, disgust and fear. It then presents a text message on the web page to display the next course of action for the driver.
Messages can be, "Drive slow", "Call to 911" etc.

## Limitations:
1. Watson API's takes a lot of time to respond with the speech analysis.

## Future work
1. Incorporate sensors to get environmental factors such as climate, car speed etc.
2. Incorporate video analysis over Image analysis
3. Noise reduction to focus on Driver speech and video feed.
4. Response module to account for next best action that can be taken by the driver.
5. Work around for low Internet coverage problems.





