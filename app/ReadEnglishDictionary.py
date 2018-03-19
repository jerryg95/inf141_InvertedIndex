def read_en_dict():
    with open("english_dictionary.txt", "r") as ed:
        en_dict = set(line.lower().strip() for line in ed)
    return en_dict
