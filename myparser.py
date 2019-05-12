from helper import Node,find_indeces

class myParser:
    iterator=0

    def __init__(self):
        self.types = []
        self.values = []
        self.iterator = 0
        self.parse_tree=None
        self.nodes_table={}
        self.edges_table=[]

    def set_types_and_values(self,types,values):
        comment_idx = find_indeces(types,'comment')
        for i in comment_idx:
            del values[i]
            del types[i]
        self.values = values
        self.types = types
        self.iterator = 0
        self.token = self.types[self.iterator]

    def next_token(self):
        if(self.iterator==len(self.types)-1):
            return False
        self.iterator += 1
        self.token=self.types[self.iterator]
        return True

    def match(self,token):
        if self.token==token:
            if not self.next_token():
                return False
            return True
        else:
            self.clear_tables()
            raise SyntaxError(self.token)

    def stmt_sequence(self):
        start_node = Node('   ')
        start_node.set_children(self.statement())
        end_if = self.types[self.iterator-1] == 'end'
        while self.token==';' or end_if:
            if not end_if:
                if not self.match(';'):
                    break
            next_node=self.statement()
            if next_node == None:
                break
            else:
                start_node.set_children(next_node)
            end_if = self.types[self.iterator-1] == 'end'
        return start_node

    def statement(self):
        if self.token=='if':
            if_tree=self.if_stmt()
            return if_tree
        elif self.token=='repeat':
            repeat_tree=self.repeat_stmt()
            return repeat_tree
        elif self.token=='identifier':
            assign_tree=self.assign_stmt()
            return assign_tree
        elif self.token=='read':
            read_tree=self.read_stmt()
            return read_tree
        elif self.token=='write':
            write_tree=self.write_stmt()
            return write_tree
        elif self.token in ['end','until','else','comment']:
            return None
        else:
            self.clear_tables()
            raise SyntaxError(self.token)

    def if_stmt(self):
        if_node=Node(self.values[self.iterator])
        if self.token=='if':
            self.match('if')
            exp_node = Node('   ')
            exp_node.set_children(self.exp())
            if_node.set_children(exp_node)
            self.match('then')
            then_node = Node('then')
            then_node.set_children(self.stmt_sequence())
            if_node.set_children(then_node)
            if self.token=='else':
                self.match('else')
                else_node = Node('else')
                else_node.set_children(self.stmt_sequence())
                if_node.set_children(else_node)
            self.match('end')
        return if_node

    def exp(self):
        left_node=self.simple_exp()
        if self.token=='<' or self.token=='>' or self.token=='=':
            op_node=Node(self.values[self.iterator])
            self.comparison_op()
            op_node.set_children(left_node)
            op_node.set_children(self.simple_exp())
            left_node = op_node
        return left_node

    def comparison_op(self):
        if self.token == '<':
            self.match('<')
        elif self.token == '>':
            self.match('>')
        elif self.token == '=':
            self.match('=')

    def simple_exp(self):
        left_node=self.term()
        while self.token=='+' or self.token=='-':
            op_node = Node(self.values[self.iterator])
            self.addop()
            op_node.set_children(left_node)
            op_node.set_children(self.term())
            left_node = op_node
        return left_node

    def addop(self):
        if self.token=='+':
            self.match('+')
        elif self.token=='-':
            self.match('-')

    def term(self):
        right_node = self.factor()
        while self.token=='*' or self.token=='/':
            op_node = Node(self.values[self.iterator])
            self.mulop()
            op_node.set_children(right_node)
            right_node = op_node
            right_node.set_children(self.factor())
        return right_node

    def mulop(self):
        if self.token=='*':
            self.match('*')
        elif self.token=='/':
            self.match('/')

    def factor(self):
        if self.token=='(':
            self.match('(')
            node = self.exp()
            self.match(')')
        elif self.token=='number':
            node = Node(self.values[self.iterator])
            self.match('number')
        elif self.token=='identifier':
            node = Node(self.values[self.iterator])
            self.match('identifier')
        else:
            self.clear_tables()
            raise ValueError(self.token)
            return None
        return node

    def repeat_stmt(self):
        repeat_node=Node(self.values[self.iterator])
        if self.token=='repeat':
            self.match('repeat')
            repeat_node.set_children(self.stmt_sequence())
            self.match('until')
            #until_node = Node('until')
            #until_node.set_children(self.exp())
            repeat_node.set_children(self.exp())
        return repeat_node

    def assign_stmt(self):
        node = Node(self.values[self.iterator])
        #node.set_children(Node(self.values[self.iterator]))
        self.match('identifier')
        self.match(':=')
        node.set_children(self.exp())
        return node

    def read_stmt(self):
        node=Node(self.values[self.iterator])
        self.match('read')
        node.set_children(Node(self.values[self.iterator]))
        self.match('identifier')
        return node

    def write_stmt(self):
        node=Node(self.values[self.iterator])
        self.match('write')
        node.set_children(self.exp())
        return node

    def create_nodes_table(self,node=None):
        if node == None:
            node = self.parse_tree
        node.index=myParser.iterator
        self.nodes_table.update({myParser.iterator:node.value})
        myParser.iterator += 1
        for child in node.children:
            self.create_nodes_table(child)

    def create_edges_table(self,node=None):
        if node == None:
            node = self.parse_tree
        for child in node.children:
            self.edges_table.append((node.index,child.index))
        for child in node.children:
            self.create_edges_table(child)


    def run(self):
        self.parse_tree=self.stmt_sequence()    #create parse tree
        self.create_nodes_table()               #create nodes_table
        self.create_edges_table()               #create edges_table
        if  self.iterator==len(self.types)-1:
            print('success')
            return self.nodes_table, self.edges_table
        elif self.iterator<len(self.types):
            self.clear_tables()
            raise SyntaxError(self.token)

    def clear_tables(self):
        self.nodes_table.clear()
        self.edges_table.clear()
        self.parse_tree = None
        myParser.iterator = 0
