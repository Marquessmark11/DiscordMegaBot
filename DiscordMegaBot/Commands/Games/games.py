import discord
from discord.ext import commands
import random
import asyncio
import copy
import upsidedown
from discord.ext import ui
import time
from discord.ext import menus

class MyMenu(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        self.playing_user = random.choice(ctx.playing_users)
        for index in range(len(ctx.playing_users)):
            if ctx.playing_users[index] == self.playing_user:
                self.playing_symbol = ctx.symbols[index]
            else:
                self.other_playing_symbol = self.ctx.symbols[index]
                self.other_playing_user = self.ctx.playing_users[index]
        self.dictofplaces = ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']
        resp = ''
        for index in range(len(self.dictofplaces)):
            if index in (2, 5):
                resp += (self.dictofplaces[index] + '\n')
                continue
            resp += self.dictofplaces[index]
        return await channel.send(resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in ctx.playing_users])}. It is {self.ctx.bot.get_user(self.playing_user).name}'s turn.\n{self.ctx.bot.get_user(self.playing_user).name} is {self.playing_symbol}\n{self.ctx.bot.get_user(self.other_playing_user).name} is {self.other_playing_symbol}")
    
    @menus.button('1\U000020e3')
    async def on_digit_one(self, payload):
        if self.dictofplaces[0] != '⬜':
            await self.ctx.send(f'<@!{payload.user_id}>, that place exists already!')
            return
        else:
            if self.playing_user == payload.user_id:
                if self.playing_user == self.ctx.buddy:
                    for index in range(len(self.dictofplaces)):
                        if self.dictofplaces[index] == chr(10060) and self.dictofplaces[index+1] == chr(10060) and self.dictofplaces[index+2] == chr(10060):
                            await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                            self.stop()
                        if self.dictofplaces[index] == chr(10060) and self.dictofplaces[index+5] == chr(10060) and self.dictofplaces[index+4] == chr(10060):
                            await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                            self.stop()
                else:
                    for index in range(len(self.dictofplaces)):
                        if self.dictofplaces[index] == chr(11093) and self.dictofplaces[index+1] == chr(11093) and self.dictofplaces[index+2] == chr(11093):
                            await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                            self.stop()
                        if self.dictofplaces[index] == chr(11093) and self.dictofplaces[index+5] == chr(11093) and self.dictofplaces[index+4] == chr(11093):
                            await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                            self.stop()
                    self.dictofplaces[0] = chr(11093)
                resp = ''
                for index in range(len(self.dictofplaces)):
                    if index in (2, 5):
                        resp += (self.dictofplaces[index] + '\n')
                        continue
                    resp += self.dictofplaces[index]
                if self.playing_user == self.ctx.buddy:
                    self.playing_user = self.ctx.playing_users[1]
                else:
                    self.playing_user = self.ctx.playing_users[0]
                await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
            else:
                await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('2\U000020e3')
    async def on_digit_two(self, payload):
        if self.playing_user == payload.user_id:
            if self.playing_user == self.ctx.buddy:
                self.dictofplaces[1] = chr(10060)
            else:
                self.dictofplaces[1] = chr(11093)
            resp = ''
            for index in range(len(self.dictofplaces)):
                if index in (2, 5):
                    resp += (self.dictofplaces[index] + '\n')
                    continue
                resp += self.dictofplaces[index]
            if self.playing_user == self.ctx.buddy:
                self.playing_user = self.ctx.playing_users[1]
            else:
                self.playing_user = self.ctx.playing_users[0]
            await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
        else:
            await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('3\U000020e3')
    async def on_digit_three(self, payload):
        if self.playing_user == payload.user_id:
            if self.playing_user == self.ctx.buddy:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(10060) and self.dictofplaces[index-1] == chr(10060) and self.dictofplaces[index-2] == chr(10060):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[2] = chr(10060)
            else:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(11093) and self.dictofplaces[index-1] == chr(11093) and self.dictofplaces[index-2] == chr(11093):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[2] = chr(11093)
            resp = ''
            for index in range(len(self.dictofplaces)):
                if index in (2, 5):
                    resp += (self.dictofplaces[index] + '\n')
                    continue
                resp += self.dictofplaces[index]
            if self.playing_user == self.ctx.buddy:
                self.playing_user = self.ctx.playing_users[1]
            else:
                self.playing_user = self.ctx.playing_users[0]
            await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
        else:
            await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('4\U000020e3')
    async def on_digit_four(self, payload):
        if self.playing_user == payload.user_id:
            if self.playing_user == self.ctx.buddy:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(10060) and self.dictofplaces[index+1] == chr(10060) and self.dictofplaces[index+2] == chr(10060):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[3] = chr(10060)
            else:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(11093) and self.dictofplaces[index+1] == chr(11093) and self.dictofplaces[index+2] == chr(11093):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[3] = chr(11093)
            resp = ''
            for index in range(len(self.dictofplaces)):
                if index in (2, 5):
                    resp += (self.dictofplaces[index] + '\n')
                    continue
                resp += self.dictofplaces[index]
            if self.playing_user == self.ctx.buddy:
                self.playing_user = self.ctx.playing_users[1]
            else:
                self.playing_user = self.ctx.playing_users[0]
            await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
        else:
            await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('5\U000020e3')
    async def on_digit_five(self, payload):
        if self.playing_user == payload.user_id:
            if self.playing_user == self.ctx.buddy:
                self.dictofplaces[4] = chr(10060)
            else:
                self.dictofplaces[4] = chr(11093)
            resp = ''
            for index in range(len(self.dictofplaces)):
                if index in (2, 5):
                    resp += (self.dictofplaces[index] + '\n')
                    continue
                resp += self.dictofplaces[index]
            if self.playing_user == self.ctx.buddy:
                self.playing_user = self.ctx.playing_users[1]
            else:
                self.playing_user = self.ctx.playing_users[0]
            await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
        else:
            await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('6\U000020e3')
    async def on_digit_six(self, payload):
        if self.playing_user == payload.user_id:
            if self.playing_user == self.ctx.buddy:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(10060) and self.dictofplaces[index-1] == chr(10060) and self.dictofplaces[index-2] == chr(10060):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[5] = chr(10060)
            else:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(11093) and self.dictofplaces[index-1] == chr(11093) and self.dictofplaces[index-2] == chr(11093):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[5] = chr(11093)
            resp = ''
            for index in range(len(self.dictofplaces)):
                if index in (2, 5):
                    resp += (self.dictofplaces[index] + '\n')
                    continue
                resp += self.dictofplaces[index]
            if self.playing_user == self.ctx.buddy:
                self.playing_user = self.ctx.playing_users[1]
            else:
                self.playing_user = self.ctx.playing_users[0]
            await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
        else:
            await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('7\U000020e3')
    async def on_digit_seven(self, payload):
        if self.playing_user == payload.user_id:
            if self.playing_user == self.ctx.buddy:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(10060) and self.dictofplaces[index+1] == chr(10060) and self.dictofplaces[index+2] == chr(10060):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[6] = chr(10060)
            else:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(11093) and self.dictofplaces[index+1] == chr(11093) and self.dictofplaces[index+2] == chr(11093):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[6] = chr(11093)
            resp = ''
            for index in range(len(self.dictofplaces)):
                if index in (2, 5):
                    resp += (self.dictofplaces[index] + '\n')
                    continue
                resp += self.dictofplaces[index]
            if self.playing_user == self.ctx.buddy:
                self.playing_user = self.ctx.playing_users[1]
            else:
                self.playing_user = self.ctx.playing_users[0]
            await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
        else:
            await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('8\U000020e3')
    async def on_digit_eight(self, payload):
        if self.playing_user == payload.user_id:
            if self.playing_user == self.ctx.buddy:
                self.dictofplaces[7] = chr(10060)
            else:
                self.dictofplaces[7] = chr(11093)
            resp = ''
            for index in range(len(self.dictofplaces)):
                if index in (2, 5):
                    resp += (self.dictofplaces[index] + '\n')
                    continue
                resp += self.dictofplaces[index]
            if self.playing_user == self.ctx.buddy:
                self.playing_user = self.ctx.playing_users[1]
            else:
                self.playing_user = self.ctx.playing_users[0]
            await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
        else:
            await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('9\U000020e3')
    async def on_digit_nine(self, payload):
        if self.playing_user == payload.user_id:
            if self.playing_user == self.ctx.buddy:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(10060) and self.dictofplaces[index-1] == chr(10060) and self.dictofplaces[index-2] == chr(10060):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[8] = chr(10060)
            else:
                for index in range(len(self.dictofplaces)):
                    if self.dictofplaces[index] == chr(11093) and self.dictofplaces[index-1] == chr(11093) and self.dictofplaces[index-2] == chr(11093):
                        await self.ctx.send(f'<@!{payload.user_id}>, you won!')
                        self.stop()
                self.dictofplaces[8] = chr(11093)
            resp = ''
            for index in range(len(self.dictofplaces)):
                if index in (2, 5):
                    resp += (self.dictofplaces[index] + '\n')
                    continue
                resp += self.dictofplaces[index]
            if self.playing_user == self.ctx.buddy:
                self.playing_user = self.ctx.playing_users[1]
            else:
                self.playing_user = self.ctx.playing_users[0]
            await self.message.edit(content=resp + f"\nThere are 2 players, {', '.join([self.ctx.bot.get_user(id).name for id in self.ctx.playing_users])}. It is now {self.ctx.bot.get_user(self.playing_user).name}'s turn")
        else:
            await self.ctx.send(f'<@!{payload.user_id}>, its not your turn!')
    
    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()
    
    def reaction_check(self, payload):
        """The function that is used to check whether the payload should be processed.
        This is passed to :meth:`discord.ext.commands.Bot.wait_for <Bot.wait_for>`.
        There should be no reason to override this function for most users.
        Parameters
        ------------
        payload: :class:`discord.RawReactionActionEvent`
            The payload to check.
        Returns
        ---------
        :class:`bool`
            Whether the payload should be processed.
        """
        if payload.message_id != self.message.id:
            return False
        if payload.user_id not in {*self.ctx.playing_users}:
            return False
        return payload.emoji in self.buttons

