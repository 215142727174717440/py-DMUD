# to invite a bot, here’s the way you make a link:
#    https://discordapp.com/oauth2/authorize?client_id={CLIENTID}&scope=bot&permissions={PERMISSIONINT}
#the permission int can be calculated on the dicord docs, Flodri used this : 3397696

from init import *

class room():
    """The class used to represent a ROOM
    """
    def __init__(self,desc,exits=set(),players=set()):
        self.desc    = desc
        self.exits   = exits
        self.players = players
    def __repr__(self):
        return f'room(**{self.__dict__.__repr__()})'

class player():
    """The class used to represend a PLAYER
    """
    def __init__(self,idt,x,y,z,inst,pseudo):
        self.idt    = idt
        self.x      = x
        self.y      = y
        self.z      = z
        self.inst   = inst
        self.pseudo = pseudo
    def save(self):
        """SAVE player data
        """
        with open(f'players/{self.idt}.txt', 'w') as fichier:
            fichier.write(self.__repr__())
    def __repr__(self):
        return f'player(**{self.__dict__.__repr__()})'

def load_player(player_id):
    global players
    """LOAD a player object in the players dict with the player_id key
    """
    with open(f'players/{player_id}.txt', 'r') as fichier:
        players[player_id]=eval(fichier.read())

def warn_coming(player_id):
    global toSend
    """If there are other players in the room where player_id goes to,
    warn them player_id has ARRIVED
    """
    p = players[player_id]
    msg = f'{players[player_id].pseudo} заходит. Ну здарова, е&@ть.'
    for player_in_room in world[p.inst][p.x,p.y,p.z].players: #Never empty, there’s at least the 1 player currently in
        if player_in_room!=player_id:toSend.append((player_in_room,msg))

def warn_leaving(player_id,d): #d for direction
    global toSend
    """if there were other players in the room where player_id was,
    tell them that player_id has LEFT
    """
    p = players[player_id]
    for player_in_room in world[p.inst][p.x,p.y,p.z].players: #Never empty, there’s at least the 1 leaving
        if player_in_room!=player_id:
            #for just 2 string, +is faster than .join
            if   d=='n':toSend.append((player_in_room,players[player_id].pseudo+" уходит на **север**. ⬆️"))
            elif d=='s':toSend.append((player_in_room,players[player_id].pseudo+" уходит на **юг**. ⬇"))
            elif d=='e':toSend.append((player_in_room,players[player_id].pseudo+" уходит на **восток**. ➡️"))
            elif d=='o':toSend.append((player_in_room,players[player_id].pseudo+" уходит на **запад**. ⬅️"))  
            elif d=='u':toSend.append((player_in_room,players[player_id].pseudo+" поднимается **выше**. 🆙"))
            elif d=='d':toSend.append((player_in_room,players[player_id].pseudo+" спускается **вниз**. ⏺️"))          

def desc_room(player_id):
    """return a description of the room ready to be sent to the player
    """
    p=players[player_id]
    if (p.x,p.y,p.z) in world[p.inst]:
        room = world[p.inst][p.x,p.y,p.z]
        r = [(p.x,p.y,p.z).__repr__(),'\n',room.desc]
        if len(room.players)>1: #since there’s some player requesting the desc, it’s always at least 1
            r.append('\nТакже поблизости находятся:\n')
            others = room.players.copy()
            others.remove(player_id)
            for player_in_room in others:
                r.append(players[player_in_room].pseudo)
                r.append('\n')
        return ''.join(r)
    else :return "`! inexisting room !`\n(тебе что, собака сутулая, делать нечего?)"

def movement(player_id,d):
    """handle the movement logic of the player
    """
    global players,world
    p=players[player_id]
    if   d==NORTH:
        if NORTH in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.remove(player_id)
            players[player_id].y+=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "На **север** прохода нет. 🚫"
    elif d==EAST  :
        if EAST in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].x+=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "На **восток** прохода нет. 🚫"
    elif d==SOUTH:
        if SOUTH in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].y-=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "На **юг** прохода нет. 🚫"
    elif d==WEST :
        if WEST in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].x-=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "На **запад** прохода нет. 🚫"
    elif d==UP   :
        if UP in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].z+=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "Не подняться здесь **выше**. 🚫"
    elif d==DOWN :
        if DOWN in world[p.inst][p.x,p.y,p.z].exits:
            warn_leaving(player_id,d)
            world[p.inst][p.x,p.y,p.z].players.discard(player_id)
            players[player_id].z-=1
            world[p.inst][p.x,p.y,p.z].players.add(player_id)
            warn_coming(player_id)
            return desc_room(player_id)
        else:return "Не спуститься здесь **вниз**. 🚫"

