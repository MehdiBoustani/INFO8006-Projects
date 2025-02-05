# Bayes Filter Agent

## Description

This project implements a Pacman agent using the **Bayes filter algorithm** to locate and eat ghosts in a maze. The agent receives noisy distance measurements and must infer ghost positions before capturing them.

## Files

- `bayesfilter.py`: Implements the Bayes filter algorithm and the ghost-eating agent.
- `ghostAgents.py`: Defines ghost behaviors (afraid, fearless, terrified).

## Usage

To run the Bayes filter agent against an **afraid** ghost on the large_filter layout:

```console
$ python run.py --ghost afraid --nghosts 1 --layout large_filter --seed 42
```

To test with multiple ghosts using the same behavior:

```console
$ python run.py --ghost terrified --nghosts 3 --layout large_filter --seed 42
```

## Implementation Details

- The **transition_matrix** function models ghost movement probabilities.
- The **observation_matrix** function models sensor noise.
- The **update** function implements the Bayes filter.
- The **Pacman agent** decides actions based on the belief state of ghost positions.

## Evaluation Criteria

- **Transition Matrix (25%)**: Accuracy of ghost movement modeling.
- **Observation Matrix (25%)**: Correct handling of noisy sensor inputs.
- **Update Function (25%)**: Proper Bayesian belief update.
- **Pacman Controller (20%)**: Efficiency in capturing ghosts.
- **Code Style (5%)**: PEP-8 compliance.

## Grade

This project was graded **15/20**

## Authors

- [Mehdi Boustani](https://github.com/MehdiBoustani)
- [Antoine Kinable](https://github.com/AntoineKin)
- [Abdelkader Albashityalshaier](https://github.com/AbdelkaderULG)

