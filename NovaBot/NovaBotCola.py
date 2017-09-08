import discord
from discord.ext import commands
import asyncio
import time
import datetime
import random

#from discord.ext.commands import Bot

#Client = discord.Client #I think I can ignore this
bot_prefix = 'n!'
client = commands.Bot(command_prefix=bot_prefix)
whitelist = ['210628530545885185', '187013842532827136' ,'89991729486245888' ,'305526265610502144', '212402356787085312']
married = []
economy = []
## balance = [-9:]
## name = [:-9]
##89991729486245888.000000100
online_msg = 'NovaBot Online'


#210628530545885185 Matt
#187013842532827136 Shea
#89991729486245888 John
#305526265610502144 Chris
#212402356787085312 Cody


##@client.event
##async def on_command_error(error, ctx):
##    print_text = ''   
##    if isinstance(error, commands.MissingRequiredArgument):
##        await client.send_message(ctx.message.channel, "! Missing Arguments")
##        print_text = 'Missing Arguments'
##    elif isinstance(error, commands.BadArgument):
##        await client.send_message(ctx.message.channel, "! Bad Arguments -- If your words have spaces, try using quotes")
##        print_text = 'Bad Arguments'
##    print('ERROR - {} {} {} in {} : {}'.format(print_text, str(datetime.datetime.now())[:-7], user(ctx), ctx.message.channel, ctx.message.content))
##

eco_file = open('economy.txt', 'r')
economy = eco_file.read().split('\n')

    
@client.event
async def on_ready():
    print(str(datetime.datetime.now())[:-7], online_msg)

# appends (output) to modlog.txt
def modlog(output):
    mod_log = open('modlog.txt','a')
    mod_log.write(output + '\n')
    mod_log.close()

# prepares command context for logging
def log_dat(c):
    return '{} {} in {} : {} : '.format(str(datetime.datetime.now())[:-7], c.message.author, c.message.channel, c.message.content)

# prints and appends to modlog.txt the command context and command-specific output
def loggify(c, output=''):
    print(log_dat(c) + output)
    modlog(log_dat(c) + output)

# readability shortcut, returns user who entered command           
def user(context):
    return context.message.author

# returns True if message author is NovaBot
def is_me(m):
    return m.author == client.user

# returns True if message author is not NovaBot
def isnt_me(m):
    return m.author != client.user


# shipper takes two integers based on user and target ID, 'combines' them, creates a hash, and returns the middle three numbers as a string.
#   being used in a percentage, if the number is greather than 100 it returns only the right-most two digits
def shipper(arg1, arg2):
    if arg1 == arg2:
        return '100'
    num = arg1*arg2
    num = hash(num)
    num = str(num)[3:6]
    num = int(num)
    if num > 100:
        num = str(num)[-2:]
    num = str(num)
    return num

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


##@client.event()
##async def

##@client.command(pass_context=True)
##async def econ(ctx):
##    pass
##    for i in economy:
##        if 
def getmemberid(name):
    for server in client.servers:
        if str(server) == 'NovaBros':
            for i in server.members:
                if str(i)[:-5] == name:
                    return i.id

@client.command(pass_context=True)
async def econ(ctx):
    bux = 0
    for i in economy:
        if i[:-10] == str(ctx.message.author.id):
            bux = int(i[-9:])
            await client.send_message(ctx.message.channel, '{} has {} novabux'.format(str(ctx.message.author)[:-5], bux))
    loggify(ctx, '{} has {} novabux'.format(str(ctx.message.author)[:-5], bux))



@client.command(pass_context=True)
async def getnum(ctx):
    num = 0
    for server in client.servers:
        if str(server)=='NovaBros':
            for i in server.members:
                num += 1
    print(num)
    await client.send_message(ctx.message.channel, 'NovaBros has {} members'.format(num))

# \!/ \/ \!/ LOTS OF ERROR POTENTIAL IN THIS ONE \!/ \/ \!/
@client.command(pass_context=True)
async def pay(ctx, target, number):
    loggify(ctx)
