#!/usr/bin/env python3
"""
__authors__    = ["Blaze Sanders"]
__contact__    = "blaze.d.a.sanders@gmail.com"
__copyright__  = "Copyright 2023"
__license__    = "GPLv3"
__status__     = "Development
__deprecated__ = False
__version__    = "0.0.1"
__doc__        = "Generate a tab based GUI to control LiteHouse and Lustron house styles"
"""
# https://www.analyticsvidhya.com/blog/2023/05/elevate-your-python-apps-with-nicegui-the-ultimate-gui-framework/

# Disable PyLint linting messages
# https://pypi.org/project/pylint/
# pylint: disable=invalid-name
import re

import GlobalConstants as GC
currentNetworkDiagram = ''''''

# https://mermaid.js.org
STATIC_DEFAULT_NETWORK = '''
                graph LR;
                    A[UniFi PoE Switch] --> B[ROOM: Master Bedroom];
                    A[UniFi PoE Switch] --> F[ZimaBoard Server];
                    F[CPU: ZimaBoard Server] --> E[DISPLAY: Main Central Control];
                    B[ROOM: Master Bedroom] --> C[LIGHT: Master Bedroom]; 
                    B[ROOM: Master Bedroom] --> D[DISPLAY: Master Bedroom];
                    A[UniFi PoE Switch] --> LIGHT-Kitcen;
                    
                    style A color:#000000, fill:#03C04A, stroke:#000000;
                    style B color:#000000, fill:#03COFF, stroke:#000000;
                    style C color:#000000, fill:#FFC04A, stroke:#000000;
                    style D color:#FFFFFF, fill:#1F1F1F, stroke:#000000;
                    style E color:#FFFFFF, fill:#1F1F1F, stroke:#000000;
                    style F color:#000000, fill:#B8191D, stroke:#000000;
                '''

def parse_network_diagram(inputData: str) -> list:
    return inputData.split(';')

def edit_network_diagram_style(input: list, styleName: str, newColor: str, newFill: str, newStroke:str) -> list:
    styleIndex = -1
    for row in input:
        if styleName in row:
            styleIndex = input.index(row)
            input[styleIndex] = re.sub(r'color:#\w{6}', newColor, row)
            newRow = input[styleIndex]
            input[styleIndex] = re.sub(r'fill:#\w{6}', newFill, newRow)
            newRow = input[styleIndex]
            input[styleIndex] = re.sub(r'stroke:#\w{6}', newStroke, newRow)

    if styleIndex == -1:
        print(styleName +' not found')

    return input

def delete_network_diagram_node(input: list, nodeName: str) -> list:
    foundIndexes = []
    # Nodes are defined uniquely as X[ in the mermaid data structure, so '[' is add to node variable to enable substring search in list comprehension
    node = nodeName + '[' 
    for row in input:
        if node in row:
            nodeIndex = input.index(row)
            foundIndexes.append(nodeIndex)

    for i in reversed(foundIndexes):
        input.pop(i)
    
    outputList = delete_network_diagram_style(input, nodeName)
    
    return outputList

def delete_network_diagram_style(input: list, styleName: str) -> list:
    for row in input:
        if styleName in row:
            styleIndex = input.index(row)
            input.pop(styleIndex)
    
    return input

def output_network_diagram(input:list) -> str:
    newNetworkDiagram = ''''''
    for row in input:
        newNetworkDiagram = newNetworkDiagram + row

    return newNetworkDiagram

def csv_to_List(col, csv_file=GC.MAC_HOME_DIRECTORY+'TODO.csv'):
    result = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            result.append(row[col])  # Append only the first column
    return result

if __name__ == "__main__":
    networkList = parse_network_diagram(STATIC_DEFAULT_NETWORK)
    #print(networkList)

    newNetworkList = edit_network_diagram_style(networkList, 'style B', 'color:#FFFFFF', 'fill:#F0F0F0', 'stroke:#0F0F00')
    #print(newNetworkDiagram)
    
    newNetworkList = delete_network_diagram_node(newNetworkList, 'D')
    #print(newNetworkDiagram)
    
    newNetworkDiagram = output_network_diagram(newNetworkList)
    print(newNetworkDiagram)