from datetime import datetime
import time
from pytz import timezone
import pytz
from sqlite3 import Date
from discord.ext import commands
import discord
import json
import random
import os
#------------ SQL SPECIFIC SHENANIGANS ----------------
from sqlalchemy import Column
from sqlalchemy import text
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import select
import sqlalchemy
import sqlalchemy.orm
#---------------
#Create engine and connect to our databse
engine = create_engine("sqlite:///CorvOS.db", echo=True,future=True)
Base = declarative_base()
#Create the user table
#DOES THIS OVERWRITE EVERYTHING???
class QuotesORG(Base):
    __tablename__ = "QuotesORG"
    ID = Column(Integer,primary_key=True)
    Name = Column(String(30))
    Msg = Column(String)
    MsgDate = Column(sqlalchemy.DateTime)
    ChannelID = Column(Integer)

    def __repr__(self):
        return f"User(ID={self.ID!r},Name={self.Name!r},Msg={self.Msg!r},MsgDate={self.MsgDate!r})"

#User will store a quote
#CorvOS will speak that quote
#Must ensure that words are filtered
#Filter List must prevent genuine fucked up slurs from being posted or STORED. 
class CorvSPEAK(Base):
    __tablename__ = "CorvSPEAK"
    ID = Column(Integer,primary_key=True)
    Name = Column(String(30))
    Msg = Column(String)
    MsgDate = Column(sqlalchemy.DateTime)
    ChannelID = Column(Integer)

    def __repr__(self):
        return f"User(ID={self.ID!r},Name={self.Name!r},Msg={self.Msg!r},MsgDate={self.MsgDate!r})"

#TODO:  Implement a table to recall SINGULAR quotes
#       Users will send $Store <text they want to store>
#       Users can use $Speak and the bot will return a randomized SINGULAR quote
#       This will be locked to a given guild using the channelID tag. 

