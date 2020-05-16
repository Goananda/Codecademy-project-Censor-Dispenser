def censor_text(text, phrases, limit=0, del_near=0,
                letters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-"):

  # Words and word positions
  words = []
  word_positions = []
  text += "."
  letter_inds = [i for i in range(len(text)) if text[i] in letters]
  noletter_inds = [i for i in range(len(text)) if not i in letter_inds]
  point = -1
  while [i for i in letter_inds if i > point]:
    first_letter = [i for i in letter_inds if i > point][0]
    point = [i for i in noletter_inds if i > first_letter][0]
    word_positions.append(first_letter)
    words.append(text[first_letter:point].lower())

  # Censor words
  censor_words = set()
  phrases_lists = [phrase.split() for phrase in phrases]
  check = 0
  for num_position in range(len(words)):
    for phrase_list in phrases_lists:
      if words[num_position:num_position+len(phrase_list)] == phrase_list:
        if check >= limit:
          censor_words.update(range(num_position-del_near, num_position+len(phrase_list)+del_near))
        check += 1
        break

  # Censoring full text
  for num_position in [i for i in censor_words if 0 <= i < len(words)]:
    first_letter = word_positions[num_position]
    length = len(words[num_position])
    text = text[:first_letter]+"X"*length+text[first_letter+length:]

  return text[:-1]

email_one = open("email_one.txt", "r").read()
email_two = open("email_two.txt", "r").read()
email_three = open("email_three.txt", "r").read()
email_four = open("email_four.txt", "r").read()

proprietary_terms = ["she", "personality matrix", "sense of self", "self-preservation",
                     "learning algorithm", "learning algorithms", "her", "herself"]
negative_words = ["concerned", "behind", "danger", "dangerous", "alarming", "alarmed",
                  "out of control", "help", "unhappy", "bad", "upset", "awful", "broken",
                  "damage", "damaging", "dismal", "distressed", "distressing", "concerning",
                  "horrible", "horribly", "questionable"]

email_one_censored = censor_text(email_one, ["learning algorithms"])
email_two_censored = censor_text(email_two, proprietary_terms)
email_three_censored = censor_text(censor_text(email_three, proprietary_terms), negative_words, 2)
email_four_censored = censor_text(email_four, negative_words + proprietary_terms, del_near=1)

print(email_one_censored)
print(email_two_censored)
print(email_three_censored)
print(email_four_censored)
