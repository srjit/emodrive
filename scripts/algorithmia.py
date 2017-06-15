import Algorithmia

apiKey = 'simQAbMR5x/Aw1QuWcRenMEWffU1'
client = Algorithmia.client(apiKey)


algo = client.algo('demo/Hello/0.1.1')
response = algo.pipe("HAL 9000")

# input = {
#     "image": "https://s-media-cache-ak0.pinimg.com/originals/de/bd/3d/debd3d0f7478d7a6b0b7215ee779e323.jpg",
#     "numResults": 7
# }


input = {
    "image": "dropbox:///images/neutral.jpg",
    "numResults": 7
}


algo = client.algo('deeplearning/EmotionRecognitionCNNMBP/0.1.2')

result = algo.pipe(input).result

print(result)