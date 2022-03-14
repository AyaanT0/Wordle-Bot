import datetime
import random

import nextcord

popular_words = open("dict-popular.txt").read().splitlines()
all_words = set(word.strip() for word in open("dict-sowpods.txt"))

EMOJI_CODES = {
    "green": {
        "a": "<:1f1e6:953052446152884234>",
        "b": "<:1f1e7:953052445733429269>",
        "c": "<:1f1e8:953052446169653258>",
        "d": "<:1f1e9:953052446173839440>",
        "e": "<:1f1ea:953052446282879007>",
        "f": "<:1f1eb:953052446161244240>",
        "g": "<:1f1ec:953052446144479234>",
        "h": "<:1f1ed:953052446182228028>",
        "i": "<:1f1ee:953052446148657204>",
        "j": "<:1f1ef:953052446157062234>",
        "k": "<:1f1f0:953052446144483359>",
        "l": "<:1f1f1:953052446127685712>",
        "m": "<:1f1f2:953052446182219816>",
        "n": "<:1f1f3:953052446148677632>",
        "o": "<:1f1f4:953052446245130240>",
        "p": "<:1f1f5:953052446500982874>",
        "q": "<:1f1f6:953052446173855774>",
        "r": "<:1f1f7:953052446215786566>",
        "s": "<:1f1f8:953052446232559717>",
        "t": "<:1f1f9:953052446190600192>",
        "u": "<:1f1fa:953052445930577941>",
        "v": "<:1f1fb:953052446186430515>",
        "w": "<:1f1fc:953052446291279882>",
        "x": "<:1f1fd:953052446282891365>",
        "y": "<:1f1fe:953052533960634378>",
        "z": "<:1f1ff:953052533964824586>",
    },
    "yellow": {
        "a": "<:1f1e6:953052325675683880>",
        "b": "<:1f1e7:953052325499527199>",
        "c": "<:1f1e8:953052325520502784>",
        "d": "<:1f1e9:953052325721821306>",
        "e": "<:1f1ea:953052325243654185>",
        "f": "<:1f1eb:953052325516288060>",
        "g": "<:1f1ec:953052325533085776>",
        "h": "<:1f1ed:953052325537271929>",
        "i": "<:1f1ee:953052325537267742>",
        "j": "<:1f1ef:953052325512101958>",
        "k": "<:1f1f0:953052325528895498>",
        "l": "<:1f1f1:953052325495308338>",
        "m": "<:1f1f2:953052325558239272>",
        "n": "<:1f1f3:953052325507924079>",
        "o": "<:1f1f4:953052325528891412>",
        "p": "<:1f1f5:953052325604388884>",
        "q": "<:1f1f6:953052325579227156>",
        "r": "<:1f1f7:>953052325809893446",
        "s": "<:1f1f8:953052325692473394>",
        "t": "<:1f1f9:953052325793124412>",
        "u": "<:1f1fa:953052325524693003>",
        "v": "<:1f1fb:953052325860233296>",
        "w": "<:1f1fc:953052325692440676>",
        "x": "<:1f1fd:953052325784748032>",
        "y": "<:1f1fe:953052325671497738>",
        "z": "<:1f1ff:953052325709217792>",
    },
    "gray": {
        "a": "<:1f1e6:953052566114156554>",
        "b": "<:1f1e7:953052566114172968>",
        "c": "<:1f1e8:953052566076424202>",
        "d": "<:1f1e9:953052565925421068>",
        "e": "<:1f1ea:953052565824733217>",
        "f": "<:1f1eb:953052566068011028>",
        "g": "<:1f1ec:953052565677957201>",
        "h": "<:1f1ed:953052566139338862>",
        "i": "<:1f1ee:953052566168686613>",
        "j": "<:1f1ef:953052566068027473>",
        "k": "<:1f1f0:953052566382579722>",
        "l": "<:1f1f1:953052566252580974>",
        "m": "<:1f1f2:953052566458077204>",
        "n": "<:1f1f3953052565896065025:>",
        "o": "<:1f1f4:953052566143524884>",
        "p": "<:1f1f5:953052566177071196>",
        "q": "<:1f1f6:953052566118334535>",
        "r": "<:1f1f7:953052566135132260>",
        "s": "<:1f1f8:953052566378397747>",
        "t": "<:1f1f9:953052566118350898>",
        "u": "<:1f1fa:953052566374195251>",
        "v": "<:1f1fb:953052566424539206>",
        "w": "<:1f1fc:953052566386798643>",
        "x": "<:1f1fd:953052566265135134>",
        "y": "<:1f1fe:953052566525206528>",
        "z": "<:1f1ff:953052566424518797>",
    },
}