class DiscordDotOrg(commands.Cog, name="DiscordDotOrg"):
   
    @commands.command()
    async def quote(self,ctx:commands.Context, count:int, channel:discord.TextChannel=None):
        """STORE MESSAGES IN DATABASE FOR LATER RECALL"""
        if count <= 00:
            await ctx.send("CAW. CAW. Usage <Command> <Number of messages to store> -- Count cant be zero")
        elif count > 0:
            flag = True # this is in my original code? not sure why?
            #Start session
            session = Session(engine)
            stmt = session.query(QuotesORG.ID).distinct(QuotesORG.ID).count() #This increments ID count up. 
            IDCOUNT = stmt # stores it to make it part of the statement later
            async for x in ctx.channel.history(limit=count+1):
                if flag == True: #SKIP THE CALLING MESSAGE
                    flag = False
                elif flag == False:
                    authorname = str(x.author).split("#")[0]
                    #set eastern timezone
                    local_tz = pytz.timezone('US/Eastern')
                    timez = x.created_at.replace(tzinfo = pytz.utc).astimezone(local_tz)
                    quote_user = QuotesORG(ID=IDCOUNT,Name=authorname,Msg = x.content,MsgDate=timez,ChannelID=ctx.guild.id)
                    session.add(quote_user)
            session.commit()


    @commands.command()
    async def recall(self,ctx:commands.Context):
        """RECALL STORED BULK MESSAGES FOR DISPLAY"""
        session = Session(engine)
        ids = session.execute(select(QuotesORG.ID).distinct(QuotesORG.ID).where(QuotesORG.ChannelID==ctx.guild.id))
        #this gets a set of id's so that we can iterate over them
        #only the id's for a given channel are pulled
        channel_quotes=[]
        #store id's in an array for easy recalling later
        for row in ids:
            channel_quotes.append(row[0])
        search = random.choice(channel_quotes)

        #set up our embed 
        embed = discord.Embed(title="CorvOSDotOrg",description="Quoth the Raven:",color=0x00ffb3)
        stmt = select(QuotesORG).where(QuotesORG.ID == search).order_by(QuotesORG.MsgDate) #SELECT * FROM <DBNAME> WHERE ID = RANDOMIDVAL ORDER BY DATE
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                unxtime = time.mktime(row.MsgDate.timetuple()) #convert time to unix time
                embed.add_field(name=f"{row.Name} -- <t:{int(unxtime)}:t>", value=row.Msg, inline=False)
        
        archivaldate = row.MsgDate.strftime("%d/%m/%Y")
        embed.set_footer(text=f"Archived On: {archivaldate}")
        session.rollback()
        await ctx.send(embed=embed)


    @commands.command()
    async def store(self,ctx:commands.Context,*mesUnFormat):
        """STORE SOMETHING YOU WANT ME TO SAY"""
        print("Getting the message")
        message = ' '.join(str(val) for val in mesUnFormat)
        print(message)
        session = Session(engine)
        idTrack = session.query(CorvSPEAK.ID).distinct(CorvSPEAK.ID).count()
        async for x in ctx.channel.history(limit = 1):
            #filter
            filtered = []
            with open("/home/vantom/Documents/programming/Python/CorvOS/modules/DiscordDotOrg/swearWords.txt") as file:
                for line in file:
                    line = line.strip()
                    filtered.append(line)
            file.close()
            for mes in filtered:
                message = message.replace(mes,"-BLAM!-")
            author = str(x.author).split("#")[0]
            local_tz = pytz.timezone('US/EASTERN')
            timez = x.created_at.replace(tzinfo = pytz.utc).astimezone(local_tz)
            datastore = CorvSPEAK(ID=idTrack,Name = author, Msg = message, MsgDate = timez, ChannelID = ctx.guild.id)
            session.add(datastore)
        session.commit()
        # if (message.author == "CorvOS"):
        #     print ("Closing the Loop")
        #     return
        # try:
        #     if(message[0] != "\'"):
        #         print("I see: " + message)
        #         raise Exception
        #     else: 
        #         #message is the actual message we need to store, minus the called statement
        #         #we need to do the async thing to get the rest of the data i need to store
        #         #TODO ADD FILTER LIST 
        #         session = Session(engine)
        #         idTrack = session.query(CorvSPEAK.ID).distinct(CorvSPEAK.ID).count()
        #         async for x in ctx.channel.history(limit = 1):
        #             #FILTER
        #             filtered = []
        #             with open("/home/vantom/Documents/programming/Python/CorvOS/modules/DiscordDotOrg/swearWords.txt") as file:
        #                 for line in file:
        #                     line = line.strip()
        #                     filtered.append(line)
        #             for mes in filtered:
        #                 message = message.replace(mes,"-BLAM!-")
        #             author = str(x.author).split("#")[0]
        #             local_tz = pytz.timezone('US/EASTERN')
        #             timez = x.created_at.replace(tzinfo = pytz.utc).astimezone(local_tz)
        #             datastore = CorvSPEAK(ID=idTrack,Name = author, Msg = message, MsgDate = timez, ChannelID = ctx.guild.id)
        #             session.add(datastore)
        #         session.commit()
        # except Exception as err:
        #     await ctx.send("CAW. Something went wrong - did you use quotes (\" \") when sending your message?")
            
    @commands.command()
    async def speak(self,ctx:commands.Context):
        """SPEAK TO CHAT - SINGLE QUOTES"""
        session = Session(engine)
        ids = session.execute(select(CorvSPEAK.ID).distinct(CorvSPEAK.ID).where(CorvSPEAK.ChannelID == ctx.guild.id))
        message = []
        for row in ids:
            message.append(row[0])
        choice = random.choice(message)
        # await ctx.send("choice follows")
        # await ctx.send(choice)
        # await ctx.send("message follows")
        # await ctx.send(message)
        stmt = select(CorvSPEAK).where(CorvSPEAK.ID == choice)
        with engine.connect() as conn:
            for row in conn.execute(stmt):
                speaker = row.Msg
            
        await ctx.send(speaker)

    @commands.command()
    async def ping(self,ctx:commands.Context):
        """CHECK IF IM AWAKE"""
        await ctx.send("CORVOS ONLINE!")
async def setup(bot:commands.Bot):
	await bot.add_cog(DiscordDotOrg(bot))

# class CorvSPEAK(Base):
#     __tablename__ = "CorvSPEAK"
#     ID = Column(Integer,primary_key=True)
#     Name = Column(String(30))
#     Msg = Column(String)
#     MsgDate = Column(sqlalchemy.DateTime)
#     ChannelID = Column(Integer)