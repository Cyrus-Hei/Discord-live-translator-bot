import re
import discord
import deepl

auth_key = "tokenhere"
translator = deepl.Translator(auth_key)


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
languages = {"BG": "Bulgarian", "CS": "Czech", "DA": "Danish", "DE": "German", "EL": "Greek", "EN": "English", "EN-GB": "English (British)", "EN-US": "English (American)", "ES": "Spanish", "ET": "Estonian", "FI": "Finnish", "FR": "French", "HU": "Hungarian", "ID": "Indonesian", "IT": "Italian", "JA": "Japanese", "LT": "Lithuanian",
             "LV": "Latvian", "NL": "Dutch", "PL": "Polish", "PT": "Portuguese", "PT-BR": "Portuguese (Brazilian)", "PT-PT": "Portuguese (all Portuguese varieties excluding Brazilian Portuguese)", "RO": "Romanian", "RU": "Russian", "SK": "Slovak", "SL": "Slovenian", "SV": "Swedish", "TR": "Turkish", "UK": "Ukrainian", "ZH": "Chinese (simplified)"}
langhelp =""
for l in languages.items():
    langhelp+= l[0]+":"+l[1]+"\n"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global lanuser
    global lan
    global user_ids
    if message.author == client.user:
        return
    
    if message.content.startswith("$help"):
        await message.channel.send(langhelp
                                   +"do ```$l @<username> <language>``` to add users and language they are using.\n")
    elif message.content.startswith("$s"):
        lanuser = []
        await message.channel.send("translation stopped")
    elif message.content.startswith("$l"):
        users = message.mentions
        user_ids = []
        lanuser = []
        lan = []
        for user in users:
            if not(user):
                await message.channel.send('no user found')
            user_ids.append(user.id)
        
        userID = user.id
        m = message.content[3:]
        temp = m.split(",")
        print(temp)
        for i in range(len(temp)):
            lanuser.append([user_ids[i],temp[i].split(" ")[-1]])
            if lanuser[i][-1] not in lan:
                lan.append(lanuser[i][-1])
        print(lanuser,lan)

        await message.channel.send("assigned languages")

    else:
        any = re.compile(r'(.*?)')
        match = any.search(message.content)
        result = []
        for i in range(len(lanuser)):
            if lanuser[i][0] == message.author.id:
                for j in range(len(lan)):
                    if lan[j] != lanuser[i][-1]:
                        
                        result.append(translator.translate_text((message.content), target_lang=lan[j]).text)

                if match:
                    await message.channel.send("from "+message.author.name+':\n'+'\n'.join(result))
                break


client.run('tokenhere')


