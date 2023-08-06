from .embedding_algorithm import Embedding
from walks.factory import walker
from .word2Vec import word2VecEmbedding
from utils import adj_list_reader
from utils import export_pickel

class DeepWalk(Embedding):

    def __init__(self, args):
        self.embedding = None;
        self.walk_len = int(args.walk_len)
        self.walks = int(args.number_of_walks)
        self.dim = int(args.dimension)
        self.walker = args.walker
        self.adj_list = adj_list_reader(args.adj_list)
        self.set_embedding()

    def set_embedding(self):
        # perform walks
        walks = walker(self.adj_list, self.walks, self.walk_len, self.walker)
        
        # word2vec on generated walks
        self.embedding = word2VecEmbedding(walks, self.dim)

    def get_embedding(self):
        data = {}
        for node in self.adj_list:
            if node in self.embedding.wv:
                data[node] = self.embedding.wv[node]
        file_name = "deep_walk_" + str(self.dim) + "_" + self.walker + "_" + str(self.walks) + "_" + str(self.walk_len)
        export_pickel(data, file_name)

def deep_walk(args):
    print("running deep walk...")
    model = DeepWalk(args)
    print("exporting embedding...")
    model.get_embedding()
    return
