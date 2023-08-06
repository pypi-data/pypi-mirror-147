from gensim.models import Word2Vec

def word2VecEmbedding(sentences, embed_size=128, window_size=5, workers=3, iter=5, **kwargs):
        print("running word2Vec embedding...")
        kwargs["sentences"] = sentences
        kwargs["min_count"] = kwargs.get("min_count", 0)
        kwargs["size"] = embed_size
        kwargs["sg"] = 1
        kwargs["hs"] = 1
        kwargs["workers"] = workers
        kwargs["window"] = window_size
        kwargs["iter"] = iter

        model = Word2Vec(**kwargs)

        return model