class TestMover(menus.Menu):
    async def send_initial_message(self, ctx, channel):
        self.listofplaces = ['⬜', '⬜', '⬜', '⬜', '😳', '⬜', '⬜', '⬜', '⬜']
        self.onebarlength = 3
        self.snakePos = 4
        resp = ''
        for place in range(len(self.listofplaces)):
            if place in (2, 5):
                resp += (self.listofplaces[place] + '\n')
                continue
            resp += self.listofplaces[place]
        return await ctx.send(resp)
    
    @menus.button('\N{LEFTWARDS BLACK ARROW}')
    async def on_left_arrow(self, payload):
        try:
            pSnakePos = self.snakePos
            self.snakePos -= 1
            self.listofplaces[self.snakePos] = '😳'
            self.listofplaces[pSnakePos] = '⬜'
            resp = ''
            for place in range(len(self.listofplaces)):
                if place in (2, 5):
                    resp += (self.listofplaces[place] + '\n')
                    continue
                resp += self.listofplaces[place]
            await self.message.edit(content=resp)
        except IndexError:
            return

    @menus.button('\N{UPWARDS BLACK ARROW}')
    async def on_up_arrow(self, payload):
        try:
            pSnakePos = self.snakePos
            self.snakePos -= self.onebarlength
            self.listofplaces[self.snakePos] = '😳'
            self.listofplaces[pSnakePos] = '⬜'
            resp = ''
            for place in range(len(self.listofplaces)):
                if place in (2, 5):
                    resp += (self.listofplaces[place] + '\n')
                    continue
                resp += self.listofplaces[place]
            await self.message.edit(content=resp)
        except IndexError:
            return
    
    @menus.button('\N{DOWNWARDS BLACK ARROW}')
    async def on_down_arrow(self, payload):
        try:
            pSnakePos = self.snakePos
            self.snakePos += self.onebarlength
            self.listofplaces[self.snakePos] = '😳'
            self.listofplaces[pSnakePos] = '⬜'
            resp = ''
            for place in range(len(self.listofplaces)):
                if place in (2, 5):
                    resp += (self.listofplaces[place] + '\n')
                    continue
                resp += self.listofplaces[place]
            await self.message.edit(content=resp)
        except IndexError:
            return
    
    @menus.button('\N{BLACK RIGHTWARDS ARROW}')
    async def on_right_arrow(self, payload):
        try:
            pSnakePos = self.snakePos
            self.snakePos += 1
            self.listofplaces[self.snakePos] = '😳'
            self.listofplaces[pSnakePos] = '⬜'
            resp = ''
            for place in range(len(self.listofplaces)):
                if place in (2, 5):
                    resp += (self.listofplaces[place] + '\n')
                    continue
                resp += self.listofplaces[place]
            await self.message.edit(content=resp)
        except IndexError:
            return
    
    @menus.button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    async def on_stop(self, payload):
        self.stop()
    
    def reaction_check(self, payload):
        """The function that is used to check whether the payload should be processed.
        This is passed to :meth:`discord.ext.commands.Bot.wait_for <Bot.wait_for>`.
        There should be no reason to override this function for most users.
        Parameters
        ------------
        payload: :class:`discord.RawReactionActionEvent`
            The payload to check.
        Returns
        ---------
        :class:`bool`
            Whether the payload should be processed.
        """
        if payload.message_id != self.message.id:
            return False
        if self.ctx.bot.get_user(payload.user_id).bot:
            return False
        return payload.emoji in self.buttons

