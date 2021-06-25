class labelledObj:

    # default constructor
    def __init__(self, label=""):
        self.label = str(label)
        self.list = [1,2,3]

    # a method for printing data members
    def print_label(self):
        print(self.label)

    def print_list(self):
        print(self.list)


# creating object of the class
obj_list = [ labelledObj(" tizio"), labelledObj(" caio"), labelledObj(" sempronio")]
for obj in obj_list:
    obj.print_label()
    obj.print_list()


def sort_list(lis):
 lis.sort(key=lambda x:x[0])

def prendo_frase_fino_a(document, char_index):
    selection = ""
    remaining = ""
    if char_index == -1:
        selection = document
        remaining = None
    else:
        selection = document[:char_index]
        remaining = document[char_index+2:]
    return [selection, remaining]

def prendo_labels_fino_a(json_list, char_index):
    selection = []
    remaining = []
    if char_index == -1:
        selection = json_list
        remaining = None
    else:
        selection = [ [st,end,word] for [st,end,word] in json_list if end <= char_index ]
        remaining = [ [st - char_index - 2,end - char_index - 2,word] for [st,end,word] in json_list if end > char_index ]
    return [selection, remaining]

def recursive_select(json_list, txt):
    # = int(input('Enter a number: '))
    sort_list(json_list)
    x = txt.find(".")
    json_sublist = []
    [ frase, documento ] = prendo_frase_fino_a( txt, x )
    [json_sublist, json_list] = prendo_labels_fino_a(json_list, x)
    '''print(x) #char index
    print(frase)
    print(json_sublist)
    print(documento)
    print(json_list)'''
    if x !=-1:
        a.append([frase, json_sublist])
        recursive_select(json_list, documento)
    return

a=[]
txt = "Hello. Welcome. Sit down. "
json_list = [[0,5,"p1"],[7,14,"p2"],[16,19,"p3w1"],[20,24,"p3w2"]]
recursive_select(json_list, txt)
print("-----")
print(a)

listatizio = []
listacaio = []
listasempronio = []
mappa = [("tizio", listatizio),("caio", listacaio),("sempronio", listasempronio)]