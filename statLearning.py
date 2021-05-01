from string import ascii_lowercase
import argparse

# parse arguments, determine whether the user is using the program correctly
def parse_args():
    parser = argparse.ArgumentParser(description='some speech thing.')
    parser.add_argument('filename', type=str, help='The input filename')
    return parser.parse_args()

# read the file, parse out all non-word characters, seperate syllables
def readFile(filename):
    with open(filename) as fp:
        text = fp.read().lower().replace("–", " ").replace("\n", " ").replace("-", " ")
        # print(text)
        newtext = ""
        for letter in text:
            if letter in ascii_lowercase or letter == " ":
                newtext += letter

        return newtext.split()

# converts all the numbers of occurrrences of each syllable to probabilities
def convertToProb(table):
    for i in table:
        total = 0
        for j in table[i]:
            total += table[i][j]        
        for j in table[i]:
            table[i][j] /= total
    return table

# determines if two syllables are part of the same word
def isPartOfSameWord(table, syl, nextSyl):
    #if the syllable has more than an 80% chance of ocurring after, it's in the word
    return table[syl][nextSyl] >= 0.8

args = parse_args()
filename = args.filename
table = {}
SyllList = readFile(filename)

# traverse the list of syllables
for i in range(len(SyllList) - 1):
    syl, nextSyl = SyllList[i], SyllList[i + 1]
    # if the syl isn't in the table, add it to the dictionary and include an instance 
    # of the next syl in its dictionary input
    if table.get(syl) is None:
        table[syl] = {nextSyl: 1}
    # if the syl is already in the dictionary, along with the next syl in its
    # dicitionary input, increment the count
    elif nextSyl in table[syl]:
        table[syl][nextSyl] += 1
    # if the syl is in the dictionary and the next syl hasn't occurred after 
    # it yet, set it
    else:
        table[syl][nextSyl] = 1

# print(table)

convertToProb(table)

# for i in table:
#     print(i, end = ": ")
#     print(table[i])

for i in range(len(SyllList) - 1):
    syl, nextSyl = SyllList[i], SyllList[i + 1]
    print (syl, end = "")
    # likelihood that the next syllable is not part of the current word
    if not isPartOfSameWord(table, syl, nextSyl):
        print (" ", end = "")
    #otherwise, it's part of the current word
# print the last syllable
print(SyllList[(len(SyllList) - 1)])
print("\n")