##    modlog(log_dat(ctx) + ctx.message.content)
    if target != str(ctx.message.author)[:-5]:
        econ_index_send = 0     # unique ID of sending user
        econ_index_receive = 0      # unique ID of receiving user
        send_id = str(ctx.message.author.id)
        receive_id = getmemberid(target)
        # find and assign unique IDs
        for i in economy:
            if i[:-10] == str(ctx.message.author.id):
                econ_index_send = economy.index(i)
            elif i[:-10] == getmemberid(target):
                econ_index_receive = economy.index(i)
        # check if sender has enough dosh, then send dosh
        if int(economy[econ_index_send][-9:]) >= int(number):
            new_string_value = ''
            new_string_valueR = ''
            new_value = str(int(economy[econ_index_send][-9:]) - int(number))
            new_valueR = str(int(economy[econ_index_receive][-9:]) + int(number))
            length = len(new_value)
            lengthR = len(new_valueR)
            new_string_value = (9 - length) * '0' + new_value
            new_string_valueR = (9 - lengthR) * '0' + new_valueR
            economy[econ_index_send] = send_id + '.' + new_string_value
            economy[econ_index_receive] = receive_id + '.' + new_string_valueR
##            print(new_string_value)
##            print(new_value)
##            print(economy[econ_index_send])
            eco_file = open('economy.txt', 'w')
            for i in economy:
                eco_file.write(i + '\n')
            await client.send_message(ctx.message.channel, ':dollar: {} novabux successfully sent to {}'.format(number, target))
        elif int(economy[econ_index_send][-9:]) < int(number):
            await client.send_message(ctx.message.channel, 'You\'re too poor to do that, you only have {}'.format(int(economy[econ_index_send][-9:])))
            

@client.command(pass_context=True)
async def payoutDONTUSE(ctx):
    if str(ctx.message.author.id) in whitelist:
        eco_file = open('economy.txt', 'w')
        for server in client.servers:
            if str(server) == 'NovaBros':
                for i in server.members:
                    eco_file.write(i.id + '.000000100\n')
        eco_file.close()
        loggify(ctx)   
        
@client.command(pass_context=True)
async def test(ctx):
    for i in ctx.message.channel.server.channels:
        if str(i) == 'HotS':
            voice = await client.join_voice_channel(i)
    player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    player.start()

@client.command(pass_context=True)
async def lenny(ctx):
    loggify(ctx, 'Sending lenny')
##    modlog(log_dat(ctx) + ctx.message.content)
    await client.send_message(ctx.message.channel, '( ͡° ͜ʖ ͡°)')
##    modlog('lenny')
    
@client.command(pass_context=True)
async def roll(ctx, num=20, num2=1):
    if num2 > 5:
        num2 = 5
    for i in range(num2):
        x = random.randint(1, (int(num)))
        modlog(log_dat(ctx) + 'Rolled {}/{}'.format(x, num))
        await client.send_message(ctx.message.channel, '`{} rolled {}`'.format(str(user(ctx))[:-5] , x))

@client.command(pass_context=True)
async def remind(ctx, arg1='', arg2=5, arg3=0):
    if is_int(arg1):
        arg3 = arg2
        arg2 = arg1
        arg1 = ''
    await client.send_message(ctx.message.channel, 'Reminder set for {} minutes and {} seconds'.format(arg2, arg3))
    log_output = '{} {} in {} : Reminder \'{}\' set for {} minutes and {} seconds'.format(str(datetime.datetime.now())[:-7], user(ctx), ctx.message.channel, arg1, arg2, arg3)
    modlog(log_output)
    print(log_output)
    wait_time = int(arg2)*60 + int(arg3)
    await asyncio.sleep(wait_time)
    log_output = '{} {} in {} : Reminder \'{}\' calling after {} minutes {} seconds'.format(str(datetime.datetime.now())[:-7], user(ctx), ctx.message.channel, arg1, arg2, arg3)
    modlog(log_output)
    await client.send_message(ctx.message.channel, 'Hey {}, it\'s time for your {} reminder'.format(str(user(ctx))[:-5], arg1), tts=True)
                              
@client.command(pass_context=True)
async def fib(ctx, num):
    num = int(num)
    i=2
    a,b=0,1
    while i < num:
        a,b=b,a+b
        i+=1
        if i == num:
            await client.send_message(ctx.message.channel, '`fib {} is {}`'.format(num, b))

