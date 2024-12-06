from lxml import etree
from collections import OrderedDict

class GMLGraph:
    def __init__(self, file_path, cache_size=100):
        self.file_path = file_path
        self.cache_size = cache_size
        self.vertex_cache = OrderedDict()
        self.neighbor_cache = OrderedDict()

    def _add_to_cache(self, cache, key, value):
        if key in cache:
            cache.move_to_end(key)
        cache[key] = value
        if len(cache) > self.cache_size:
            cache.popitem(last=False)

    def get_vertices(self):
        if 'vertices' in self.vertex_cache:
            return self.vertex_cache['vertices']
        
        vertices = set()
        context = etree.iterparse(self.file_path, tag='node', huge_tree=True, recover=True)
        for _, elem in context:
            vertex_id = int(elem.findtext('id'))
            vertices.add(vertex_id)
            elem.clear()
        
        self._add_to_cache(self.vertex_cache, 'vertices', vertices)
        return vertices

    def get_vertex_count(self):
        if 'vertex_count' in self.vertex_cache:
            return self.vertex_cache['vertex_count']
        
        count = 0
        context = etree.iterparse(self.file_path, tag='node', huge_tree=True, recover=True)
        for _, elem in context:
            count += 1
            elem.clear()
        
        self._add_to_cache(self.vertex_cache, 'vertex_count', count)
        return count

    def get_neighbors(self, vertex_id):
        if vertex_id in self.neighbor_cache:
            return self.neighbor_cache[vertex_id]

        neighbors = set()
        context = etree.iterparse(self.file_path, tag='edge', huge_tree=True, recover=True)
        for _, elem in context:
            source = int(elem.findtext('source'))
            target = int(elem.findtext('target'))
            if source == vertex_id:
                neighbors.add(target)
            elif target == vertex_id:
                neighbors.add(source)
            elem.clear()
        
        self._add_to_cache(self.neighbor_cache, vertex_id, neighbors)
        return neighbors

    def get_edges_of_vertex(self, vertex_id):
        if vertex_id in self.vertex_cache:
            return self.vertex_cache[vertex_id]

        edges = []
        context = etree.iterparse(self.file_path, tag='edge', huge_tree=True, recover=True)
        for _, elem in context:
            source = int(elem.findtext('source'))
            target = int(elem.findtext('target'))
            if source == vertex_id or target == vertex_id:
                edges.append((source, target))
            elem.clear()
        
        self._add_to_cache(self.vertex_cache, vertex_id, edges)
        return edges

    def clear_cache(self):
        self.vertex_cache.clear()
        self.neighbor_cache.clear()
    
    def subgraph(self, vertices):
        pass