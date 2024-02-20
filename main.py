import os
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
from discord import Intents, Client, Message, utils
import discord
from responses import get_response

import ceny_paliva

# LOAD TOKEN
load_dotenv()
TOKEN = os.getenv('TOKEN')

# SETUP BOT
intents = Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True
client = Client(intents=intents)

message_created = False


# MESSAGE FUNC
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty')
        return

    is_private = user_message[0] == '?'

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        responses = get_response(user_message)
        await message.author.send(responses) if is_private else await message.channel.send(responses)

    except Exception as e:
        print(e)


async def daily_prices():
    channel = client.get_channel(1209228158143045633)
    if channel is not None:
        print("Kanál bol úspešne získaný.", channel.name)
        tankovanie_rola = discord.utils.get(channel.guild.roles, name="Tankovanie")
        fuel_prices = ceny_paliva.get_fuelPrices()

        if fuel_prices:
            message = f"{tankovanie_rola.mention} tu mate priemerne ceny palív pre dnešný deň! \n Aktuálne ceny palív:\n"
            for fuel, price in fuel_prices.items():
                message += f"{fuel}: {price} €\n"

            await channel.send(message)
        else:
            await channel.send("Nepodarilo sa získať aktuálne ceny palív.")
    else:
        print("Kanál s daným ID neexistuje alebo bot nemá oprávnenie posielať správy do tohto kanálu.")


# HANDLING START UP
@client.event
async def on_ready():
    print(f'{client.user} is now running!')

    # Získať kanál
    channel = client.get_channel(1209520390963994624)

    # Kontrola, či kanál existuje
    if channel is not None:
        print("Kanál bol úspešne získaný:", channel.name)

        message = await channel.fetch_message(1209528076766281758)

        if message is None:
            # Vytvoriť prvotnú správu
            embed = discord.Embed(title="Chceš mať prehľad o cenách paliva?",
                                  description="Pridaj si rolu, aby si mal prehľad o cenách pohonných hmôt.")
            sent_message = await channel.send(embed=embed)

            # Pridať reakciu na prvotnú správu
            await sent_message.add_reaction('🚗')

        else:
            print("Reaction Post už existuje")

    else:
        print("Kanál s daným ID neexistuje alebo bot nemá oprávnenie posielať správy do tohto kanálu.")

    while True:
        now = datetime.now()
        target_time = datetime(now.year, now.month, now.day, 7, 0)  # Set target time (7:00 AM)

        # Calculate delay until target time
        delta = target_time - now
        if delta.total_seconds() <= 0:
            delta = timedelta(days=1) + delta

        await asyncio.sleep(delta.total_seconds())

        # Execute daily task (price update)
        await daily_prices()


@client.event
async def on_raw_reaction_add(payload):
    # Ensure all necessary information is available
    if not payload.channel_id or not payload.message_id or not payload.member:
        return

    # Verify channel and message IDs match the desired interaction
    if payload.channel_id != 1209520390963994624 or payload.message_id != 1209528076766281758:
        return

    # Fetch the guild and the target role
    guild = client.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name='Tankovanie')

    # Handle potential errors gracefully
    if not guild or not role:
        print(f"Error processing reaction: Guild or role not found.")
        return

    # Check if the member already has the role
    if payload.member in role.members:
        print(f"Užívateľ {payload.member.name} už má rolu {role.name}.")
        return

    # Add the role to the user and provide feedback
    try:
        await payload.member.add_roles(role)
        print(f'Užívateľ {payload.member.name} bol úspešne pridaný do roly {role.name}')
    except discord.Forbidden:
        print(f"Bot nemá oprávnenie pridať rolu {role.name} užívateľovi {payload.member.name}.")


# HANDLING INCOME MESSAGES
@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f"{username} sent message: {user_message} in channel: ({channel})")
    await send_message(message, user_message)


# MAIN ENTRY POINT
def main():
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
