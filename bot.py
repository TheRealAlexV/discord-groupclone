import discord
from discord import app_commands
from discord.ext import commands
import os
import re

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="groupclone_roles")
async def clone_roles(interaction: discord.Interaction, rolefind: str, rolereplace: str):
    print(f"Command received. rolefind: '{rolefind}', rolereplace: '{rolereplace}'")
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    roles_to_clone = sorted([role for role in guild.roles if rolefind.lower() in role.name.lower()], key=lambda r: r.position, reverse=True)
    
    print(f"Roles to clone: {[role.name for role in roles_to_clone]}")
    print(f"Find: '{rolefind}', Replace: '{rolereplace}'")

    new_roles = []
    for role in roles_to_clone:
        old_name = role.name
        new_name = re.sub(re.escape(rolefind), rolereplace, role.name, flags=re.IGNORECASE)
        print(f"Old name: '{old_name}', New name: '{new_name}'")
        
        new_role = await guild.create_role(
            name=new_name,
            permissions=role.permissions,
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable
        )
        new_roles.append(new_role)
    
    # Find the lowest position of the original roles
    lowest_position = min(role.position for role in roles_to_clone)
    
    # Sort all guild roles
    sorted_roles = sorted(guild.roles, key=lambda r: r.position, reverse=True)
    
    # Find the index where we should insert our new roles
    insert_index = len(sorted_roles) - sorted_roles[::-1].index(discord.utils.get(sorted_roles, position=lowest_position))
    
    # Remove new roles from their current positions
    sorted_roles = [role for role in sorted_roles if role not in new_roles]
    
    # Insert new roles at the correct position, maintaining their order
    for i, new_role in enumerate(new_roles):
        sorted_roles.insert(insert_index + i, new_role)
    
    # Prepare the positions dictionary
    positions = {role: len(sorted_roles) - i for i, role in enumerate(sorted_roles)}
    
    # Update role positions
    await guild.edit_role_positions(positions)
    
    cloned_roles_info = "\n".join([f"'{role.name}' -> '{new_roles[i].name}'" for i, role in enumerate(roles_to_clone)])
    await interaction.followup.send(f"Cloned {len(new_roles)} roles with name replacements:\n{cloned_roles_info}", ephemeral=True)

@bot.tree.command(name="groupclone_channels")
async def clone_channels(interaction: discord.Interaction, channel_id: str, chanfind: str, chanreplace: str):
    print(f"Command received. channel_id: '{channel_id}', chanfind: '{chanfind}', chanreplace: '{chanreplace}'")
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    category = discord.utils.get(guild.categories, id=int(channel_id))
    
    if not category:
        await interaction.followup.send("Category not found.", ephemeral=True)
        return
    
    def clone_overwrites(old_overwrites):
        new_overwrites = {}
        for target, overwrite in old_overwrites.items():
            if isinstance(target, discord.Role):
                new_role_name = re.sub(re.escape(chanfind), chanreplace, target.name, flags=re.IGNORECASE)
                new_role = discord.utils.get(guild.roles, name=new_role_name)
                if new_role:
                    new_overwrites[new_role] = overwrite
                else:
                    print(f"Warning: Role '{new_role_name}' not found")
            else:
                new_overwrites[target] = overwrite
        return new_overwrites

    # Clone category with permissions
    new_category_overwrites = clone_overwrites(category.overwrites)
    new_category = await guild.create_category(
        name=re.sub(re.escape(chanfind), chanreplace, category.name, flags=re.IGNORECASE),
        overwrites=new_category_overwrites
    )
    print(f"Created category: '{new_category.name}' with {len(new_category_overwrites)} permission overwrites")
    
    channels_to_clone = sorted(
        [channel for channel in category.channels if isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.ForumChannel))],
        key=lambda c: c.position
    )
    
    print(f"Channels to clone: {[channel.name for channel in channels_to_clone]}")
    
    new_channels = []
    for channel in channels_to_clone:
        old_name = channel.name
        new_name = re.sub(re.escape(chanfind), chanreplace, channel.name, flags=re.IGNORECASE)
        print(f"Old name: '{old_name}', New name: '{new_name}'")
        
        channel_overwrites = clone_overwrites(channel.overwrites)
        
        channel_args = {
            'name': new_name,
            'overwrites': channel_overwrites,
            'category': new_category,
            'position': channel.position,
        }
        
        if isinstance(channel, discord.TextChannel):
            channel_args.update({
                'topic': channel.topic,
                'slowmode_delay': channel.slowmode_delay,
                'nsfw': channel.nsfw,
                'default_auto_archive_duration': channel.default_auto_archive_duration,
            })
            new_channel = await guild.create_text_channel(**channel_args)
        elif isinstance(channel, discord.VoiceChannel):
            channel_args.update({
                'bitrate': channel.bitrate,
                'user_limit': channel.user_limit,
            })
            new_channel = await guild.create_voice_channel(**channel_args)
        elif isinstance(channel, discord.ForumChannel):
            channel_args.update({
                'topic': channel.topic,
                'slowmode_delay': channel.slowmode_delay,
                'nsfw': channel.nsfw,
            })
            new_channel = await guild.create_forum(**channel_args)
        
        new_channels.append(new_channel)
        print(f"Created channel: '{new_channel.name}' with {len(channel_overwrites)} permission overwrites")
    
    # Sort the new channels to match the order of the original channels
    for i, channel in enumerate(new_channels):
        await channel.edit(position=i)
    
    cloned_channels_info = "\n".join([f"'{channel.name}' -> '{new_channels[i].name}'" for i, channel in enumerate(channels_to_clone)])
    await interaction.followup.send(f"Cloned category '{category.name}' with {len(new_channels)} channels:\n{cloned_channels_info}", ephemeral=True)

bot.run(os.getenv('DISCORD_TOKEN'))
