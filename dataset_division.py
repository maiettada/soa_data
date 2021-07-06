

def sort_list(lis):
    lis.sort(key=lambda x: x[0])


def prendo_frase_fino_a(document, char_index):
    selection = ""
    remaining = ""
    if char_index == -1:
        selection = document
        remaining = None
    else:
        selection = document[:char_index]
        remaining = document[char_index + 2:]
    return [selection, remaining]


def prendo_labels_fino_a(json_list, char_index):
    selection = []
    remaining = []
    if char_index == -1:
        selection = json_list
        remaining = None
    else:
        selection = [[st, end, word] for [st, end, word] in json_list if end <= char_index]
        # the following labels must be indexed starting from the new sentence.
        # Starting Point and Ending Point of a label: must be decreased by (char_index+2)
        remaining = [[st - char_index - 2, end - char_index - 2, word] for [st, end, word] in json_list if
                     end > char_index]
    return [selection, remaining]


def period_sect(json_list, txt, a):
    """

    :param json_list:
    :param txt:
    :return:
    """
    # = int(input('Enter a number: '))
    # separator =
    x = txt.find(". ")
    json_sublist = []
    [frase, txt] = prendo_frase_fino_a(txt, x) #separator len
    print(frase,"||,", txt)
    [json_sublist, json_list] = prendo_labels_fino_a(json_list, x)
    print(json_sublist,"||,", json_list)
    print()
    '''print(x) #char index
    print(frase)
    print(json_sublist)
    print(documento)
    print(json_list)'''
    a.append([frase, json_sublist])
    return x, json_list, txt

#dividing document "i" in periods
# trivial case: every sentence is labelled
a = []
txt = "Hello. Welcome. Sit down. "
json_list = [[0, 5, "p1"], [7, 14, "p2"], [16, 19, "p3w1"], [20, 24, "p3w2"]]
sort_list(json_list)
found = 0
while found!=-1:
    found, json_list, txt = period_sect(json_list, txt, a)
print("-----")
print("-----")
print("-----")
print(a)
#dividing document "i" in periods
# trivial case: every sentence is labelled
a = []
txt = "Hello Paperino. Welcome Minnieee. Sit down Topolino. "
json_list = [[6,14, "paperino"], [24,32, "minnie"], [43, 51, "topolino"]]
sort_list(json_list)
found = 0
while found!=-1:
    found, json_list, txt = period_sect(json_list, txt, a)
print("-----")
print(a)


