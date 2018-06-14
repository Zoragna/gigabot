import os
import json

import discord
import twitter

import random

import string

import time
import datetime

import copy

import pprint

from apscheduler.schedulers.background import BackgroundScheduler

# FAIRE UN SCHEDULER QUI ENVOIE LE JSON

basicBattle = {
    "id" : 0,
    "players" : [],
    "playersHP" : [],
    "opened" : False
}
basicCharacteristics = {
    'strength' : 0,
    'mind' : 0,
    'constitution' : 0,
    'agility' : 0,
    'charisma' : 0,
    'luck' : 0
}
basicPlayer = {
    'name' : '',
    'side' : '',
    'money' : 0,
    'combat' : 0,
    'localization' : '',
    'characteristics' : basicCharacteristics.copy()
}

TOKEN = "NDU2MTQ1MTE5OTEwMDM1NTI3.DgGRxQ.-eMz0x7vqFAd-WP7pXlzA7P6vlo"

storagePath = "Documents\\N7\\Clubs\\NEt7\\GigaGuerre\\"
try :
    os.chdir(storagePath)
except FileNotFoundError :
    print("Already in "+os.getcwd())

def load(dicName) :
    try :
        file = ""
        with open(dicName+".json", "r") as stream :
            for line in stream :
                file += line
        return json.loads(file)
    except FileNotFoundError :
        return dict()
        
def actualize(dic, basicItem):
    for _id in dic.keys() :
        for key in basicItem.keys() :
            if type(dic[_id]) is type(dict()) :
                if not(key in dic[_id].keys()) :
                    dic[_id][key] = basicItem[key]
            else :
                dic[_id] = {}
                dic[_id] = basicItem[key]
        tmp_removal = []
        for key in dic[_id].keys() :
            if not(key in basicItem.keys()):
                tmp_removal.append(key)
        for key in tmp_removal :
            dic[_id].pop(key)

def initDic(dic, key, value):
    if not(key in dic.keys()):
        dic[key] = value

def writeEntry(dic, key, value, fileName):
    dic[key] = value
    refresh(dic, fileName)

def refresh(newDic, dicName):
    print("Refreshing "+dicName+" with "+str(newDic))
    try :
        fileDescriptor = open(dicName+".json","w")
        fileDescriptor.write(json.dumps(newDic))
        fileDescriptor.close()
    except FileNotFoundError :
        print(dicName+" does not exist ! Dictionnary not stored !")

prefix = ">"
embedColor = 0xc08500
messageBeforeStart = "Coucou"    

sched = BackgroundScheduler()
@sched.scheduled_job('cron', hour = 0)
def atMidnight() :
    print("Day has finished !")

sched.start()

players = load('players')
actualize(players, basicPlayer)
refresh(players, 'players')

battles = load('battles')
actualize(battles, basicBattle)
refresh(battles, 'battles')

war = load('war')
if war == {} :
    war = {'maxId' : 0}



print("On going battles :")
print(battles)
print(war)

client = discord.Client()

twi = twitter.Api(  consumer_key='8JjLv2lG9qYZJGwIEIhWte08W',
                    consumer_secret='ljJ65zQPGShB7LciQ4YVMAnZ158Z71tBGii5dGhcJcIThrfVRf',
                    access_token_key='1006620066765524993-MYQIvSS0f8YP5M8Sq2me4XwX8PaN12',
                    access_token_secret='MtH0uDz231zHG8hDTrjXuDN1xM3lamm1Lizs6PnJPoTTU')