@client.command(pass_context=True)
async def ship(ctx, arg1, arg2):
    num1 = int(str(ctx.message.channel.server.get_member_named(arg1))[-4:])
    num2 = int(str(ctx.message.channel.server.get_member_named(arg2))[-4:])
    num = shipper(num1, num2)
    thing = 'a'
    if int(num) < 10:
        num = num[-1:]
    if num[0:1] == '8' or num == '18':
        thing = 'an'
    output_message = '{} and {} are {} {}% match'.format(arg1, arg2, thing, num)
    modlog(log_dat(ctx) + output_message)
    if int(num) > 90:
        output_message = output_message + '   ( ͡° ͜ʖ ͡°)'
    await client.send_message(ctx.message.channel, output_message)
    print(log_dat(ctx) + output_message)
    
@client.command(pass_context=True)
async def whr(ctx):
    log_output = 'User: {}, Channel: {}'.format(user(ctx), ctx.message.channel)
    print(log_output)
    if str(user(ctx).id) in whitelist:
        print('Whitelist Accept')
        print(str(user(ctx).id))
    else:
        print('Whitelist Deny')
        print(str(user(ctx).id))

@client.command(pass_context=True)
async def bing(ctx, num=1, buffer=0):
    if str(ctx.message.author.id) in whitelist:
        num = int(num)
        pingtime = time.time()
        log_output = '{} {} in {} : Bing {} times with {} seconds buffer'.format(str(datetime.datetime.now())[:-7], user(ctx), ctx.message.channel, num, buffer)
        print(log_output)
        for i in range(num):
            ping = time.time() - pingtime
            pingtime = time.time()
            await client.send_message(ctx.message.channel, '`Bong {} ms`'.format(round(ping*1000, 2)))
            await asyncio.sleep(int(buffer))
        print('{} Bing complete'.format(str(datetime.datetime.now())[:-7]))
        
@client.command(pass_context=True)
async def ping(ctx, num=1, buffer=0):
    if str(ctx.message.author.id) in whitelist:
        num = int(num)
        pingtime = time.time()
        log_output = 'Ping {} times with {} seconds buffer'.format(num, buffer)
        loggify(ctx, log_output)
        for i in range(num):
            ping = time.time() - pingtime
            pingtime = time.time()
            await client.send_message(ctx.message.channel, '`Pong {} ms`'.format(round(ping*1000, 2)))
            await asyncio.sleep(int(buffer))
        print('{} Ping complete'.format(str(datetime.datetime.now())[:-7]))
            
@client.command(pass_context=True)
async def find(ctx):
    loggify(ctx, 'Blah blah blah, this is the second part')

@client.command(pass_context = True)
async def nbspeak(ctx, channel, message):
    if str(ctx.message.author.id) in whitelist:
        for i in ctx.message.channel.server.channels:
            if str(i) == channel:
                await client.send_message(i, message)
                output_message = 'Speaking as NovaBot in {}, {}'.format(i, message)
                loggify(ctx, output_message)
        
@client.command(pass_context = True)
async def clear(ctx, num=1, name=''):
    if str(ctx.message.author.id) in whitelist:
        if name == '':
            loggify(ctx, 'Clearing {} messages'.format(num))
            mgs = []
            num = int(num) + 1
            async for i in client.logs_from(ctx.message.channel, limit=num):
                if i.pinned != True:
                    mgs.append(i)
            await client.delete_messages(mgs)
        elif name != '':
            target = ctx.message.channel.server.get_member_named(name)
            loggify(ctx, 'Clearing {} from last {} messages'.format(str(target)[:-5], num))
            mgs = []
            num = int(num) + 1
            async for i in client.logs_from(ctx.message.channel, limit=num):
                if i.author == target or i.content == ctx.message.content:
                    if i.pinned != True:
                        mgs.append(i)
            await client.delete_messages(mgs)



@client.command(pass_context = True)
async def add(ctx, num1, num2):
    log_output = '{} {} in {} : Adding {}, {}'.format(str(datetime.datetime.now())[:-7], user(ctx), ctx.message.channel, num1, num2)
    print(log_output)
    ans = int(num1) + int(num2)
    return await client.send_message(ctx.message.channel,'{} + {} = {}'.format(num1, num2, ans))

client.run('MzE2OTAwMTg1ODU2OTMzODg4.DEFRdw.F1vlxTgAQmVdmMHA9LEVjRJOmGU')
