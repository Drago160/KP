import pandas as pd

number = 3
with open('/home/stase/home/stase/PycharmProjects/testRepo/' + str(
        number) + '/black.json', encoding='utf-8') as inputfile:
    df = pd.read_json(inputfile)

df.to_csv('/home/stase/home/stase/PycharmProjects/testRepo/' + str(
        number) + '/black.csv',
          encoding='utf-8', index=False)