def cmd_interpreter(player_id,text,msg):
    """Implement the folowing commands in order:
    logout	: disconnects the player
    -		: “say” sends what follows to players in the room
    me/try	: “emote” is used to perform certain custom actions
    look	: returns the room description
    who		: “showlads” returns a list of who’s online
    n/north	: if possible, move the player in said direction
    e/east	: if possible, move the player in said direction
    s/south	: if possible, move the player in said direction
    w/west	: if possible, move the player in said direction
    u/up	: if possible, move the player in said direction
    d/down	: if possible, move the player in said direction
    """
    global players,world,toSend
    if (text == "link start"):
        p = players[player_id]
        world[p.inst][p.x,p.y,p.z].players.add(player_id)
        return ("`**Заходи — не бойся, выходи — не плачь…**`\n> Основано на py-DMUD от Flodri (discord: Flodri#5261). См. также ⚓<https://github.com/flodri/py-DMUD>\n\n" + desc_room(player_id))
    elif (text == "logout") and (player_id in connected):
        p = players[player_id]
        world[p.inst][p.x,p.y,p.z].players.discard(player_id)
        connected.discard(player_id)
        return ("`*Успешно разлогинились!*`")

    ### The '-' command:
    if text.startswith('-'):
        p = players[player_id]
        sendTo = world[p.inst][p.x,p.y,p.z].players.copy()
        sendTo.discard(player_id)
        if len(sendTo)==0:return "Но никто не услышал."
        else:
            msg=f'`{players[player_id].pseudo} : {str(msg.content)[1:]}`'
            for player_in_room in sendTo:toSend.append((player_in_room,msg))
            return msg
        
    ### The “look” command:
    elif text=={'look', 'осмотр', 'осмотреть', 'смотреть', 'смотрю'}:
        return desc_room(player_id)

    ### The “who” command:
    elif text=={'who', 'showlads', 'онлайн'}:
        who=[]
        for p in connected:who.append(players[p].pseudo)
        return str(len(who))+'\n'+'\n'.join(who)
    
    ### The movements commands:
    d=False
    if   text in{'n','north','с','север','⬆️'		}:d=NORTH
    elif text in{'e','east','в','восток','➡️'	}:d=EAST
    elif text in{'s','south','ю','юг','⬇'		}:d=SOUTH
    elif text in{'w','west','з','запад','⬅️'		}:d=WEST
    elif text in{'u','up','вверх','🆙'			}:d=UP
    elif text in{'d','down','вниз','⏺️'			}:d=DOWN
    if d:return movement(player_id,d)

    return '?'



##################################
#End of def, start of game logic :
##################################



with open('world.txt', 'r') as fichier:
    world.update(eval(fichier.read()))
    
for p in os.listdir('./players'):
    load_player(p[:-4])

async def background_toSend():
    """Essential, check regularly the messages that are to be sent"""
    global toSend
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            if len(toSend)!=0:
                print(toSend)
                for m in toSend[:]:
                    await players_channels[m[0]].send(m[1])
                    toSend.remove(m)#can’t use pop and the index as toSend can be modified during the await    
            await asyncio.sleep(0.5) #Repeat after 0.2 s
        except:
            print("!!!!!!! background toSend споткнулся, сучка !!!!!!!'\n")
            await asyncio.sleep(0.1)
            pass

@client.event #event decorator/wrapper
async def on_ready():
    print(f'Logged on as {client.user}')

@client.event #event decorator/wrapper
async def on_message(message):
    
    try : #To have an idea of what’s going on,
          #to comment out if you actually have some amount of activity on your MUD
        print(message.content)
    except : print("##### !!! UN-PRINTABLE !!! #####")
    
    if str(message.author) != "Ну игра чтоб играть в#0964":#otherwise it would answer itself (-_-")
        msg = str(message.content)
        
        if str(message.channel)[0:20]=='Direct Message with ':
            player_id = str(message.author.id)
            text = str(message.content)
            if text=="link start":
                #Already registered:
                if player_id in players:
                    if player_id in connected:
                        await message.channel.send(" *Ваш уровень доступа:* **а вот это уже пацанчик**.")
                    else:
                        players_channels[player_id] = message.channel
                        connected.add(player_id)
                        async with message.channel.typing():
                            await message.channel.send(cmd_interpreter(message))  
                        
                #First connection:
                else:
                    players_channels[player_id] = message.channel
                    #No character creation as is, if you want one you should put it here
                    #instead of the cmd_interpreter(message) part
                    players[player_id]=player(player_id,0,0,0,0,str(message.author))
                    connected.add(player_id)
                    async with message.channel.typing():
                        await message.channel.send(cmd_interpreter(player_id,text,message))

            #If not “link start” and the player is co, we interpret:
            elif player_id in connected:
                async with message.channel.typing():
                    await message.channel.send(cmd_interpreter(player_id,text,message))
            #If not “link start” and is not co, we check if we’re creating a character, if yes interpret acordingly
            #otherwise ignore:
            #elif etat.get(player_id) <=-1:
            #    async with message.channel.typing():
            #        await message.channel.send(crea_FR(message))

        elif str(message.author) in admins:#admins is a set, so hashtable make this pretty fast
            if ("!quit" == msg) :
                #Disconnect your bot.
                await client.close()
                sys.exit()
                
            elif ("!save" == msg):
                #Save everything.   
                for p in players:p.save()
                with open('world.txt', 'w') as fichier:
                    fichier.write(world.__repr__())
                    
            elif ("!save quit"):
                #Save everything, then disconnect your bot.
                for p in players:p.save()
                with open('world.txt', 'w') as fichier:
                    fichier.write(world.__repr__())
                await client.close()
                sys.exit()
        else:
            if ("!who" == msg):
                #Outputs a list of everyone currently online in the MUD.
                who=[]
                for p in connected:who.append(players[p].pseudo)
                message.channel.send(str(len(who))+'\n'+'\n'.join(who))
                
#client.loop.create_task(background_task())
client.loop.create_task(background_toSend())

client.run(TOKEN)
