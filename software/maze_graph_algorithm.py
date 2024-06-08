import heapq

class PixelNode:
    def __init__(self, y = None, x = None, color = "black"):
        self.y = y
        self.x = x
        self.coordinates = [y, x]
        self.color = color
        self.d = float('inf')
        self.parent = None
        self.finished = False

    def set_color(self, color):
        self.color = color

    def __lt__(self, other):
        return (self.d < other.d)

class MazeGraph:
        def __init__(self, nodes = []):
            self.nodes = nodes
            self.adj_list = {}
            if self.nodes:
                for node in self.nodes:
                    self.adj_list[node] = []

        def add_node(self, node):
            self.nodes.append(node)
            self.adj_list[node] = []

        def add_edge(self,u,v):
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)

        def remove_edge(self,u,v):
            self.adj_list[u].remove(v)
            self.adj_list[v].remove(u)

        def print_adj_list(self):
            for node in self.nodes:
                print(node.coordinates, "-> ", end = "")
                for edge in self.adj_list[node]:
                    print(edge.coordinates, end = " ")
                print()

        def print_colors(self):
            for node in self.nodes:
                print(node.coordinates, "color is:", node.color)

        def print_distances(self):
            for node in self.nodes:
                print(node.coordinates, "distance is:", node.d)

def dijkstra(graph,source,end):
  solution_path = []
  solution_coordinates = []
  nodes={}
  for node in graph.nodes:
      nodes[node] = PixelNode()
  nodes[source].d = 0
  queue=[(0,source)]
  while queue:
      d,node=heapq.heappop(queue)
      if nodes[node].finished:
          continue
      nodes[node].finished=True
      for neighbor in graph.adj_list[node]:
          if neighbor.finished:
              continue
          new_d = d + 1
          if new_d < neighbor.d:
              neighbor.d = new_d
              neighbor.parent = node
              heapq.heappush(queue,(new_d,neighbor))  
  cur_node = end
  while cur_node != source:
      solution_path.append(cur_node)
      solution_coordinates.append((cur_node.y,cur_node.x))
      cur_node = cur_node.parent
  solution_path.append(cur_node)
  solution_coordinates.append((cur_node.y,cur_node.x))
  return solution_path, solution_coordinates

def print_dijkstra_solution(solution_path):
    for node in solution_path:
        if node == solution_path[-1]:
            print(node.coordinates)
        else:
            print(node.coordinates, "-> ", end = "")