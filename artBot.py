from bennetsSecrets import *
import tweepy

from PIL import Image, ImageDraw
import random
if (random.randint(1,10) == 9) :
    img = Image.new("RGB", (1200 , 675), (255,255,255))
    drawing_context = ImageDraw.Draw(img)
    drw = ImageDraw.Draw(img, 'RGBA')


    x = random.randint(-100,1300)
    y = random.randint(-75, 775)
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)

    # Create image using 50000 ellipses. Each new dot is slightly
    # differently colored and positioned than the last.  
    for _ in range(50000):
        if random.randint(0,1) == 0 and x > -50:
            x = x - random.randint(0,50)
        elif x < 1250:
            x = x + random.randint(0,50)
        else:
            x = x - random.randint(0,50)


        if random.randint(0,1) == 0 and y > -50:
            y = y - random.randint(0,50)
        elif y < 725:
            y = y + random.randint(0,50)
        else:
            y= y - random.randint(0,50)
        
        if random.randint(0,1) == 0 and r > 0:
            r = r - random.randint(0,4)
        elif r < 255:
            
            r = r + random.randint(0,4)
        else:
            r = r - random.randint(0,4)


        if random.randint(0,1) == 0 and g > 0:
            g = g - random.randint(0,4)
        elif g < 255:
            g = g + random.randint(0,4)
        else:
            g = g - random.randint(0,4)

        if random.randint(0,1) == 0 and b > 0:
            b = b - random.randint(0,4)
        elif b < 255:
            b = b + random.randint(0,4)
        else:
            b = b - random.randint(0,4)
            
        drw.ellipse([x, y, x + 100, y + 100], fill = (r,g,b, 5))
      
    img.save("/Users/bennet/Programming/artBot/test.png")

    client = tweepy.Client(bearer_token = BEARER_TOKEN, consumer_key=API_KEY, consumer_secret=API_KEY_SECRET, access_token=ACCESS_TOKEN, access_token_secret= ACCESS_TOKEN_SECRET)
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
  
    file_name = "/Users/bennet/Programming/artBot/test.png"
    upload = api.media_upload(file_name)
    client.create_tweet(text= "#Art #Bot #Artbot #Wallpaper", media_ids=[upload.media_id_string])