eightBall_msgs = ["It is certain","Without a doubt", "\
You may rely on it","\
Yes definitely","\
It is decidedly so","\
As I see it, yes","\
Most likely","\
Yes","\
Outlook good","\
Signs point to yes","\
Reply hazy try again","\
Better not tell you now","\
Ask again later","\
Cannot predict now","\
Concentrate and ask again","\
Don’t count on it","\
Outlook not so good","\
My sources say no","\
Very doubtful","\
My reply is no"]
    
rocpapsci = ['rock', 'paper', 'scissors']

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.wtp_is_playing = False
    
    @commands.command(brief='A classic game of rock paper scissors')
    async def rps(self, ctx, ropasc=None):
        if ropasc is None:
            await ctx.send('Missing Required Arguments!')
            return
        if not ropasc in rocpapsci:
            await ctx.send('Invalid Argument! Valid Arguments: paper, scissors, rock')
            return
        a = random.choice(rocpapsci)
        await ctx.send('rock..')
        await asyncio.sleep(0.3)
        await ctx.send('paper..')
        await asyncio.sleep(0.3)
        await ctx.send('scissors..')
        await asyncio.sleep(0.3)
        await ctx.send('shoot!')
        await asyncio.sleep(0.3)
        await ctx.send('I chose {}.. you chose {}.'.format(a, ropasc))
    
    @commands.command(name='8ball', brief='Shows you a random answer to your yes or no question')
    async def _8ball(self, ctx, *, question):
        answer = random.choice(eightBall_msgs)
        await ctx.send(f'Question: {question}\nAnswer: {str(answer)}')
    
    @commands.command(brief='Makes the bot roll a dice for you')
    async def roll(self, ctx, dice:int=3):
        if dice > 20:
            await ctx.send(f'Sorry, but i don\'t have {dice} dice')
            return
        if dice < 1:
            await ctx.send(f'Sorry, but i don\'t have {dice} die')
            return
        a = []
        for x in range(dice):
            a.append(str(random.randint(0, 10)))
        await ctx.send('You Rolled: \n`' + (', '.join(a)) + '`')
    
    @commands.command(brief='Makes the bot choose a random option out of what you give it')
    async def choose(self, ctx, *args):
        choice = random.choice(args)
        await ctx.send('I chose '+choice)
    
    @commands.command(brief='Generates random text and gives it to you')
    async def pseudotext(self, ctx):
        predicate = random.choice(['pseudo text', 'dog', 'cat', 'your mom', 'mr. beaver', 'people'])
        adjective = random.choice(['cool', 'bad', 'awesome', 'big', 'stupid', 'also stupid'])
        await ctx.send(predicate + ' is ' + adjective)
    
    @commands.command(brief='Spins a fidget spinner')
    async def spinner(self, ctx):
        a = random.randint(1, 100)
        await ctx.send('You started spinning a fidget spinner, lets see how long it spins!')
        await asyncio.sleep(a)
        await ctx.send(f'It spun for {a} seconds!')
    
    @commands.command(brief='Scrambles the text you give it')
    async def scramble(self, ctx, *, text:str):
        a = list(text)
        random.shuffle(a)
        await ctx.send(''.join(a))
    
    @commands.command(brief='Reverses the text you give it')
    async def reverse(self, ctx, *, text:str):
        a = list(text)
        a.reverse()
        await ctx.send(''.join(a))
    
    @commands.command(name='upsidedown', brief='Makes the text you give it upside down')
    async def _upsidedown(self, ctx, *, text:str):
        text = upsidedown.transform(text)
        await ctx.send(text)
    
    @commands.command(brief='Eats the person you choose')
    async def eat(self, ctx, member:discord.Member=None, *, reason:str=None):
        if member == None or member == ctx.author:
            await ctx.send(f'{ctx.author.mention} ate themselves...')
            return
        if reason == None:
            await ctx.send(f'{ctx.author.mention} ate {member.mention}')
        elif reason != None:
            await ctx.send(f'{ctx.author.mention} ate {member.mention} for {reason}')
    
    @commands.command(brief='Kills the person you choose')
    async def kill(self, ctx, member:discord.Member=None, *, reason:str=None):
        if member == None or member == ctx.author:
            await ctx.send(f'{ctx.author.mention} commited suicide')
            return
        if reason == None:
            await ctx.send(f'{ctx.author.mention} killed {member.mention}')
        elif reason != None:
            await ctx.send(f'{ctx.author.mention} killed {member.mention} for {reason}')
    
    @commands.command(brief='Generates a random number and makes you guess it')
    async def guessnum(self, ctx):
        min = random.randint(1, 100)
        max = random.randint(1, 100 + min)
        num = random.randint(min, max)
        print('Someone ran guessnum, the number is {}'.format(num))
        for max in range(4):
            guess = await ui.prompt(ctx, f'I\'m thinking of a number between {num-random.randint(num-40, num)} and {num+random.randint(num, num+40)}, What do you think it is? (BTW the range of the numbers might change, but the real number never changes)')
            if guess == str(num):
                await ctx.send('Correct!')
                return
            elif guess != str(num):
                await ctx.send('Incorrect....')
        await ctx.send(f'You\'ve ran out of guesses! I was thinking of {num}....')
    
    @commands.command(brief='A game of "Whose thats pokemon?"')
    async def wtp(self, ctx):
        if self.wtp_is_playing == True:
            await ctx.send('Theres another running game, let the person finish it before starting a new one')
            return
        elif self.wtp_is_playing == False:
            self.wtp_is_playing = True
            guess_orders = [3, 2, 1, 0]
            wtp_object = await self.bot.dag.wtp()
            await ctx.send(wtp_object.question)
            guess = await ui.prompt(ctx, 'You have {} guesses to guess the pokemon'.format(len(guess_orders)-1))
            for guesses in guess_orders:
                if guess.capitalize() == wtp_object.name:
                    await ctx.send('Correct, you got it with {} guesses left.'.format(guesses))
                    break
                if guesses == 0:
                    await ctx.send(f'You have no guesses left. It was {wtp_object.answer}')
                    break
                elif guess.lower() == 'stop' or guess.lower() == 'end':
                    await ctx.send('Stopping Game...')
                    self.wtp_is_playing = False
                    break
                elif guess.capitalize() != wtp_object.name:
                    guess = await ui.prompt(ctx, 'Incorrect, you have {} guesses left. What is your new guess?'.format(guesses))
    
    @commands.command(brief='Roasts people, roasty toasty!')
    async def roast(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author
        
        await ctx.send(f'**{member.name}**, {await self.bot.dag.roast()}')
    
    @commands.command(brief='Catch the pie within the time')
    async def pie(self, ctx):
        embed = discord.Embed(title='Catch the Pie!', color=discord.Color.green(), description='3')
        msg = await ctx.send(embed=embed)
        for x in ['2', '1']:
            await asyncio.sleep(1)
            embed.description = x
            await msg.edit(embed=embed)
        await asyncio.sleep(1)
        embed.description = 'NOW'
        await msg.edit(embed=embed)
        await msg.add_reaction('\U0001f967')
        time_perf = time.perf_counter()
        def check(reaction, user):
            return str(reaction.emoji) == '🥧' and user.name != self.bot.user.name
        
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        embed.description = user.name + ' got it in ' + str(round((time.perf_counter()-time_perf) * 1000, 6)) + 'ms'
        await msg.edit(embed=embed)
    
    @commands.command(brief='Plays a game of TicTacToe (WARNING: Command is in development)')
    async def ttt(self, ctx, buddy:discord.Member=None):
        if buddy is None:
            await ctx.send('Who would you like to play with?')
            return
        ctx.symbols = [f"{chr(10060)}", f"{chr(11093)}"]
        ctx.buddy = buddy.id
        ctx.playing_users = [buddy.id, ctx.author.id]
        menu = MyMenu()
        await menu.start(ctx)

def setup(bot):
    bot.add_cog(Games(bot))
