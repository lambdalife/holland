<h1 align='center'>Holland</h1>
<h2 align='center'>Genetic Algorithm Library for Python</h1>

> Computer programs that "evolve" in ways that resemble natural selection can solve complex problems even their creators do not fully understand



<div align='center'>
    <a href='https://pypi.org/project/holland/'><img src='https://img.shields.io/pypi/v/holland.svg' alt='PyPI'></img></a>
    <a href='https://travis-ci.com/lambdalife/holland'><img src='https://travis-ci.com/lambdalife/holland.svg?branch=master' alt='Build'></img></a>
	<a href='https://codecov.io/gh/lambdalife/holland'><img src='https://codecov.io/gh/lambdalife/holland/branch/master/graph/badge.svg' alt='Coverage'></img></a>
    <a href='https://hollandpy.readthedocs.io/en/latest'><img src='https://readthedocs.org/projects/hollandpy/badge/?version=latest' alt='Documentation Status' /></a>
    <a href="https://github.com/henrywoody/holland/blob/master/LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-purple.svg"></a>
</div>



### Description

Holland is a simple, flexible package for implementing the Genetic Algorithm in Python. The program is designed to act on an arbitrary evaluation function with arbitrary encoding of individuals within a population, both of which are provided by the user.

### Installing


Holland is available via the [Python Package Index (PyPI)](https://pypi.org/project/holland/) and can be installed with:

```shell
pip install holland
```

### Usage

[Full Documentation](https://hollandpy.readthedocs.io/en/latest/)

**Hello World!**

```python
from holland import Evolver
from holland.library import get_uniform_crossover_function
from holland.utils import bound_value
import random


# Define a fitness function
def fitness_function(genome):
    message = genome["message"]
    target = "Hello World!"
    score = 0
    for i in range(len(message)):
        score += abs(ord(target[i]) - ord(message[i]))
    return score

def mutation_function(value):
    mutated_value = ord(value) * random.random() * 2
    return chr(bound_value(mutated_value, minimum=32, maximum=126, to_int=True))

# Define genome parameters for individuals
genome_params = {
    "message": {
        "type": "[str]",
        "size": len("Hello World!"),
        "initial_distribution": lambda: chr(random.randint(32, 126)),
        "crossover_function": get_uniform_crossover_function(),
        "mutation_function": mutation_function,
        "mutation_rate": 0.15
    }
}

# Define how to select individuals for reproduction
selection_strategy = {"pool": {"top": 10}}

# Run Evolution
evolver = Evolver(
    fitness_function,
    genome_params,
    selection_strategy,
    should_maximize_fitness=False
)
final_population = evolver.evolve(stop_conditions={"target_fitness": 0})
```

With sample run:

> Generation: 0; Top Score: 201:     N~flx.JGcu-*
>
> Generation: 1; Top Score: 98:       Xljlw);mj]f 
>
> Generation: 2; Top Score: 64:       =c}kk SmsYf 
>
> Generation: 3; Top Score: 37:       Kcjlk$Vms]f 
>
> Generation: 4; Top Score: 24:       Cdjkn Smshf 
>
> Generation: 5; Top Score: 16:       Idjln Vmshf 
>
> Generation: 6; Top Score: 14:       Idjln Voshf 
>
> Generation: 7; Top Score: 11:       Hdjln Vmslf 
>
> Generation: 8; Top Score: 9:         Hdjln Voslf 
>
> Generation: 9; Top Score: 8:         Hdjln Vosle 
>
> Generation: 10; Top Score: 7:       Hdmln Vosle 
>
> Generation: 11; Top Score: 6:       Hdlln Vosle 
>
> Generation: 12; Top Score: 5:       Hdllo Vosle 
>
> Generation: 13; Top Score: 4:       Hdllo Vosle!
>
> Generation: 14; Top Score: 3:       Hello Vosle!
>
> Generation: 15; Top Score: 2:       Hello Wosle!
>
> Generation: 16; Top Score: 2:       Hello Wosle!
>
> Generation: 17; Top Score: 1:       Hello Worle!
>
> Generation: 18; Top Score: 1:       Hello Worle!
>
> Generation: 19; Top Score: 1:       Hello Worle!
>
> Generation: 20; Top Score: 0:       Hello World!

Best Genome:

```python
{
    'message': ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd', '!']
}
```
