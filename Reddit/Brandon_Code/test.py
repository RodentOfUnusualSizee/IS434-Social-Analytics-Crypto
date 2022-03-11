import requests
import shutil

url = "https://scontent-bru2-1.cdninstagram.com/v/t51.2885-15/275440088_359934012516245_1406423334571149469_n.jpg?stp=dst-jpg_e35&_nc_ht=scontent-bru2-1.cdninstagram.com&_nc_cat=105&_nc_ohc=2kuPyI9n2Z4AX-BIDdx&edm=AABBvjUBAAAA&ccb=7-4&ig_cache_key=Mjc5MDA0MzA3MjY4MTgxNjY5NQ%3D%3D.2-ccb7-4&oh=00_AT-PWbeqIp47nANQeQsDMKZpktXkXI7lBE_PWuZIpcQlqw&oe=62304E26&_nc_sid=83d603"

url_filename = url.split("/")[-2] + ".png"
print(url_filename)


r = requests.get(url, stream=True)

if r.status_code == 200:
    r.raw.decode_content = True

    with open(url_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
        
        print("Image successfully Downloaded:", url_filename)
else:
    print("Unable to download the image")