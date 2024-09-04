import json
import pymorphy2
from functools import cmp_to_key

comparing = {}

# analyzer = pymorphy2.MorphAnalyzer()
# parser = analyzer.parse("ищу")
# print(parser[0].inflect({'3per'}))
number = 4
white_length = 0
with open("/home/stase/home/stase/PycharmProjects/testRepo/" + str(number) +"/white.json") as f:
    senteceDict = json.load(f)
    print("white length: ", len(senteceDict))
    white_length = len(senteceDict)
    for text in senteceDict:
        words = set(text.replace(",", " ")
                    .replace("!", " ")
                    .replace(".", " ")
                    .replace(";", " ")
                    .replace("?", " ")
                    .replace("+", " ")
                    .replace("#", " ").split(" "))
        for word in words:
            arr = comparing.get(word, [0, 0])
            arr[0] += 1
            comparing[word] = arr
with open("/home/stase/home/stase/PycharmProjects/testRepo/" + str(number) +"/black.json") as f:
    senteceDict = json.load(f)
    print("black length: ", len(senteceDict))
    for text in senteceDict[:white_length]:
        # !.;?+#"
        words = set(text
                    .replace(",", " ")
                    .replace("!", " ")
                    .replace(".", " ")
                    .replace(";", " ")
                    .replace("?", " ")
                    .replace("+", " ")
                    .replace("#", " ")
                    .split(" "))
        for word in words:
            arr = comparing.get(word, [0, 0])
            arr[1] += 1
            comparing[word] = arr

arr = list(comparing.items())
arr2 = sorted(arr, key=cmp_to_key(lambda t, s: t[1][0] - t[1][1] - (s[1][0] - s[1][1])))
for val in arr2:
    print(val)
# for k, v in comparing.items():
#     print(k, ": ", v)