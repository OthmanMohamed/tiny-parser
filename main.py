import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget, QMessageBox
from scanner import Scanner
from parser import Parser
import networkx as nx
from tkinter import filedialog
import matplotlib.pyplot as plt


class ParserWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl = QLabel('Enter Tiny Code', self)
        self.input_code = QTextEdit()
        self.add_initial_code()
        submit_button = QPushButton('Parse')
        submit_button.clicked.connect(self.submitted)
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(lbl, 1, 0)
        grid.addWidget(self.input_code, 1, 1)
        grid.addWidget(submit_button, 2, 1)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Tiny Parser')
        self.error = QMessageBox()
        self.error.setIcon(QMessageBox.Critical)
        self.show()
        

    def add_initial_code(self):
        self.input_code.append("{ sample code for testing }")
        self.input_code.append("read x;")
        self.input_code.append("sum:=0;")
        self.input_code.append("if 0<x then")
        self.input_code.append("    repeat")
        self.input_code.append("        sum:=sum+x;")
        self.input_code.append("        x:=x - 1;")
        self.input_code.append("    until x=0;")
        self.input_code.append("    write x;")
        self.input_code.append("else")
        self.input_code.append("    write error;")
        self.input_code.append("end")

    def draw(self):
        plt.clf()
        pos = nx.nx_pydot.graphviz_layout(self.graph,prog='dot')
        labels = dict((n, d['value']) for n, d in self.graph.nodes(data=True))
        nx.draw(self.graph, pos, labels=labels, with_labels=True, arrows=False, node_size=400,node_color='y')
        plt.title('Parse Tree')
        plt.show()

    def submitted(self):
        try:
            scanner = Scanner(self.input_code.toPlainText())
            types,values = scanner.tokenize()
            parser = Parser()
            parser.set_types_and_values(types, values)
            nodes_list,edges_list = parser.run()
            self.graph = nx.DiGraph()
            for node_number, node_value in nodes_list.items():
                self.graph.add_node(node_number, value=node_value)
            self.graph.add_edges_from(edges_list)
            parser.clear_tables()
            self.draw()
        except (ValueError, SyntaxError) as error:
            self.showError(error)

    def showError(self, error):
        error_type = 'Error'
        if isinstance(error,ValueError):
            error_type = 'ValueError'
            message = f"Value {error} raises an error" 
        elif isinstance(error,SyntaxError):
            error_type = 'SyntaxError'
            message = f"Invalid syntax at {error}"
        self.error.setWindowTitle(error_type)
        self.error.setText(message)
        self.error.exec_()
        
app = QApplication(sys.argv)
w = ParserWidget()
sys.exit(app.exec_())
