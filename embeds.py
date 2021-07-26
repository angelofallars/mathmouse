import discord


def print_embed(title="math.mouse",
                description=None,
                footer=None):
    '''Return a Discord embedded message.
    '''

    embed = discord.Embed(title=title,
                          description=description,
                          color=0x2ab245)
    if footer:
        embed.set_footer(text=footer)

    return embed
