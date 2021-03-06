import Algorithmia
import dropbox
import os

## Algorithmia client
apiKey = 'simQAbMR5x/Aw1QuWcRenMEWffU1'
client = Algorithmia.client(apiKey)
algo = client.algo('deeplearning/EmotionRecognitionCNNMBP/0.1.2')

## Dropbox client
access_token="LADJrEFyvzAAAAAAAAAAPmxqPUmb_CQlDVK-iUvXLKyk6DbxuoV_0_UVoqTqZoIa"
dbx = dropbox.Dropbox(access_token)

def dropbox_image_upload(image_path, dropbox_path):
    """
    
    Arguments:
    - `local_filepath`:
    - `dropbox_path`:
    """
    with open(image_path, 'rb') as f:
        dbx.files_upload(f.read(),upload_path,mute=True)
        print("Uploaded ", file_name)


def get_dropbox_files(folder):
    """
    
    Arguments:
    - `folder`:
    """
    return dbx.files_list_folder(folder).entries


def analyze_image(image):
    """

    Get the emotion scores for the image from algorithmia
    
    Arguments:
    - `image`: Dropbox locaiton of the image
    """
    params = {}
    params["image"] = "dropbox://" + image
    params["numResults"] = 7

    return algo.pipe(params).result



image_folder = "/images"
images = [image_folder + os.sep + entry.name for entry in get_dropbox_files(image_folder)]
scores = [analyze_image(image) for image in images]


    
## sample upload
file_name='/home/sree/code/emodrive/images/angry.jpg'
upload_path="/images/angry.jpg"

dropbox_image_upload(file_name, upload_path)

    


