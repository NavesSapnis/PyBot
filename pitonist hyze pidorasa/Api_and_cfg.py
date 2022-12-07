token=""

with open("config\cfg.txt", "r") as f:
    text = f.read(100)

try:
    text=text.split()
    id=int(text[2])
    token=text[5]
except:
    pass

with open("config\pic_i.txt", "r") as f:
    text_i = f.read(100)
    pic_i=text_i


API_TOKEN = f"{token}"
CLIENT_ID="02ae4e958d6aac4"
path="pictures\\test.jpg"