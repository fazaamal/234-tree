import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Node:
    """
    Constructor used to declare node properties, such as children, parent and keys
    """
    def __init__(self, values=None):
        self.children = []
        self.parent = None

        if(values == None):
            self.keys = []
        else:
            self.keys = values
    
    #Returns type of node (2, 3 or 4 node)
    def nodeType(self):
        return len(self.keys)+1
    
    #Returns child at specified index number, if no children return None
    def getChild(self, index):
        if(index > len(self.children)-1):
            return None
        else:
            return self.children[index]

    #Returns key value at specified index, if the index is more than number of keys then return None
    def getKey(self, index):
        if(index > len(self.keys)-1):
            return None
        else:
            return self.keys[index]

    #Set child of node at specified index number
    def setChild(self, index, value):
        self.children[index] = value

    #Set key of node at specified index number
    def setKey(self, index, value):
        self.keys[index] = value

    #Get root of current node, searches upwards from the node until it reaches a node with no parent
    def getRoot(self):
        currNode = self
        while(currNode.parent != None):
            currNode = currNode.parent
        
        return currNode

def balance(node: Node, middleKey = None):
    """
    Balance overflowing nodes from bottom to top
    """
    if(len(node.keys) > 3):
        parentMiddleKey = None

        #Create new left and right nodes, splitting apart the current node's keys 
        leftSide = Node(node.keys[0:node.keys.index(middleKey)])
        rightSide = Node(node.keys[node.keys.index(middleKey)+1:])

        if(node.parent != None): 
            #If the node has a parent then the middle key will be added to the parent node, 
            #and current node removed as a child and the new left and right nodes are added as children
            if(len(node.parent.keys) >= 2):
                parentMiddleKey = node.parent.keys[1]

            node.parent.children.remove(node)
            node.parent.keys.append(middleKey)
            node.parent.children.append(leftSide)
            node.parent.children.append(rightSide)
            node.parent.keys.sort()
            node.parent.children.sort(key=lambda x: x.keys[0]) #Sorts chilren based on first number in the list 
        else:
            #If the current node is the root then a new root is created with the middle key from the 5 node as the key
            #New left and right sides added as children
            newRoot = Node([middleKey])
            node.parent = newRoot
            newRoot.children.append(leftSide)
            newRoot.children.append(rightSide)

        #Set the parent of the current node as the parents of the new left and right nodes
        leftSide.parent = node.parent
        rightSide.parent = node.parent

        if(len(node.children) > 0):
            #If the node has children then the new left and right nodes have the old 5 node's children added
            #and 5 node's children have the new left and right nodes set as their parents
            leftSide.children = node.children[0:2]
            rightSide.children = node.children[2:]

            for child in node.children[0:2]:
                child.parent = leftSide
            
            for child in node.children[2:]:
                child.parent = rightSide

        if(len(node.parent.keys) > 3):
            #If the parent has more than 3 keys after balancing current node then the balance function is called on the parent
            balance(node.parent, parentMiddleKey)
        
        return node.getRoot()
    else:
        return node.getRoot()

def insert(node: Node, value: (int | float)):
    """
    Insert value into tree starting from the root from top to bottom.
    If current node not at bottom level (i.e. has children) recursion of insert() will occur until reached bottom level.
    It returns latest root of tree, in case new root was created when balancing the tree.
    """
    if(len(node.children) == 0):
        if(len(node.keys) < 3):
            node.keys.append(value)
            node.keys.sort()
        elif(len(node.keys) == 3):
            middleKey = node.keys[1]

            node.keys.append(value)
            node.keys.sort()

            return balance(node, middleKey)
    else:
        for i in range(len(node.keys)):
            #If index is at first key and value is less than the first key then call insert() value on first child node
            if(i==0 and value < node.keys[0]):
                insert(node.children[0], value)
                break
            #If index is at last key of node, then call insert() value on last child node
            elif(i==len(node.keys)-1):
                insert(node.children[i+1], value)
                break

            else:
                if(value > node.keys[i] and value < node.keys[i+1]):
                    insert(node.children[i+1], value)
                    break
    
    return node.getRoot()

def search(node: Node, value:(int|float)):
    """
    Recursive function to search whether value is inside tree or not. Returns True if included, False if otherwise
    """
    #If the value is inside the keys of the current node then return True, if not check the children
    if(value in node.keys):
        return True
    else:
        if(len(node.children) == 0):
            return False
        else:
            for i in range(len(node.keys)):
                #If index is at first key and value is less than the first key then traverse to first child and check value inside that child
                if(i==0 and value < node.keys[0]):
                    return search(node.children[0], value)
                #If index is at last key of node, then search for value in the last child 
                elif(i==len(node.keys)-1):
                    return search(node.children[i+1], value)
                #If not at first or last key, check if value is greater than current key and less than the next key, if so search for value in the child between the 2 keys
                else:
                    if(value > node.keys[i] and value < node.keys[i+1]):
                        return search(node.children[i+1], value)
                        

def printTree(root: Node):
    """
    Uses BFS traversal to get all children of current node level to print out to terminal
    """
    currNode = root
    queue = []
    print(currNode.keys)
    for child in currNode.children:
        queue.append(child)

    while(len(queue) > 0):
        children = []
        currentLevel = []
        for node in queue:
            print(node.keys, end=' ')
            for child in node.children:
                children.append(child)
            currentLevel.append(node)

        for child in children:
            queue.append(child)
        
        for node in currentLevel:
            queue.remove(node)

        print('')

if __name__ == "__main__":
    values = [2, 13, 7, 16, 19, 9, 22, 10, 14, 17]
    root = Node([values[0]])

    for value in values[1:]:
        print(bcolors.OKBLUE+'Inserting ' + str(value) + bcolors.ENDC)
        root = insert(root, value)
        printTree(root)

    includedValues = [2, 13, 7, 16, 19, 9, 22, 10, 14, 17]
    excludedValues = [100, 1, 0, 8, 29, 40, 21, 15]
    print(bcolors.OKGREEN+'Searching for values added to tree'+bcolors.ENDC)
    for value in includedValues:
        print(str(value)+ ' included in tree? ' + str(search(root, value)))
    
    print(bcolors.OKGREEN+'Searching for values not inserted to tree'+bcolors.ENDC)
    for value in excludedValues:
        print(str(value)+ ' included in tree? ' + str(search(root, value)))