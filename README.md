# meta-babel
Data generator library for meta-learning language learning algorithms

## Install
```
pip install -r requirements.txt
```

## Usage

`main.py` defines a simple interface where languages configurations are defined directly in code, and then generation is controlled with several CLI parameters. For example, to use the `dfa_simple` configuration to generate 1,024 languages with around 10,000 tokens each, run the following command.
```
python main.py --config dfa_simple --languages 1024 --tokens 10_000 --output dfa_simple.pickle
```

This creates a (roughly) 80 MB pickle file containg a list of lists of 1-dimensional numpy arrays.

To create your own languages configurations, edit `main.py` to add an additional configuration.
