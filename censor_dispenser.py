import re
from itertools import chain

def censor(text, censor_list, limit=0, near=0):

    re_word = lambda word: rf"(?i)([\w'-]*[^\w'-]*){{{near}}}\b{word}\b([^\w'-]*[\w'-]*){{{near}}}"
    links = chain(*[re.finditer(re_word(word), text) for word in censor_list])
    for link in sorted(links, key=lambda x: x.start())[limit:]:
        text = text[:link.start()] + re.sub(r"[\w'-]", "X", link.group()) + text[link.end():]

    return text

email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation",
                     "learning algorithms ", "her", "herself"]
negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed",
                  "out of control", "help", "unhappy", "bad", "upset", "awful", "broken",
                  "damage", "damaging", "dismal", "distressing", "distressed", "concerning",
                  "horrible", "horribly", "questionable"]

print(censor(email_one, ["learning algorithms"]))
print(censor(email_two, proprietary_terms))
print(censor(censor(email_three, proprietary_terms), negative_words, 2))
print(censor(email_four, proprietary_terms + negative_words, near=1))