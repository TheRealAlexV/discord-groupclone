# Discord Roles and Channel Cloning Bot

* 1. [Description](#Description)
* 2. [Features](#Features)
* 3. [Requirements](#Requirements)
* 4. [Setup](#Setup)
	* 4.1. [Docker Setup (Containerized)](#DockerSetupContainerized)
	* 4.2. [Local Setup (From Source)](#LocalSetupFromSource)
* 5. [Usage](#Usage)
	* 5.1. [Clone Roles](#CloneRoles)
		* 5.1.1. [groupclone_roles](#groupclone_roles)
		* 5.1.2. [groupclone_channels](#groupclone_channels)
	* 5.2. [Clone Channels](#CloneChannels)
* 6. [Support](#Support)
* 7. [Contributing](#Contributing)
* 8. [License](#License)

##  1. <a name='Description'></a>Description

This Discord bot is designed to facilitate the rapid creation of organized groups within a Discord server. It provides functionality to clone groups of roles and entire channel categories (including their channels) along with their permissions. This bot is particularly useful for server administrators who need to create multiple similar channel and role structures within their Discord server.

##  2. <a name='Features'></a>Features

- Clone roles with name replacement in the form of a string search and replace
- Clone channel categories with name replacement in the form of a string search and replace
- Maintain role and channel permissions during cloning and adapt role permissions via search and replacement
- Preserve channel-specific settings (e.g., slowmode, NSFW status, etc.)
- Use slash commands for easy interaction (/groupclone)

##  3. <a name='Requirements'></a>Requirements

- git
- Python 3.8+
- Discord.py library

**OR**

- Docker & Docker-Compose (For containerized deployment)

##  4. <a name='Setup'></a>Setup

1. **You must first create a Discord bot API token.** You can follow the following guide to create your bot token: https://www.writebots.com/discord-bot-token/

The permissions you need for this bot are:
- View Channels
- Manage Channels
- Manage Roles
- Send Messages

Once you have the token, save it for the next steps...

2. Clone this repository:
```
git clone https://github.com/TheRealAlexV/discord-groupclone.git
cd discord-groupclone
```

3. Copy the included .env.example to .env. After copying the file, be sure to replace "YOUR_DISCORD_TOKEN" with the discord bot token you put aside.
```
cp .env.example .env
```

###  4.1. <a name='DockerSetupContainerized'></a>Docker Setup (Containerized)

**NOTE:** Be sure to complete the steps in the [Setup](#Setup) section before starting this section.

You should have Docker and Docker-compose installed. If on windows, you can download "Docker for Windows".

**Note:** If you prefer to run this bot in a local environment instead of from a container, skip to the next section titled "Local Setup (From Source)"

1. Build and run the Docker container:
```
docker-compose up --build
```

###  4.2. <a name='LocalSetupFromSource'></a>Local Setup (From Source)

**NOTE:** Be sure to complete the steps in the [Setup](#Setup) section before starting this section.

1. Install the required dependencies:
```
pip install -r requirements.txt
```

2. Run the bot
```
python bot.py
```

##  5. <a name='Usage'></a>Usage

The bot uses slash commands for all operations. Here are the available commands:

###  5.1. <a name='CloneRoles'></a>Clone Roles

####  5.1.1. <a name='groupclone_roles'></a>groupclone_roles

Command: `/groupclone_roles <rolefind> <rolereplace>`
This command will clone all roles containing \<rolefind> in their name, replacing that part with \<rolereplace> in the new role names. The new roles will be created with the same permissions as the original roles.

- \<rolefind>: The string to search for in role names to select multiple roles by, or just the entire role name if cloning a single role.
- \<rolereplace>: The string to replace \<rolefind> with in the new role names. If you are not replacing anything, use the same value you used for rolefind.

**Example:** 

If we have the following roles: "Red Players, Red Admins, Red Leaders"
`/groupclone_roles Red Blue`
Will create the following roles: "Blue Players, Blue Admins, Blue Leaders"

####  5.1.2. <a name='groupclone_channels'></a>groupclone_channels

###  5.2. <a name='CloneChannels'></a>Clone Channels

Command: `/groupclone_channels <channel_id> <chanfind> <chanreplace>`

- `<channel_id>`: The ID of the category to clone
- `<chanfind>`: The string to search for in channel names
- `<chanreplace>`: The string to replace `<chanfind>` with in the new channel names

This command will clone the specified category and all its channels. It will replace `<chanfind>` with `<chanreplace>` in all channel names and related role permissions.

Example:
/groupclone_channels 123456789 Red Blue

This will clone the category with ID 123456789, replacing "Red" with "Blue" in all channel names and related permissions. 

**BEWARE:** When setting channel and category Permissions, it will also copy the existing role permissions, while ALSO replacing "Red" with "Blue" in all role names. Role permissions that do not match the chanfind parameter will be copied to the new channels as is.

##  6. <a name='Support'></a>Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

##  7. <a name='Contributing'></a>Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

##  8. <a name='License'></a>License

This project is licensed under the MIT License - see the LICENSE file for details.