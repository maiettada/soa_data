import sys, os


def sort_list(lis):
    lis.sort(key=lambda x: x[0])


def prendo_frase_fino_a(document, char_index):
    """
    This function selects a sub-text. Actually it splits a document into a selected part and a remaining part.

    :param document: text
    :param char_index: integer
    :return: [selection, remaining], where selection is the part of the document up to char_index
    for iteration purposes, the remaining part of the document is given.
    """
    selection = ""
    remaining = ""
    if char_index == -1:
        selection = document
        remaining = None
    else:
        selection = document[:char_index]
        remaining = document[char_index + 2:]
    return [selection, remaining]


def prendo_labels_fino_a(labels_list, char_index):
    """
    This function uses a labels_list; it retrieves the labels that span up to char_index

    :param labels_list: list of the labels related to the document txt
    :param char_index: integer
    :return: [selection, remaining], where selection is actually the list of labels that span until the char_index;
    for iteration purposes, the remaining list of labels is given
    """
    selection = []
    remaining = []
    if char_index == -1:
        selection = labels_list
        remaining = None
    else:
        selection = [[st, end, word] for [st, end, word] in labels_list if end <= char_index]
        # the following labels must be indexed starting from the new sentence.
        # Starting Point and Ending Point of a label: must be decreased by (char_index+2)
        remaining = [[st - char_index - 2, end - char_index - 2, word] for [st, end, word] in labels_list if
                     end > char_index]
    return [selection, remaining]


# Disable
def block_print():
    sys.stdout = open(os.devnull, 'w')


# Restore
def enable_print():
    sys.stdout = sys.__stdout__


def period_sect(labels_list, txt, labels_txt_list):
    """
    This function divides a big [txt, labels_list] data structure in
    a proper list [[sentence1,labels_list1],...,[sentence_n,labels_list_n]]

    :param labels_list: list of the labels related to the document txt
    :param txt: document
    :return: [ending_condition, list, txt], where ending_condition is actually the char index;
    the document was completely sectioned if ending_condition = -1
    """
    block_print()
    x = txt.find(". ")
    sublist = []
    [frase, txt] = prendo_frase_fino_a(txt, x) #separator len
    print(frase,"||,", txt)
    [sublist, labels_list] = prendo_labels_fino_a(labels_list, x)
    print(sublist,"||,", labels_list)
    print()
    labels_txt_list.append([frase, sublist])
    enable_print()
    return x, labels_list, txt


def main():
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
    return


if __name__ == "__main__":
    main()
