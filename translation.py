import re
import discord
import deepl

auth_key = "your token"
translator = deepl.Translator(auth_key)


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
languages = {"BG": "Bulgarian", "CS": "Czech", "DA": "Danish", "DE": "German", "EL": "Greek", "EN": "English", "EN-GB": "English (British)", "EN-US": "English (American)", "ES": "Spanish", "ET": "Estonian", "FI": "Finnish", "FR": "French", "HU": "Hungarian", "ID": "Indonesian", "IT": "Italian", "JA": "Japanese", "LT": "Lithuanian",
             "LV": "Latvian", "NL": "Dutch", "PL": "Polish", "PT": "Portuguese", "PT-BR": "Portuguese (Brazilian)", "PT-PT": "Portuguese (all Portuguese varieties excluding Brazilian Portuguese)", "RO": "Romanian", "RU": "Russian", "SK": "Slovak", "SL": "Slovenian", "SV": "Swedish", "TR": "Turkish", "UK": "Ukrainian", "ZH": "Chinese (simplified)"}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    global lan
    global user_ids
    if message.author == client.user:
        return
    
    if message.content.startswith("$help"):
        await message.channel.send(', '.join(languages.keys()),"\n","do \"$l <language1>, <language2>\" to add user and language they are using.")
    elif message.content.startswith("$l"):
        lan = []
        m = message.content[3:]
        lan = m.strip(" ").split(",")


        await message.channel.send(', '.join(lan))
    elif message.content.startswith("$f"):
        m = message.content[3:]
        if m =="true":
            formality = "more"
            await message.channel.send("formal")
        elif m =="false":
            formality = "less"
            await message.channel.send("informal")
        else:
            await message.channel.send("formality not valid")

    else:
        any = re.compile(r'(.*?)')
        match = any.search(message.content)
        result = []
        for i in range(len(lan)):
            result.append(translator.translate_text((message.content), target_lang=lan[i]).text)
            
        
        # if message.content.startswith('*'):
        if match:
            await message.channel.send('\n'.join(result))
            # await message.channel.send("function halted")


client.run('your token')
