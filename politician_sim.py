import matplotlib.pyplot as plt

import random

from typing import List

MAX_ISLAND = 7
SEED = 101

# real theta (the islands)
real_theta: List[int] = [i for i in range(1, MAX_ISLAND + 1)]

# real population plot
plt.bar(real_theta, real_theta, color='blue')
plt.xlabel(r'$\theta$')
plt.ylabel(r'$P(\theta)$')
plt.title('The distribution of population on the islands')
plt.show()


def run_mcmc(rounds: int, seed: int, islands: List[int]) -> List[int]:
    '''
    Runs the random-walk simulation `rounds` times
    and returns the resulting posterior distribution
    '''
    random.seed(seed)

    current: int = random.choice(islands)   # start somewhere
    proposal: int = 0
    n: int = len(islands)
    posterior: List[int] = [0 for _ in range(n)]
    round_count: int = 0

    while round_count < rounds:
        # determine which direction to take
        proposal_string: str = random.choice(['left','right'])
        if proposal_string == 'right':
            proposal = current + 1
        elif proposal_string == 'left':
            proposal = current - 1

        # condition for edge cases
        if (proposal > n) or (proposal < 0):
            proposal = 0

        p_move: float = min((proposal / current), 1)
        roulette: float = random.uniform(0, 1)
        if (roulette > 0) and (roulette <= p_move):
            current = proposal
        posterior[current - 1] += 1

        round_count += 1

    return posterior


# for post
for rounds in [100, 200, 500, 1000]:
    post = run_mcmc(rounds=rounds, seed=SEED, islands=real_theta)

    plt.bar([i for i in range(1, len(post) + 1)], post, color='brown')
    plt.xlabel(r'$\theta$')
    plt.ylabel('Frequency')
    plt.title(f'Posterior distribution of the population on the islands\n{rounds} Rounds')
    plt.savefig(f'posterior_{rounds}_rounds.png')
    plt.show()