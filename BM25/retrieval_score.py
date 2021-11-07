import tqdm

def topk_experiment(result_retriever):
    result = 0.0
    #retriever.get_sparse_embedding()
    correct = 0
    for index in range(len(result_retriever)):
        if (
             result_retriever["original_context"][index]
             in result_retriever["context"][index]
        ):
            correct += 1
    result = correct / len(result_retriever)
    return result
