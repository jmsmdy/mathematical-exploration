import copy

def is_equal(oriented_simplex_A, oriented_simplex_B):
    A = list(oriented_simplex_A)
    B = list(oriented_simplex_B)
    if set(A) != set(B):
        return False
    if len(A) == 0:
        return True
    for i in range(len(B)):
        if B[i] == A[0]:
            k = i
            break
    if k == 0:
        return is_equal(tuple(A[1:]), tuple(B[1:]))
    else:
        B[i] = B[0]
        return is_equal(tuple(A[1:]), tuple(B[1:]))
    
def are_equal(set_A, set_B):
    A = list(set_A)
    B = list(set_B)
    if len(A) != len(B):
        return False
    for a in A:
        a_is_in_B = False
        for b in B:
            if is_equal(a,b):
                a_is_in_B = True
        if not a_is_in_B:
            return False
    return True

class oriented_simplex_complex:
    def __init__(self, data):
        if not type(data) is dict:
            raise ValueError('Data must be given as a dictionary.')
        self.dimension = len(data) - 1
        
        if 'vertices' not in data.keys():
            raise ValueError('Missing "vertices" key.')
        if not type(data['vertices']) is set:
            raise ValueError('Vertices must be given as a set of strings.')
        for vertex in data['vertices']:
            if not type(vertex) is str:
                raise ValueError('Vertices must be strings.')
        self.vertices = copy.deepcopy(data['vertices'])
        
        self.simplices = {}
        for i in range(1, self.dimension + 1):
            if f'{i}-simplices' not in data.keys():
                raise ValueError(f'Missing "{i}-simplices" key.')
            if not type(data[f'{i}-simplices']) is set:
                raise ValueError(f'{i} simplices must be given as a set of {i+1}-tuples.')
            for simplex in data[f'{i}-simplices']:
                if (not type(simplex) is tuple) or (len(simplex) != i+1):
                    raise ValueError(f'Directed edges must be {i+1}-tuples')
                for j in range(i+1):
                    if simplex[j] not in self.vertices:
                        raise ValueError('Unknown vertex.')
            self.simplices[i] = copy.deepcopy(data[f'{i}-simplices'])
            
    def is_automorphism(self, f):   
        try:
            forward_dict = {v : f(v) for v in self.vertices}
            inverse_dict = {f(v) : v for v in self.vertices if f(v) in self.vertices}
        except:
            print('Not a valid function on vertices.')
            return False
        if len(forward_dict) != len(inverse_dict):
            print('Not a valid bijection on vertices')
            return False
        pullback_simplices = {}
        for i in range(1, self.dimension+1):
            pullback_simplices[i] = {tuple([inverse_dict[v] for v in simplex]) for simplex in self.simplices[i]}
            if not are_equal(pullback_simplices[i], self.simplices[i]):
                return False
        return True

class digraph:
    def __init__(self, vertices, directed_edges):
        if not (type(vertices) is list):
            raise ValueError('Vertices must be ghiven as a list of strings.')
        for vertex in vertices:
            if not (type(vertex) is str):
                raise ValueError('Vertices must be strings.')
        self.vertices = copy.deepcopy(vertices)
        
        if not (type(directed_edges) is list):
            raise ValueError('Directed edges must be given as a list of pairs.')
        for edge in directed_edges:
            if (not (type(edge) is tuple)) or (len(edge) != 2):
                raise ValueError('Directed edges must be pairs')
            if (edge[0] not in self.vertices) or (edge[1] not in self.vertices):
                raise ValueError('Unknown vertex.')
        self.edges = copy.deepcopy(directed_edges)
        
    def is_automorphism(self, f):   
        try:
            forward_dict = {v : f(v) for v in self.vertices}
            inverse_dict = {f(v) : v for v in self.vertices if f(v) in self.vertices}
        except:
            print('Not a valid function on vertices.')
            return False
        if len(forward_dict) != len(inverse_dict):
            print('Not a valid bijection on vertices')
            return False
        pullback_edges = [(v, w) for v in vertices for w in vertices if (f(v), f(w)) in self.edges]
        if set(pullback_edges) == set(self.edges):
            return True
        else:
            return False