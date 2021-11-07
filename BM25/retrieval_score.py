import tqdm

def topk_experiment(result_retrieval):
    result = 0.0
    #retrieval.get_sparse_embedding()
    correct = 0
    for index in range(len(result_retrieval)):
        if (
             result_retrieval["original_context"][index]
             in result_retrieval["context"][index]
        ):
            correct += 1
    result = correct / len(result_retrieval)
    return result
