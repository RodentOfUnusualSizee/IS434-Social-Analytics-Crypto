## Getting last date of data 

import pandas as pd
dfOld = pd.read_csv(
    "../textData/discord.csv", encoding="ISO-8859-1")

lastDate = dfOld['date'][0]



## getting new data to from present to lastDate

import requests
import json

headers = {
    'authorization': 'MzM0ODY3MDQ3MDIyNDYwOTMx.YiG5KA.xXckGG7feFGQe87AZCOdICWJSOc'
    }
end = lastDate
end = end.split("/")
endyear = end[2]
endmonth = end[1]  
if len(endmonth) == 1:
    endmonth = "0"+endmonth
endday = end[0]  
if len(endday) == 1:
    endday = "0"+endday
endcomb = endyear+endmonth+endday
endDate = int(endcomb)
def retrive_messages(serverName,channelName, channelid):
    r = requests.get('https://discord.com/api/v9/channels/' +
                    channelid+'/messages?limit=100', headers=headers)

    fullJson = []
    jsonn = json.loads(r.text)
    fullJson.extend(jsonn)

    counter = 1
    maxcounter = 2 # if max counter = 10, we will scrape 10*100 messages
    

    while len(r.text) == 100 or counter != maxcounter:
        try:
            lstmsg = jsonn[99]
            lstmsgID = lstmsg['id']
            r = requests.get('https://discord.com/api/v9/channels/' +
                        channelid+'/messages?limit=100&before='+lstmsgID, headers=headers)
            jsonn = json.loads(r.text)
            
            ## check if data has been caught up
            lastTimestamp = jsonn[len(jsonn)-1]['timestamp']
            dateData = lastTimestamp.split("T")[0].split("-")
            year = dateData[0]
            month = dateData[1]    
            day = dateData[2]   
            comb = year+month+day
            comb = int(comb)
            print(comb ,endDate)
            if comb <= endDate:
                print("hit last date")
                break
            else:    
                fullJson.extend(jsonn)
                print('lastMsgId', lstmsgID)
                print("scrapping channel id: "+channelid +
                      " 100 x "+str(counter)+" scrapped")
                counter += 1
        except:
            print("end of total message")
            break

    for i in range(0, len(fullJson)):
        fullJson[i]['serverName'] = serverName
        fullJson[i]['channelName'] = channelName

    print("scrapped finished : "+serverName+"-"+channelName +
          " total no of message:" + str(len(fullJson)))
    return fullJson


channelList= [
    ['SushiSwap Community','Price Talk','749777962995548210'],
    ['SushiSwap Community','sushi-dao','748033004323995680'],
    ['SushiSwap Community','General','748031363935895556'],
    ['r/CryptoCurrency','crypto-trading','679137528153899039'],
    ['r/CryptoCurrency','technical-analysis','864653165680918528'],
    ['r/CryptoCurrency','market-outlook','831648840586100846'],
    ['Cryptodra','crypto-chat','922148826133966898'],
    ['Cryptodra','-analysis','922149162437443624'],
    ['Official /r/wallstreetbets','crypto-trading','881514481845403699'],
    ['Larva Labs','cryptopunks','567343234687303700'],
]

mainList = []

left = 1
total = len(channelList)
for channelDetails in channelList:
    mainList.extend(retrive_messages(channelDetails[0], channelDetails[1] ,channelDetails[2]))
    print(left,"/",total)
    left += 1


dfNew=pd.DataFrame.from_records(mainList)
messageID = dfNew['id']
author_id = []
author_username = []
content = dfNew['content']
timestamp = dfNew['timestamp']
serverName = dfNew['serverName']
channelName = dfNew['channelName']
date = []
for i in dfNew['author']:
    author_id.append(i['id'])
    author_username.append(i['username'])    

for i in dfNew['timestamp']:
    dateData = i.split("T")[0].split("-")
    year = dateData[0]
    month = dateData[1]    
    day = dateData[2]   
    output = day+'/'+month+'/'+year
    date.append(output)

d = {'messageID':messageID,'author_id':author_id,'author_username':author_username,'content':content,'timestamp':timestamp,'serverName':serverName,'channelName':channelName,'date':date}
df = pd.DataFrame(data=d)

finalDF = pd.concat([df,dfOld])
finalDF.to_csv("../textData/newdiscord.csv")