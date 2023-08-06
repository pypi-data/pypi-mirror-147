import importlib.machinery


def load_model(model_source_path: str):
    loader = importlib.machinery.SourceFileLoader("model_source", model_source_path)
    return loader.load_module("model_source")
