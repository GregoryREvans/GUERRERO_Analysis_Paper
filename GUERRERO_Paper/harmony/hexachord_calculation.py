import itertools
key = {'0':'C', '1':'C#', '2':'D', '4':'E', '7':'G', '8':'Ab', }
for x in itertools.combinations('012478', 3):
    print(x)
    trichord = []
    for y in x:
        trichord.append(key[y])
    print(trichord)
