from nodes import Node, Leaf,splits,parent_splits,fusions,parent_fusions

class BPlusTree(object):
    """
    B+ tree object

    Nodes will be automatically split into two once they're full. When a split occurs
    a key will float upwards and be inserted into the parent node to act as a pivot.
    [a,b,c,d].split() -> Parent[c]
                         |      |
                        [a,b]   [d]
    Attributes:
        maximum (int): The maximum number of keys a node can hold before triggering split.
    """
    root: Node

    def __init__(self,maximum = 4):
        self.root = Leaf()
        self.maximum: int = maximum if maximum > 2 else 2
        self.minimum: int = self.maximum // 2
        self.depth = 0

    def find_end(self) -> Leaf:
        node = self.root
        while True:
            if type(node) is Leaf:
                return node
            else:
                node = node.values[-1]

    def find(self,key) -> Leaf:
        """
        find the leaf
        Returns:
            Leaf: the leaf which should have the key
        """
        node = self.root
        # traverse until the leaf node is reached
        while type(node) is not Leaf:
            node = node[key]

        return node

    def __getitem__(self, item):
        return self.find(item)[item]

    def query(self,key):
        """
        Returns the value for a given key or None if no such key exists
        """
        leaf = self.find(key)
        return leaf[key] if key in leaf.keys else None

    def range(self,start,end):
        start_node = self.find(start)
        end_node = self.find(end)

        current_node = start_node
        cursor = current_node.index(start)
        while  current_node != end_node.next:
            current_key = current_node.keys[cursor]
            cursor += 1

            if current_key >= end:
                break
            elif cursor >= len(current_node.keys):
                cursor = 0
                current_node = current_node.next

            yield current_key

    def cursor(self,start):
        end  = self.find_end().keys[-1]
        for k in self.range(start,end):
            yield k

    def __setitem__(self, key, value,leaf=None):
        """
        Inserts a key-value pair after traversing to a leaf node.
        If the node is full, splits the leaf into two
        """
        if leaf is None:
            leaf = self.find(key)
        leaf[key] = value
        if len(leaf.keys) > self.maximum:
            # NOTE: * is splat;used here to pass multiple returns of split to insert_index
            self.insert_index(*leaf.split())

    def insert(self,key,value):
        """
        Returns :
            (bool,Leaf): the leaf where the key is inserted. return False if the key already exists
        """
        leaf = self.find(key)
        if key in leaf.keys:
            return False,leaf
        else:
            self.__setitem__(key,value,leaf)
            return True,leaf

    def insert_index(self,key,values: list[Node]):
        """
        For a parent and child node,
        insert the values from the child onto the values of parent
        """
        parent = values[1].parent
        if parent is None:
            values[0].parent = values[1].parent = self.root = Node()
            self.depth += 1
            self.root.keys = [key]
            self.root.values = values
            return

        parent[key] = values
        # if node is full, split it
        # once the leaf node is split, it consists of an internal node and two leaf nodes
        # these need to be re-inserted back to the tree
        if len(parent.keys) > self.maximum:
            self.insert_index(*parent.split())


    def delete(self,key,node: Node = None):
        if node is None:
            node = self.find(key)
        del node[key]

        if len(node.keys) < self.minimum:
            if node == self.root:
                if len(self.root.keys) == 0 and len(self.root.values) > 0:
                    self.root = self.root.values[0]
                    self.root.parent = None
                    self.depth -= 1
                return
            elif not node.borrow_key(self.minimum):
                node.fusion()
                self.delete(key,node.parent)

    def show(self,node=None,file=None,_prefix="",_last=True):
        """Prints keys at each level"""
        if node is None:
            node = self.root
        print(_prefix,"`_ " if _last else "|- ", node.keys,sep="",file=file)
        _prefix += "   " if _last else "|  "

        if type(node) is Node:
            # recursively print the key of child nodes if exists
            for i, child in enumerate(node.values):
                _last = (i == len(node.values) - 1)
                self.show(child,file,_prefix,_last)

    def stats(self):
        return splits,parent_splits,fusions,parent_fusions,self.depth
