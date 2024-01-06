from imageProviders.DalleProvider import DalleProvider

dalleKeyFile = open("dalle.key", "r")
dalleKey = dalleKeyFile.read()

dalleProvider = DalleProvider(key=dalleKey);
img = dalleProvider.get_image_from_string(text="test")