from distribution_automaton import DistributionAutomaton

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
    [json_sublist, json_list] = prendo_labels_fino_a(json_list, x)
    '''print(x) #char index
    print(frase)
    print(json_sublist)
    print(documento)
    print(json_list)'''
    if x != -1:
        a.append([frase, json_sublist])
    return x, json_list, txt

#dividing document "i" in periods
a = []
txt = "Hello. Welcome. Sit down. "
json_list = [[0, 5, "p1"], [7, 14, "p2"], [16, 19, "p3w1"], [20, 24, "p3w2"]]
sort_list(json_list)
found = 0
while found!=-1:
    found, json_list, txt = period_sect(json_list, txt, a)
print("-----")
print(a)

#initialization of automata
soa_classifiche = ['I', 'II', 'III-bis', 'IV', 'IV-bis', 'V', 'VI', 'VII', 'VIII']
soa_categorie = ['OG-1', 'OG-2', 'OG-3', 'OG-4', 'OG-5', 'OG-6', 'OG-7', 'OG-8', 'OG-9', 'OG-10',
                 'OG-11', 'OG-12', 'OG-13', 'OS-1', 'OS-2A', 'OS-2B', 'OS-3', 'OS-4', 'OS-5', 'OS-6',
                 'OS-7', 'OS-8', 'OS-9', 'OS-10', 'OS-11', 'OS-12A', 'OS-12B', 'OS-13',
                 'OS-14', 'OS-15', 'OS-16', 'OS-17', 'OS-18A', 'OS-18B', 'OS-19', 'OS-20A',
                 'OS-20B', 'OS-21', 'OS-22', 'OS-23', 'OS-24', 'OS-25', 'OS-26', 'OS-27',
                 'OS-28', 'OS-29', 'OS-30', 'OS-31', 'OS-32', 'OS-33', 'OS-34', 'OS-35']
label_list = soa_categorie + soa_classifiche
# creating object of the class
obj_list = []
for label in label_list:
    new_obj = DistributionAutomaton(label)
    obj_list.append(new_obj)
'''
for obj in obj_list:
    print(obj.get_label())
    print(obj.read_decision())
'''

