import comics
import datetime
import discord
from discord.ext import commands
import os
from random import randint

DISCORD_KEY = os.environ.get("DISCORD_KEY")

all_comics = comics.directory.listall()

nancy_start = comics.directory.get_start_date("nancy")

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


# for com, endpoint, title in commandnames:
#
#    def make_f(ctx, date, k=endpoint):
#        async def f():
#            print(date, k)
#            await get_random(ctx, date, k)
#
#        return f
#
#    @bot.slash_command(
#        name=com,
#        description=f"pull up a {title} strip",
#        options=[
#            discord.Option(
#                input_type=discord.SlashCommandOptionType.string,
#                name="date",
#                description="[yyyy-mm-dd] pull a specific date (random if omitted)",
#                required=False,
#            ),
#        ],
#    )
#    async def get_comic(ctx, date):
#        await make_f(ctx, date)()


@bot.slash_command(
    name="pearls",
    description=f"pull up a Pearls Before Swine strip",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="date",
            description="[yyyy-mm-dd] pull a specific date (random if omitted)",
            required=False,
        ),
    ],
)
async def pearls(ctx, date):
    await get_random(ctx, "pearlsbeforeswine", date)


@bot.slash_command(
    name="cathy",
    description=f"pull up a Cathy strip",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="date",
            description="[yyyy-mm-dd] pull a specific date (random if omitted)",
            required=False,
        ),
    ],
)
async def cathy(ctx, date):
    await get_random(ctx, "cathy", date)


@bot.slash_command(
    name="calvin",
    description=f"pull up a Calvin and Hobbes strip",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="date",
            description="[yyyy-mm-dd] pull a specific date (random if omitted)",
            required=False,
        ),
    ],
)
async def calvin(ctx, date):
    await get_random(ctx, "calvinandhobbes", date)


@bot.slash_command(
    name="foxtrot",
    description=f"pull up a Foxtrot strip",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="date",
            description="[yyyy-mm-dd] pull a specific date (random if omitted)",
            required=False,
        ),
    ],
)
async def foxtrot(ctx, date):
    await get_random(ctx, "foxtrot", date)


@bot.slash_command(
    name="nancyclassic",
    description=f"pull up a Nancy Classics strip",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="date",
            description="[yyyy-mm-dd] pull a specific date (random if omitted)",
            required=False,
        ),
    ],
)
async def nancyclassic(ctx, date):
    await get_random(ctx, "nancy-classics", date)


@bot.slash_command(
    name="nancy",
    description=f"pull up a Nancy strip",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="date",
            description="[yyyy-mm-dd] pull a specific date (random if omitted)",
            required=False,
        ),
    ],
)
async def nancy(ctx, date):
    await get_random(ctx, "nancy", date)


@bot.slash_command(
    name="garfield",
    description=f"pull up a Garfield strip",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="date",
            description="[yyyy-mm-dd] pull a specific date (random if omitted)",
            required=False,
        ),
    ],
)
async def garfield(ctx, date):
    await get_random(ctx, "garfield", date)


@bot.slash_command(
    name="nancyartist",
    description=f"pull up a Nancy strip by a specified artist",
    options=[
        discord.Option(
            input_type=discord.SlashCommandOptionType.string,
            name="artist",
            description="artist to pull (probably not 100% accurate)",
            required=True,
            choices=["bushmiller", "gilchrist", "jaimes", "cash"],
        ),
    ],
)
async def nancyartist(ctx, artist):
    daterange = {
        "bushmiller": (nancy_start, "1995-09-02"),
        "gilchrist": ("1995-09-04", "2018-02-18"),
        "jaimes": ("2018-04-09", "2025-12-31"),
        "cash": ("2026-01-01", datetime.datetime.now().strftime("%Y-%m-%d")),
    }[artist]
    await get_random(ctx, "nancy", None, daterange)


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
async def get_random(ctx, endpoint, date, daterange=None):
    await ctx.defer()
    i = 0
    while True:
        i += 1
        try:
            effectivedate = None
            if daterange is not None:
                start = datetime.datetime.strptime(daterange[0], "%Y-%m-%d")
                end = datetime.datetime.strptime(daterange[1], "%Y-%m-%d")
                rand_days = randint(0, (end - start).days)
                effectivedate = (start + datetime.timedelta(days=rand_days)).strftime(
                    "%Y-%m-%d"
                )
            elif date is not None:
                effectivedate = date
            r = comics.search(
                endpoint, date="random" if effectivedate is None else effectivedate
            )
            r.image_url
            break
        except comics.exceptions.InvalidEndpointError:
            await ctx.respond(f"`{endpoint}` is not a valid GoComics endpoint.")
            return
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
