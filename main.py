import discord
import random
from datetime import datetime
import tailf
import json
import asyncio
import traceback
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
    async def tailer(bootOrigin):
        address = bootOrigin.content.split()[1]
        try:
            with tailf.Tail(address) as tail:
                while True:
                    event = await tail.wait_event()
                    if isinstance(event, bytes):
                        newText = event.decode("utf-8")
                        print(newText, end="")
                        await bootOrigin.channel.send(newText)
                    elif event is tailf.Truncated:
                        print("File was truncated")
                    else:
                        assert False, "unreachable" # currently. more events may be introduced later
        except:
            bootOrigin.channel.send("No se encontró el archivo.")

    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    async def spam(bootOrigin):
        while True:
            await bootOrigin.channel.send("abcdefghijklmnopqrstuvwxyz"[random.randrange(0,25)])
            await asyncio.sleep(0.05)
        
    @client.event
    async def on_message(message):
        print("["+datetime.now().strftime("%d/%m/%Y %H:%M:%S")+"]["+message.channel.name+"]["+message.author.name+"] "+message.content)
        if message.author != client.user and message.guild.id in roomList and (message.channel.id in roomList[message.guild.id]["textChannelID"] or "*" in roomList[message.guild.id]["textChannelID"]):
            if message.content.lower() in response:
                await message.channel.send(response[message.content.lower()])
                print("actuation")
            if message.content.split()[0] == "boothere":
                taskTailf = asyncio.create_task(tailer(message))
                await taskTailf
            if message.content == "spamhere":
                taskSpam = asyncio.create_task(spam(message))
                taskSpam
                await asyncio.sleep(30)
                taskSpam.cancel()
            if message.content == "stopspam":
                try:
                    await taskSpam.cancel()
                    await message.channel.send("ok pues")
                except:
                    await message.channel.send("No.")
                    await message.channel.send(traceback.format_exc())
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