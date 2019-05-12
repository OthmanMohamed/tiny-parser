import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, QTextEdit, QWidget, QMessageBox
from scanner import Scanner
from myparser import myParser
import networkx as nx
from tkinter import filedialog
import matplotlib.pyplot as plt


class ParserW(QWidget):
    def __init__(self):
        super().__init__()
        self.myStart()


    def draw(self):
        plt.clf()
        pos = nx.nx_pydot.graphviz_layout(self.graph,prog='dot')
        labels = dict((n, d['value']) for n, d in self.graph.nodes(data=True))
        nx.draw(self.graph, pos, labels=labels, with_labels=True, arrows=False, node_size=300,node_color='w')
        plt.title('Parse Tree')
        plt.show()

    def myStart(self):
        try:
            with open('input.txt', 'r') as myfile:
                data = myfile.read()
            scanner = Scanner(data)
            types,values = scanner.tokenize()
            parser = myParser()
            parser.set_types_and_values(types, values)
            nodes_list,edges_list = parser.run()
            self.graph = nx.DiGraph()
            for node_number, node_value in nodes_list.items():
                self.graph.add_node(node_number, value=node_value)
            self.graph.add_edges_from(edges_list)
            parser.clear_tables()
            self.draw()
        except (ValueError, SyntaxError) as error:
            error_type = 'Error'
            if isinstance(error,ValueError):
                error_type = 'ValueError'
                print(f"Value {error} raises an error")
            elif isinstance(error,SyntaxError):
                error_type = 'SyntaxError'
                print(f"Invalid syntax at {error}")


print ("welcome")
app = QApplication(sys.argv)
w = ParserW()
