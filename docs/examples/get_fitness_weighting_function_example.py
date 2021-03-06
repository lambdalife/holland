from holland.utils import select_random


weighting_function = get_some_weighting_function()

breeding_pool = select_breeding_pool(fitness_results, **selection_strategy.get("pool"))
# split fitness and genomes into separate lists
fitness_scores, genomes = zip(*breeding_pool)

weighted_scores = [weighting_function(fitness) for fitness in fitness_scores]
weighted_total = sum(weighted_scores)
selection_probabilities = [weighted_score / weighted_total for weighted_score in weighted_scores]

parents = select_random(genomes, probabilities=selection_probabilities, n=2)
