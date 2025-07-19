import discord
from discord import app_commands
from discord.ext import commands
# tools
import random
# words :D
import nltk
nltk.download('reuters')
from nltk.corpus import words

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
word = None

@bot.event
async def on_ready():
    await bot.tree.sync() #
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="hello", description="Test")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}!")

@bot.tree.command(name="play", description="Zagraj z podaną liczbą")
@app_commands.describe(number="Wpisz jakąś liczbę")
async def play(interaction: discord.Interaction, number: int):
    global word
    word_list = words.words()  # poprawka tutaj
    filtered_words = [w for w in word_list if len(w) == number]
    if not filtered_words:
        await interaction.response.send_message(f"There no words with {number} length ;c")
        return

    word = random.choice(filtered_words)
    print(f"New word to guess! {word}")

    embed = discord.Embed(
    title="New Wordle game!",
    description=f"Respond to my message to start!",
    color=discord.Color.blue()  # możesz zmienić kolor
    )
    embed.set_author(name=bot.user.display_name, url="https://github.com/R3akeOn3", icon_url="https://i.imgur.com/y3m6x7h.png")
    embed.set_thumbnail(url=interaction.user.avatar.url)
    embed.add_field(name="Word Lenght", value=f"Lenght {number}", inline=True)
    embed.set_footer(text="Made in China",)

    await interaction.response.send_message(embed=embed)
    
@bot.event
async def on_message(message):
    global word
    if message.author == bot.user:
        return

    if message.reference:
        replied_message = await message.channel.fetch_message(message.reference.message_id)
        if replied_message.author == bot.user and word is not None:
            guess = message.content.lower()
            secret = word.lower()

            if guess == secret:
                embed = discord.Embed(
                    title="You won! ✔",
                    description="Wow, that's awesome!",
                    color=discord.Color.green()
                )
            elif len(guess) < len(secret):
                embed = discord.Embed(
                    title="Your answer is too short! ❌",
                    description="Try something longer!",
                    color=discord.Color.red()
                )
            elif len(guess) > len(secret):
                embed = discord.Embed(
                    title="Your answer is too long! ❌",
                    description="Try something shorter!",
                    color=discord.Color.red()
                )
            else:
                result = ""
                for i in range(len(secret)):
                    if guess[i] == secret[i]:
                        result += "🟩"
                    elif guess[i] in secret:
                        result += "🟧"
                    else:
                        result += "⬛"
                embed = discord.Embed(
                    title=result,
                    description="**Keep trying! 😶**",
                    color=discord.Color.yellow()
                )

            embed.set_author(name=bot.user.display_name, url="https://github.com/R3akeOn3", icon_url="https://i.imgur.com/y3m6x7h.png")
            embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else "https://i.imgur.com/y3m6x7h.png")
            embed.set_footer(text="Made in China")
            await message.channel.send(embed=embed)

    await bot.process_commands(message)

bot.run("ur_token")
