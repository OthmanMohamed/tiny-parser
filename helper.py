class Node:
    def __init__(self,value):
        self.value =  value
        self.children = []
        self.index=None

    def __str__(self):
        s = f"{self.value}\n"
        for child in self.children:
            s+=f"{child.value}\n"
        return s

    def set_children(self,children):
        if children == None:
            return
        try:
            assert isinstance(children,list)
            for child in children:
                self.children.append(i)
        except AssertionError:
            self.children.append(children)

def find_indeces(list,value):
    indeces = []
    for i in range(len(list)):
        if list[i] == value:
            indeces.append(i)
    return indeces
