import sys

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.edges = []
        self.num_vert = 0
    
    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vert = self.num_vert + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, dist):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], dist)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], dist)
        self.edges.append([self.get_vertex(frm), self.get_vertex(to), dist])

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.distance = sys.maxsize
        self.visited = False
        self.previous = None

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, dist):
        self.adjacent[neighbor] = dist
    
    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def get_edge_dist(self, neighbor):
        return self.adjacent[neighbor]

def get_min_distance_vertex(graph):
        min = sys.maxsize
        for v in graph:
            if v.get_distance() < min:
                min = v.get_distance()
                min_dist_vert = v
        return min_dist_vert

def dijkstra_alghorithm(graph, source, target):
    
    source.set_distance(0)

    queue = [v for v in graph]
    
    while len(queue):
        u = get_min_distance_vertex(queue)
        current = u
        current.set_visited()

        if u == target:
            path = [target.get_id()]
            while u.previous:
                path.append(u.previous.get_id())
                u = u.previous
            path.reverse()
            print("source: %s, target: %s, shortest distance: %s, shortest path: %s" %(source.get_id(), target.get_id(), target.get_distance(), path))
            break
        else:
            for next in current.adjacent:
                if next.visited:
                    continue
                new_dist = current.get_distance() + current.get_edge_dist(next)

                if new_dist < next.get_distance():
                    next.set_distance(new_dist)
                    next.set_previous(current)
        
            queue = [v for v in graph if not v.visited]
        
def ford_algorithm(graph, source, target):
    source.set_distance(0)
    for _ in range(len(graph.vert_dict) - 1):
        for u, v, w in graph.edges:
            new_dist = u.get_distance() + w
            if new_dist < v.get_distance():
                v.set_distance(u.get_distance() + w)
                v.set_previous(u)
    for u, v, w in graph.edges:
        new_dist = u.get_distance() + w
        if new_dist < v.get_distance():
            print("error: Graph contains a negative-weight cycle")
    
    path = [target.get_id()]
    u = target
    while u.previous:
        path.append(u.previous.get_id())
        u = u.previous
    path.reverse()        
    print("source: %s, target: %s, shortest distance: %s, shortest path: %s" %(source.get_id(), target.get_id(), target.get_distance(), path))

#Graph for Dijkstra's algorithm
dijk_g = Graph()
dijk_g.add_edge("a","b",2)
dijk_g.add_edge("a","c",1)
dijk_g.add_edge("a","d",1)
dijk_g.add_edge("b","c",3)
dijk_g.add_edge("b","d",4)
dijk_g.add_edge("b","e",7)
dijk_g.add_edge("c","f",6)
dijk_g.add_edge("c","g",3)
dijk_g.add_edge("e","f",12)
dijk_g.add_edge("f","g",1)
dijk_g.add_edge("f","j",4)
dijk_g.add_edge("g","h",1)
dijk_g.add_edge("g","i",5)
dijk_g.add_edge("h","i",1)
dijk_g.add_edge("i","j",8)

#Graph for Bellman-Ford's algorithm. It also contains negative edge weights.
ford_g = Graph()
ford_g.add_edge("a","b",2)
ford_g.add_edge("a","b",-1)
ford_g.add_edge("a","c",1)
ford_g.add_edge("a","d",1)
ford_g.add_edge("b","c",3)
ford_g.add_edge("b","c",-1)
ford_g.add_edge("b","d",4)
ford_g.add_edge("b","e",7)
ford_g.add_edge("c","f",6)
ford_g.add_edge("c","g",3)
ford_g.add_edge("e","f",12)
ford_g.add_edge("e","f",-3)
ford_g.add_edge("f","g",1)
ford_g.add_edge("f","j",4)
ford_g.add_edge("g","h",1)
ford_g.add_edge("g","i",5)
ford_g.add_edge("g","i",-2)
ford_g.add_edge("h","i",1)
ford_g.add_edge("i","j",8)
ford_g.add_edge("i","j",-2)

dijkstra_alghorithm(dijk_g, dijk_g.get_vertex("a"), dijk_g.get_vertex("j"))
ford_algorithm(ford_g, ford_g.get_vertex("a"), ford_g.get_vertex("j"))