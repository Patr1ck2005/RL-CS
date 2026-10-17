# RL-CS

**Historical game-agent and optimization experiments.** A custom Python game environment sits alongside neuroevolution, genetic algorithms, particle-swarm optimization and supervised-learning exercises.

[简体中文](README.zh-CN.md) · [History](docs/README-history.md)

## Repository map

| Path | Material |
|---|---|
| `Game/`, `Object/`, `map/` | Custom game rules, objects and maps |
| `Neuron_Network/`, `neat/` | Network integration and bundled NEAT source |
| [Algorithm/](Algorithm/) | GA, PSO, Bayesian/other optimization experiments |
| [SL/](SL/) | Separate supervised-learning exercises and sample assets |
| `main_neat.py`, `main_opt.py`, `main_gui.py` | Historical training/optimization/GUI entries |
| `CSDeepLearing_v*.zip` | Version archives retained as history |

## Status and use

A learning/experiment archive, not an agent integration for live Counter-Strike. The repository name does not establish that every experiment is reinforcement learning: the source includes multiple optimization and supervised-learning approaches.

There is no unified pinned environment, maintained installer or newly reproduced training result. Read a specific experiment and its imports before reconstructing an isolated environment; entry scripts may start training or open windows immediately. Do not treat bundled winner/checkpoint files or old archive versions as current benchmarks. This documentation update did not run the application, load serialized checkpoints or train agents.

## Attribution and license

Existing module names and contribution history are preserved. The bundled `neat/` library retains its [own license](neat/LICENSE) and attribution; that license does not automatically cover the rest of the repository. No repository-wide open-source license is declared. [Documentation history](docs/README-history.md) points to the original version note.
