# TODO
from cs50 import get_string

text = get_string("Text: ")

words = 0
letters = 0
sentences = 0

for char in text:
  if char.isalpha():
    letters += 1

  if char.isspace():
    words += 1

  if char in ['?', '.', '!']:
    sentences += 1


words += 1

L = (letters * 100 )/ words
S = (sentences * 100 )/ words

calc = int((0.0588 * L - 0.296 * S -15.8) + 0.5)

if calc < 1:
  print('Before Grade 1')
elif calc >= 16:
  print('Grade 16+')

else:
  print(f'Grade {calc}')




