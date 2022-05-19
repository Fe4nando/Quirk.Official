import discord
import os
from discord.ext import commands
from config import *
from discord.ui import Button,View

intents = discord.Intents.all()
discord.member = True
client=commands.Bot (command_prefix=commands.when_mentioned_or('!'),intents = intents)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,activity=discord.Game('!help'))
    print('Quirk Is Online')
    absolute_path = os.path.abspath(__file__)
    print("Full path: " + absolute_path)
    print("Directory Path: " + os.path.dirname(absolute_path))
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandNotFound):
        await ctx.send("Please use a vaild Command available. Use the command !help for more info")

@client.command()       
async def report(ctx):
        member=ctx.author
        try:
            button=Button(label="Continue",style=discord.ButtonStyle.green)
            view=View()
            view.add_item(button)
            await ctx.message.add_reaction("✅")
            await member.send("click on continue to start",view=view)
            async def button_callback(interaction):
                button=Button(label="YES",style=discord.ButtonStyle.green)
                button1=Button(label="NO",style=discord.ButtonStyle.red)
                embed=discord.Embed(title="Report",description="For Report the user you must provide the follwing information")
                embed.add_field(name="Information Needed",value="Type of Report:\n[Type here]\nDescription of Report\n[Type here]\nThe name of the user:\n[Type Here]\nScreenshot and evidence\n[Please provide as link]")
                embed.set_footer(text="By clicking on Yes,you can start typing your report in the format given above.Please note the message needs to be sent as one.")
                view=View()
                view.add_item(button)
                view.add_item(button1)
                async def button_callback(interaction):
                    embed=discord.Embed(title="Report",description="For Report the user you must provide the follwing information")
                    embed.add_field(name="Information Needed",value="Type of Report:\n[Type here]\nDescription of Report\n[Type here]\nThe name of the user:\n[Type Here]\nScreenshot and evidence\n[Please provide as link]")
                    embed.set_footer(text="By clicking on Yes,you can start typing your report in the format given above.Please note the message needs to be sent as one.")
                    await interaction.response.send_message(embed=embed)
                    channel=client.get_channel(962389878748880926)
                    def check(m):
                      return m.author.id==ctx.author.id
                    message=await client.wait_for("message",check=check)
                    await message.add_reaction("<:Bruh:905404779860209699>")
                    report=discord.Embed(title="New Report",description=f"This Report was sent by {ctx.author.display_name}")
                    report.add_field(name="The Report",value=f"{message.content}")
                    await channel.send(embed=report)
                button.callback=button_callback
                async def button1_callback(interaction):
                    embed=discord.Embed(title="Rejected Report Request!")
                    view=View()
                    await interaction.response.edit_message(embed=embed,view=view)
                button1.callback=button1_callback
                await interaction.response.send_message(embed=embed,view=view)
            button.callback=button_callback
            
        except:
            embed=discord.Embed()
            embed.set_image(url="https://media.discordapp.net/attachments/966210256847900693/966212516512411698/unknown.png")
            await ctx.send("You have Disabled allow user dm in privacy settings",embed=embed)
            await ctx.message.add_reaction("❌")
            await ctx.message.remove_reaction("✅")
            
@client.command()
async def help(ctx):
    embed=discord.Embed(title="Help Commands of Python Quirk")
    embed.add_field(name="Member Count",value="Gives the Server member count")
    embed.add_field(name="`!report`",value="You can report users and bugs over here")
    embed.add_field(name="Features",value="Logging,Anit-Swear,Warnings,Security System")
    await ctx.send(embed=embed)

import datetime 
from datetime import datetime
@client.command()
async def downloadlogs(ctx,*,reason=None):
    if reason==None:
        reason='Not provided'
    timestamp=datetime.now()
    try:
     ent=open(r'C:\Users\LENOVO\OneDrive\Documents\Desktop\Python Bot\PIE\Quik-2.0-test\logs\messagelogs.txt','a', encoding='utf-8')
    except:
     ent=open(r'/workspace/logs/messagelogs.txt','a', encoding='utf-8')
    ent.write(f"\n Data was Downloaded on {timestamp} by:{ctx.author.display_name},with the reason of:{reason}\n")
    ent.close()
    try:
     await ctx.send(file=discord.File(r'C:\Users\LENOVO\OneDrive\Documents\Desktop\Python Bot\PIE\Quik-2.0-test\logs\messagelogs.txt'))
    except:
     await ctx.send(file=discord.File(r'/workspace/logs/messagelogs.txt'))
     
