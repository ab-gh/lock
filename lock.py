__authors__ = 'aejb'
import json
import math
import numpy
import typing
import time

import discord
import aiohttp
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from random import randint

MOD_ROLE = 835836027767619584
LOCK_CATEGORIES = [835836880334749736, 835840078475165728]


class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_lock_categories(self, guild, categories):
        lock_categories = []
        for category in categories:
            lock_categories.append(guild.get_channel(category))
        return lock_categories

    async def status_embed(self, ctx, description):
        guild = ctx.author.guild
        everyone_role = discord.utils.get(guild.roles, name="@everyone")
        channelarr = ctx.author.guild.channels
        embed = discord.Embed()
        embed.set_author(name=description)
        for category in ctx.author.guild.by_category():
            value = ""
            for channel in category[1]:
                if isinstance(channel, discord.TextChannel):
                    send = channel.overwrites_for(everyone_role).send_messages
                    if send:
                        emoji = "\u2705"
                    elif send == False:
                        emoji = "\U0001F512"
                    else:
                        emoji = "\u3030"
                    value += f"{channel.mention}\t\t{emoji}\n"
            embed.add_field(name=category[0], value=value, inline=False)
        return embed

    async def channel_lock(self, everyone, channel):
        await channel.set_permissions(everyone, send_messages=False, reason="Automatic channel locking")

    async def channel_unlock(self, everyone, channel):
        await channel.set_permissions(everyone, send_messages=True, reason="Automatic channel unlocking")

    async def has_mod(self, ctx):
        return ctx.guild.get_role(754378392647893103) in ctx.author.roles

    @commands.command()
    async def ping(self, ctx):
        """------ a simple ping-pong command"""
        latency_rounded = str("internal heartbeat latency = " + str(round(self.bot.latency, 1)) + "ms")
        embed = discord.Embed()
        embed.add_field(name=latency_rounded,
                        value="pong!",
                        inline=True)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(MOD_ROLE)
    async def lock(self, ctx):
        """------ locks every channel in a given category"""
        guild = ctx.author.guild
        lock_categories = await self.get_lock_categories(guild, LOCK_CATEGORIES)
        everyone_role = discord.utils.get(guild.roles, name="@everyone")
        lock_string = ', '.join(map(str, lock_categories))
        embed = discord.Embed(description=f"Locking channels in {lock_string}...")
        message = await ctx.send(embed=embed)
        for category in ctx.author.guild.by_category():
            if category[0] in lock_categories:
                for channel in category[1]:
                    await self.channel_lock(everyone_role, channel)
        time.sleep(2)
        embed = await self.status_embed(ctx, description=f"Locked channels in category \'{lock_string}\'")
        await message.edit(embed = embed)
        
    @commands.command()
    @commands.has_role(MOD_ROLE)
    async def unlock(self, ctx):
        """------ unlocks every channel in a given category"""
        guild = ctx.author.guild
        lock_categories = await self.get_lock_categories(guild, LOCK_CATEGORIES)
        everyone_role = discord.utils.get(guild.roles, name="@everyone")
        lock_string = ', '.join(map(str, lock_categories))
        embed = discord.Embed(description=f"Unlocking channels in {lock_string}...")
        message = await ctx.send(embed=embed)
        for category in ctx.author.guild.by_category():
            if category[0] in lock_categories:
                for channel in category[1]:
                    await self.channel_unlock(everyone_role, channel)
        time.sleep(2)
        embed = await self.status_embed(ctx, description=f"Unlocked channels in category \'{lock_string}\'")
        await message.edit(embed = embed)

    @commands.command()
    @commands.has_role(MOD_ROLE)
    async def status(self, ctx):
        """------ checks the status for all channels"""
        embed = await self.status_embed(ctx, description="Send Message permissions for @everyone")
        message = await ctx.send(embed=embed)
        
    @status.error
    async def status_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You do not have the permissions to use this command')
            await ctx.message.add_reaction('\N{CROSS MARK}')
        if isinstance(error, commands.BadArgument):
            await ctx.send('That user was not found in this guild.')
            await ctx.message.add_reaction('\N{CROSS MARK}')

def setup(bot):
    bot.add_cog(moderation(bot))