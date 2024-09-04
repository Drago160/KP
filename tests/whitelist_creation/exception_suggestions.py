import json

number = 1
with open("/home/stase/home/stase/PycharmProjects/testRepo/" + str(
        number) + "/white.json") as f:
    senteceDict = json.load(f)
    for text in senteceDict:
        whitelist = ["ищем", "ищет", "ищу", "требуется",  "требуются",  "looking for", "lookingfor", "lookfor", "we need", "в поиске", "seeking", "необходим"]
        if not any(word in text for word in whitelist):
            words = text.split()
            for i in range(0, len(words), 10):
                end = min(i + 10, len(words))
                print(" ".join(words[i:end]))
            input()
