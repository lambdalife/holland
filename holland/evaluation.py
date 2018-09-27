def run_evaluation(evaluate, gene_pool):
    results = []
    for genome in gene_pool:
        score = evaluate(genome)
        results.append((score, genome))
    return results