@client.event
async def on_message(message):
    now = datetime.datetime.now()
    if message.author.bot :
        return
    else :
        if not(message.author.id in players.keys()) :
            players[message.author.id] = basicPlayer.copy()
            refresh(players, 'players')     
    if message.content.startswith(prefix):
        args = message.content[len(prefix):].split(' ')
        print(message.author, message.content)
        if 'fiche' == args[0] :
            idx_pseudo = 1
            try :
                member = message.mentions[0]
            except IndexError :
                msg = "vous n'avez pas mentionne de joueur :<"
                await client.send_message(message.author, msg)
                return
            if len(args) >= 3 and'creer' == args[2] : # Manque uen protection vis à vis du rôle
                # genre if rôle / elif len / else !
                print(len(args))
                if len(args) == 2*len(basicCharacteristics.keys())+3:
                    charac = basicCharacteristics.copy()
                    s = 0
                    for i in range(0,2*len(basicCharacteristics),2):
                        if args[idx_pseudo+2+i] == 'FP' :
                            charac['strength'] = int(args[idx_pseudo+2+i+1])
                        elif args[idx_pseudo+2+i] == 'FM' :
                            charac['mind'] = int(args[idx_pseudo+2+i+1])
                        elif args[idx_pseudo+2+i] == 'E' :
                            charac['constitution'] = int(args[idx_pseudo+2+i+1])
                        elif args[idx_pseudo+2+i] == 'A' :
                            charac['agility'] = int(args[idx_pseudo+2+i+1])
                        elif args[idx_pseudo+2+i] == 'CHAR' :
                            charac['charisma'] = int(args[idx_pseudo+2+i+1])
                        elif args[idx_pseudo+2+i] == 'CHAN' :
                            charac['luck'] = int(args[idx_pseudo+2+i+1])
                        s += int(args[idx_pseudo+2+i+1])
                    if s == 300 :
                        players[member.id]['characteristics'] = charac
                        refresh(players, 'players')
                        msg = "le personnage de {} a ete enregistre".format(member).format(message)
                        await client.send_message(message.author, msg)
                    else :
                        msg = "la somme des characteristiques vaut {}".format(s).format(message)
                        await client.send_message(message.author, msg)
                else :
                    msg = "format de la creation de fiche non respecte".format(message)
                    await client.send_message(message.author, msg)
            else :
                for member in message.mentions :
                    try :
                        msg = ("Supersona : {name} sous : {money} camp : {side}".format(**players[member.id])).format(message)
                        await client.send_message(message.channel, msg)
                        msg = ''
                        for key in players[member.id]['characteristics'].keys() :
                            msg += key+' : '+str(players[member.id]['characteristics'][key])+' ' 
                        await client.send_message(message.channel, msg.format(message))
                    except KeyError :
                        print("{} n'a pas été enregistré.e".format(member))
        elif 'twitter' == args[0] :
            result = random.choice(twi.GetSearch("VHUniverse")).AsDict()
            msg = ''
            if "urls" in result.keys() :
                if len(result['urls']) > 0 :
                    msg = result["urls"][0]["url"].format(message)
            if "urls" in result["retweeted_status"] :
                if len(result["retweeted_status"]["urls"]) > 0 :
                    msg = result["retweeted_status"]["urls"][0]["url"].format(message)
            if msg != '':
                await client.send_message(message.channel, msg)
        elif 'roll' == args[0] :
            rolls = []
            for roll in args[1:] :
                roll = roll.split('d')
                for _ in range(int(roll[0])):
                    rolls.append(str(random.randint(1,int(roll[1])))+"/"+roll[1])
            msg = str(rolls).format(message)
            await client.send_message(message.channel, msg)
        elif 'combat' == args[0] : 
            # la personne qui a lancé le combat clôt le lobby
            # jets d'initiative 
            # LES JOUEURS DOIVENT LANCER LEUR DES
            print(war)
            print(battles)
            print(players[message.author.id])
            if (len(args) > 1) and (players[message.author.id]['combat'] == 0):
                war['maxId'] = war['maxId'] + 1

                battle = basicBattle.copy()
                battle["id"] =  war['maxId']
                for member in message.mentions :
                    if players[member.id]['combat'] == 0:
                        try :
                            players[member.id]['combat'] = battle["id"]
                            battle["players"].append(member.id)
                            battle["playersHP"].append(players[member.id]['characteristics']['constitution'])
                        except KeyError :
                            msg = str(member)+"n'est pas enregistré".format(message)
                            await client.send_message(message.channel, msg)
                    else :
                        msg = "{} est deja en combat !".format(member).format(message)
                        await client.send_message(message.channel, msg)
                players[message.author.id]['combat'] = battle["id"]
                battle["players"].append(message.author.id)
                battle["playersHP"].append(players[member.id]['characteristics']['constitution'])
                
                battles[battle["id"]] = battle
                
                refresh(players, 'players')
                refresh(war, 'war')
                refresh(battles, 'battles')
                
                print("BATTLE===========")
                print(battle)
                
                str_battle = str(battle).replace('{','').replace('}','')
                
                msg = "{}".format(str_battle).format(message)
                await client.send_message(message.channel, msg)
                for fighter in battle['players'] :
                    await client.send_message(message.server.get_member(fighter), msg) 
            elif players[message.author.id]['combat'] != 0 :
                print(battles[str(players[message.author.id]['combat'])])
                print(str(battles[str(players[message.author.id]['combat'])]))
                str_battle = str(battles[str(players[message.author.id]['combat'])]).replace('{','').replace('}','')
                msg = "Tu es déjà en combat !\n{}".format(str_battle).format(message)
                await client.send_message(message.author, msg)
            else :
                msg = "Tu ne te bats pas, la police te remercie !".format(message)
                await client.send_message(message.author, msg)
        elif 'fuite' == args[0] :
            if players[message.author.id]['combat'] == 0:
                msg = "Tu n'es pas en combat ! :<".format(message)
                await client.send_message(message.author, msg)
            else :
                battles[str(players[message.author.id]['combat'])]['players'].remove(message.author.id)
                msg = "{} a fui !".format(message.author).format(message)
                await client.send_message(message.channel, msg)
                if len(battles[str(players[message.author.id]['combat'])]['players']) == 1 :
                    players[battles[str(players[message.author.id]['combat'])]['players'].pop(0)]['combat'] == 0
                    msg = "Tout le monde a fui !".format(message)
                    await client.send_message(message.channel, msg)
                if len(battles[str(players[message.author.id]['combat'])]['players']) == 0 :
                    battles.pop(str(players[message.author.id]['combat']))
                players[message.author.id]['combat'] = 0
                refresh(battles, "battles")
        elif 'physique' == args[0] :
            if players[message.author.id]['combat'] != 0 :
                if battles[str(players[message.author.id]['combat'])]['players'].index(message.author.id) == 0 :
                    attacked = random.choice(battles[str(players[message.author.id]['combat'])]['players'])
                    msg = "Quelle frappe ! Dix points de dégats infligés à {}".format(message.server.get_member(attacked).mention).format(message)
                    battles[str(players[message.author.id]['combat'])]['playersHP'][ battles[str(players[message.author.id]['combat'])]['players'].index(attacked) ] -= 10
                    battles[str(players[message.author.id]['combat'])]['players'].append(battles[str(players[message.author.id]['combat'])]['players'].pop(0))
                else :
                    print(message.server.get_member(battles[str(players[message.author.id]['combat'])]['players'][0]).mention)
                    msg = "c'est au tour de {}".format(message.server.get_member(battles[str(players[message.author.id]['combat'])]['players'][0]).mention).format(message)
                await client.send_message(message.channel, msg)
        else :
            msg = "Help".format(message)
            await client.send_message(message.author, msg)
    else :
        return 
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(twi.VerifyCredentials())
    print('------')

client.run(TOKEN)