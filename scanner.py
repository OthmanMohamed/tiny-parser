class Scanner:
    def __init__(self,input_code):
        self.input_code = input_code


    def tokenize(self, toFile=False):
        import re
        groups = [
            r'(?P<comment>(?<={)[^{}]*(?=}))',
            r'(?P<reserved>if|then|else|end|repeat|until|read|write)',
            r'(?P<number>\-?[0-9]+)',
            r'(?P<symbol>[\+\-\*\/=\<();])',
            r'(?P<assign>:=)',
            r'(?P<identifier>[a-zA-Z]+)',
        ]
        tinyRegex = re.compile('|'.join(x for x in groups),re.IGNORECASE)
        types = []
        values = []

        for match in re.finditer(tinyRegex,self.input_code):
            token = f"{match.group(0).strip()}"
            values.append(token)
            if(match.lastgroup in ['identifier','number','comment']):
                types.append(match.lastgroup)
            else:
                types.append(token)

        if toFile:
            writer=open('tokens.txt','w')
            print(set(zip(values,types)), file=writer)
        self.types = types
        self.values = values
        return types,values
