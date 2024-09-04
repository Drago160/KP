import csv
import json

# first = False
# second = False
number = 4
trusted_strong_blacklist = set()
trusted_strong_whitelist = set()
trusted_week_blacklist = set()
trusted_week_whitelist = set()


def contains_any(text, dictionary):
    for word in dictionary:
        if word in row:
            return True, word
    return False, None


for path_set in [(trusted_strong_whitelist, "trusted_strong_whitelist"),
                 (trusted_strong_blacklist, "trusted_strong_blacklist"),
                 (trusted_week_whitelist, "trusted_week_whitelist"),
                 (trusted_week_blacklist, "trusted_week_blacklist"),
                 ]:
    with open("trusted/" + path_set[1]) as f:
        path_set[0].update(set([word.replace("\n", "") for word in f.readlines()]))
        if "" in path_set[0]:
            path_set[0].remove("")

print(trusted_strong_whitelist)

with open('/home/stase/home/stase/PycharmProjects/testRepo/' + str(
        number) + '/Messages_Request_From_2024_04_29.csv',
          newline='') as csvfile:
    spamreader = [line[2] for line in csv.reader(csvfile, delimiter=',', quotechar='|')]
    white = []
    black = []
    cnt = 0
    # print(spamreader)
    for row in set(spamreader):
        cnt += 1
        in_trusted_black, black_word = contains_any(row, trusted_strong_blacklist)
        in_trusted_white, white_word = contains_any(row, trusted_strong_whitelist)
        if in_trusted_white and not in_trusted_black:
            white.append(row)
        elif in_trusted_black and not in_trusted_white:
            black.append(row)
        else:
            if in_trusted_white and in_trusted_black:
                print("Strong black (" + black_word +") and strong white (" + white_word + ") in one sentence")
            else:
                in_trusted_black, black_word = contains_any(row,
                                                            trusted_week_blacklist)
                in_trusted_white, white_word = contains_any(row,
                                                            trusted_week_whitelist)
                if in_trusted_white and not in_trusted_black:
                    white.append(row)
                    continue
                elif in_trusted_black and not in_trusted_white:
                    black.append(row)
                    continue

            words = row.split()
            print(cnt)
            for i in range(0, len(words), 10):
                end = min(i + 10, len(words))
                print(" ".join(words[i:end]))

            inp = input()
            if inp in ["`", "1", "2", "3", "q", "w", "e"]:
                white.append(row)
                # first = True
            else:
                black.append(row)
                # second = True
            # if first and second:
            #     break

with open('/home/stase/home/stase/PycharmProjects/testRepo/' + str(number) + '/white.json',
          mode='w') as f:
    json.dump(white, f, ensure_ascii=True)

with open('/home/stase/home/stase/PycharmProjects/testRepo/' + str(number) + '/black.json',
          mode='w') as f:
    json.dump(black, f, ensure_ascii=True)
