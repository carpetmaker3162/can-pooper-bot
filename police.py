import string

lwords = tuple(open("/Users/neng/desktop/nengstuff/code/algorithm/words.txt", "r").read().split("\n"))

def search_same_length(checkword):
    words = [w for w in lwords if sum(a != b for a, b in zip(checkword, w)) == 1]
    words = list(filter(lambda a: len(a) == len(checkword), words))
    return words

async def police(message, exempted):
    punctuation = (".", "!", "?")
    curse_words = ("fuck","shit","crap","bitch","faggot","fag","dick","cock")
    if message.author.id in exempted:
        return
    if tuple(message.content)[0].lower() == tuple(message.content)[0] and tuple(message.content)[0] not in punctuation:
        await message.reply("Lol that sentence needs to be capitalized")
    if tuple(message.content)[-1] not in punctuation:
        await message.reply("no punctuation yikes")
    for word in message.content.split():
        input_word = ''.join(list(filter(lambda a: a in string.ascii_lowercase, list(word.lower()))))
        if word.lower() in curse_words:
            await message.reply(f"What? Why did you need to swear? Surely you can get your point across without using words like '{word}'")
        
        if input_word in lwords:
            continue

        words = search_same_length(input_word)

        if not words:
            await message.reply(f"Your spelling is pretty bad, '{word}' is not a word, and there are literally no matches for something similar")
            continue
        matches = []
        for i in words:
            matches.append(i)
        newl = "\n"
        for i, j in enumerate(matches):
            matches[i] = f"`{matches[i]}`"
        await message.reply(f"Hello? '{word}' is not a word. In case you need a helping hand, here are some words similar to '{word}':\n{newl.join(matches)}")