@client.event
async def on_message_delete(message):
    timestamp=datetime.now()
    try:
     ent=open(r'C:\Users\LENOVO\OneDrive\Documents\Desktop\Python Bot\PIE\Quik-2.0-test\logs\messagelogs.txt','a', encoding='utf-8')
    except:
     ent=open(r'/workspace/logs/messagelogs.txt','a', encoding='utf-8')
    ent.write(f"Time:{timestamp} Message:{message.content} Location:{message.channel.mention} Author:{message.author.display_name} ID:{message.author.id} \n")
    ent.close()
    
@client.event
async def on_message_edit(before,after):
    channel=client.get_channel(966186616232243210)
    embed=discord.Embed(title="Message Edited",description=f"User:{before.author}\nPrevious:{before.content}\nAfter:{after.content}\nChannel:{before.channel.mention}")
    await channel.send(embed=embed)
  
    
import Word_filter
from Word_filter import word
filtred_words=word
@client.event
async def on_message(ctx):
    channel=client.get_channel(966186616232243210)
    for word in filtred_words:
        if word in ctx.content:
            await ctx.delete()
            embed=discord.Embed(title="Swear Word Used",description=f"{ctx.author.name} used a swear word.\nWord:||{ctx.content}||")
            await channel.send(embed=embed)
    await client.process_commands(ctx)
    
@commands.has_permissions(manage_messages=True)
@client.command(aliases=["purge"])
async def clear(ctx,amount:int):
    await ctx.channel.purge(limit=amount)

@commands.has_permissions(ban_members=True)
@client.command(pass_context=True)
async def mute(ctx,user:discord.Member=None,*,reason="No reason provided"):
    if user==None:
        await ctx.send("You need to specify the user!")
    elif user==ctx.message.author:
        await ctx.send("You cant mute yourself")
    elif user.guild_permissions.administrator:
        await ctx.send("You cant mute a administrator")
    else:
        mute=ctx.guild.get_role(852770025521807400)
        await ctx.send(f"{user} has been muted!\nReason:{reason}")
        await user.add_roles(mute)
        
@commands.has_permissions(ban_members=True)
@client.command(pass_context=True)
async def unmute(ctx,user:discord.Member=None):
    mute=ctx.guild.get_role(852770025521807400)
    if user==None:
        await ctx.send("You need to specify the user!")
    elif user==ctx.message.author:
        await ctx.send("You cant unmute yourself!")
    elif user.guild_permissions.administrator:
        await ctx.send("You cant unmute a administrator!")
    elif mute not in user.roles:
        await ctx.send("The user isnt even muted at first!")
    else:
        await ctx.send(f"{user} has been unmuted")
        await user.remove_roles(mute)
        
@commands.has_permissions(ban_members=True)
@client.command(pass_context=True)
async def warn(ctx,user:discord.Member=None,*,reason="No reason provided"):
    channel=client.get_channel(966186616232243210)
    if user==None:
        await ctx.send("You need to specify the user!")
    elif user==ctx.message.author:
        await ctx.send("You cant warn yourself")
    elif user.guild_permissions.administrator:
        await ctx.send("You cant warn administrator")
    else:
        embed=discord.Embed(title="Warning!",description=f"{user.mention} has been warning.Reason:{reason}")
        await ctx.send(embed=embed)
        await channel.send(embed=embed)
        try: 
          await user.send(f"You have been warned by the adminstrator of the Grade 9 IGCSE Server.Reason:{reason}")
        except:
          await channel.send("Unable to dm the user,has dms permissions off,cant message user about warn")

@commands.has_permissions(ban_members=True)
@client.command(pass_context=True)
async def ban(ctx,user:discord.Member,reason="No Reason Provided"):
    if user==None:
        await ctx.send("Invailded Information Provided")
    elif user.guild_permissions.administrator:
        await ctx.send("Unable to Ban Error Code:Admin=True")
    else:
        try:
            embed=discord.Embed(title="Ban",
                                description="It looks like you have been banned from the server!\n You can request for a unban appeal by click the button below.")
            button=Button(label="Request Appeal",url="https://docs.google.com/forms/d/e/1FAIpQLSdvYvZGKhi4VDoiKs6lleraftf-ke4Yxh_SGe5vBRsdGUIEbg/viewform?usp=sf_link")
            view=View()
            view.add_item(button)
            await user.send(embed=embed,view=view)
            await ctx.send(f"{user.display_name} has been banned from the server")
            await user.ban(reason=reason)
        except:
            await ctx.send("Cannot Message User! They cant request for a ban appeal")
            await user.ban(reason=reason)

      
      
      
    
client.run(token)