def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray
    Args:
        word (str): The word to be colored
        answer (str): The answer to the word
    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters
    Returns:
        str: A string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(user: nextcord.User, puzzle_id: int) -> nextcord.Embed:
    """
    Generate an embed for a new puzzle given the puzzle id and user
    Args:
        user (nextcord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID
    Returns:
        nextcord.Embed: The embed to be sent
    """
    embed = nextcord.Embed(title="Wordle")
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command /play!\n"
        "To guess, reply to this message with a word."
    )
    return embed


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    """
    Updates the embed with the new guesses
    Args:
        embed (nextcord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the user
    Returns:
        nextcord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    """
    Validates a word
    Args:
        word (str): The word to validate
    Returns:
        bool: Whether the word is valid
    """
    return word in all_words


def random_puzzle_id() -> int:
    """
    Generates a random puzzle ID
    Returns:
        int: A random puzzle ID
    """
    return random.randint(0, len(popular_words) - 1)


def daily_puzzle_id() -> int:
    """
    Calculates the puzzle ID for the daily puzzle
    Returns:
        int: The puzzle ID for the daily puzzle
    """
    # calculate days since 1/1/2022 and mod by the number of puzzles
    num_words = len(popular_words)
    time_diff = datetime.datetime.now().date() - datetime.date(2022, 1, 1)
    return time_diff.days % num_words


def is_game_over(embed: nextcord.Embed) -> bool:
    """
    Checks if the game is over in the embed
    Args:
        embed (nextcord.Embed): The embed to check
    Returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description


def generate_info_embed() -> nextcord.Embed:
    """
    Generates an embed with information about the bot
    Returns:
        nextcord.Embed: The embed to be sent
    """
    join_url = "https://discord.com/oauth2/authorize?client_id=952966077887971401&permissions=11328&scope=bot%20applications.commands"
    return nextcord.Embed(
        title="About Discord Wordle Bot",
        description=(
            "Discord Wordle Bot is a game of wordle-like puzzle solving. Ian sucks btw.\n\n"
            "**You can start a game with**\n\n"
            ":sunny: `/play daily` - Play the puzzle of the day\n"
            ":game_die: `/play random` - Play a random puzzle\n"
            ":boxing_glove: `/play id <puzzle_id>` - Play a puzzle by ID\n\n"
            f"<:member_join:942985122846752798> [Add this bot to your server]({join_url})\n"
        ),
    )


async def process_message_as_guess(
    bot: nextcord.Client, message: nextcord.Message
) -> bool:
    """
    Check if a new message is a reply to a Wordle game.
    If so, validate the guess and update the bot's message.
    Args:
        bot (nextcord.Client): The bot
        message (nextcord.Message): The new message to process
    Returns:
        bool: True if the message was processed as a guess, False otherwise
    """
    # get the message replied to
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return False
    parent = ref.resolved

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != bot.user.id:
        return False

    # check that the message has embeds
    if not parent.embeds:
        return False

    embed = parent.embeds[0]

    guess = message.content.lower()

    # check that the user is the one playing
    if (
        embed.author.name != message.author.name
        or embed.author.icon_url != message.author.display_avatar.url
    ):
        reply = "Start a new game with /play"
        if embed.author:
            reply = f"This game was started by {embed.author.name}. " + reply
        await message.reply(reply, delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the game is not over
    if is_game_over(embed):
        await message.reply(
            "The game is already over. Start a new game with /play", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that a single word is in the message
    if len(message.content.split()) > 1:
        await message.reply(
            "Please respond with a single 5-letter word.", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the word is valid
    if not is_valid_word(guess):
        await message.reply("That is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass

    return True
