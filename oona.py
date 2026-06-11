import comics
import datetime
import discord
from discord.ext import commands
import os

DISCORD_KEY = os.environ.get("DISCORD_KEY")

all_comics = comics.directory.listall()

bot = commands.Bot()

commandnames = [
    ("calvin", "calvinandhobbes", "Calvin and Hobbes"),
    ("nancy", "nancy", "Nancy"),
    ("foxtrot", "foxtrot", "FoxTrot"),
]


def style_comic(name, date, url, image_url):
    dateparts = date.split("-")
    d = datetime.datetime(int(dateparts[0]), int(dateparts[1]), int(dateparts[2]))
    return discord.Embed(
        title=name,
        description=d.strftime("%A, %B %d, %Y"),
        image=image_url,
        color=discord.Colour.blue(),
        url=url,
        footer=discord.EmbedFooter(text="gocomics.com"),
    )


for com, endpoint, title in commandnames:

    @bot.slash_command(
        name=com,
        description=f"pull up a {title} strip",
        options=[
            discord.Option(
                input_type=discord.SlashCommandOptionType.string,
                name="date",
                description="[yyyy-mm-dd] pull a specific date (random if omitted)",
                required=False,
            ),
        ],
    )
    async def get_comic(ctx, date):
        await get_random(ctx, endpoint, date)


@bot.slash_command(
    name="comicsearch",
    description="search any comic",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="comic",
            description="the comic to search for",
            required=True,
            autocomplete=discord.utils.basic_autocomplete(all_comics),
        ),
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="date",
            description="[yyyy-mm-dd] pull a specific date (random if omitted)",
            required=False,
        ),
    ],
)
async def get_random(ctx, endpoint, date):
    await ctx.defer()
    i = 0
    while True:
        i += 1
        try:
            r = comics.search(endpoint, date="random" if date is None else date)
            r.image_url
            break
        except:
            if date is not None or i > 50:
                await ctx.respond(
                    f"Could not find {r.title} for {r.date}."
                    if date is not None
                    else f"Unable to find {r.title} on random date in 50 attempts. Try again."
                )
                return
    await ctx.respond(embed=style_comic(r.title, r.date, r.url, r.image_url))


@bot.slash_command(
    name="listall",
    description="list all available comics",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="startswith",
            description="show only comics that start with this",
            required=False,
        )
    ],
)
async def listall(ctx, letter):
    with open("allcomics.txt", "w") as f:
        f.write(
            "\n".join(
                all_comics
                if letter is None
                else filter(lambda c: c.startswith(letter), all_comics)
            )
        )
    with open("allcomics.txt", "r") as f:
        await ctx.respond(
            file=discord.File(
                f,
                filename="allcomics.txt" if letter is None else f"comics-{letter}.txt",
            )
        )


bot.run(DISCORD_KEY)
