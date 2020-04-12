import discord
import random
from datetime import datetime
#import tailf
import json

def processInfo(file):
    with open(file, 'r') as myfile:
        data = myfile.read().replace('\n', '')
    data=json.loads(data)

    roomList = {}
    for i in data["roomList"]:
        roomList[int(data["roomList"][i]["id"])] = data["roomList"][i]
        roomList[int(data["roomList"][i]["id"])]["id"] = ""
    return data["config"], roomList

def loadFunc(response):
    @client.event

    async def tailer():
        with tailf.Tail(filename) as tail:
            while True:
                event = await tail.wait_event()
                if isinstance(event, bytes):
                    print(event.decode("utf-8"), end='')
                elif event is tailf.Truncated:
                    print("File was truncated")
                else:
                    assert False, "unreachable" # currently. more events may be introduced later

    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        print("["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]["+message.channel.name+"]["+message.author.name+"] "+message.content)
        if message.author != client.user and message.guild.id in roomList and (message.channel.id in roomList[message.guild.id]["textChannelID"] or "*" in roomList[message.guild.id]["textChannelID"]):
            if message.content.lower() in response:
                await message.channel.send(response[message.content.lower()])
                print("actuation")
        else:
            return

    @client.event
    async def on_typing(channel, user, when):
        if user != client.user and channel.guild.id in roomList and (channel.id in roomList[channel.guild.id]["textChannelID"] or "*" in roomList[channel.guild.id]["textChannelID"]):
            insultos = ["Callate mamagüevo", "Que te calles mamagüevo", "Bueno pero y entonces?", "Bueno mano?", "Tela jeta marico", "Cuándo te callas?", "Hablas más que perico","Qué cotorra eres","Hablas más que humanista","Cierra el pico","Cierra el ocico","Verga chamo callate de una vez","Invocando al Rey de España: POR QUÉ NO TE CALLAS?","Me tienes las bolas colgando marico","Dale el derecho de palabra a alguien que lo merezca más","No puedo soportar tu voz","Si vas a decir algo, prométeme que no será tan inútil como lo otro que dices","Cuidado todo el mundo este bicho está apunto de hablar"]
            await channel.send(insultos[random.randrange(0,len(insultos))]+" "+user.mention)



if __name__ == "__main__":
    (config, roomList) = processInfo("info.json")
    response = {
        "ping":"pong",
        "puta":"tu mamá",
        "coño":"verga",
        "what":"tu me oíste",
        "verga":"coño",
        "🔫":"desenfunda!"
    }
    client = discord.Client()
    loadFunc(response)
    client.run(config["token"])
    print("end")