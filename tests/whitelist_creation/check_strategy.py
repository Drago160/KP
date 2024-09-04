import json

folders = [i for i in range(1, 5)]

trusted_strong_blacklist = set()
trusted_strong_whitelist = set()
trusted_week_blacklist = set()
trusted_week_whitelist = set()
trusted_strong_blackdict = dict()
trusted_strong_whitedict = dict()
trusted_week_blackdict = dict()
trusted_week_whitedict = dict()

strong_conflict = dict()
week_conflict = dict()

for path_set in [(trusted_strong_whitelist, trusted_strong_whitedict,
                  "trusted_strong_whitelist"),
                 (trusted_strong_blacklist, trusted_strong_blackdict,
                  "trusted_strong_blacklist"),
                 (trusted_week_whitelist, trusted_week_whitedict,
                  "trusted_week_whitelist"),
                 (trusted_week_blacklist, trusted_week_blackdict,
                  "trusted_week_blacklist"),
                 ]:
    with open("trusted/" + path_set[2]) as f:
        path_set[0].update(
            set([word.replace("\n", "") for word in f.readlines()]))
        if "" in path_set[0]:
            path_set[0].remove("")
    for word in f.readlines():
        word = word.replace("\n", "")
        path_set[1][word] = {"in_white": 0, "in_black": 0}



def parse_color(color, blackdict, whitedict, description):
    with open(str(i) + "/" + color + ".json") as f:
        texts = json.load(f)
        for text in texts:
            black = []
            for word in blackdict:
                if word in text:
                    black.append(word)
                    blackdict[word]["in_" + color] += 1
            for word in whitedict:
                white = []
                if word in text:
                    white.append(word)
                    whitedict[word]["in_" + color] += 1



for i in folders:
    parse_color("black")


