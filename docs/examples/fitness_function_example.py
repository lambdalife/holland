def fitness_function(genome):
    """Evaluates an ImageClassifier instance (that uses a neural network with weight vectors w1 and w2)"""
    individual = ImageClassifier(w1=genome["w1"], w2=genome["w2"])
    fitness = 0

    for label, image in labeled_images:
        classification = ImageClassifier.classify(image)
        if classification == label:
            fitness += 100

    return fitness
