## Installation

`pip install feng-hirst-rst-parser`

## README.md and README_original.md

This project is a fork of an update of the original Feng-Hirst RST parser repo. The original README.md is included as
README_original.md. It is recommended to install this project as a Python package and use it that way. This should
simplifiy usage significantly and make it more accessible.
This README.md will focus on the current version and does not include instructions for how to run the original version.

## General Information

* This RST-style discourse parser produces discourse tree structure on full-text level, given a raw text. No prior
  sentence splitting or any sort of preprocessing is expected. The program runs on Linux systems.
* The overall software work flow is similar to the one described in the paper by Feng and Hirst (ACL 2014). They removed
  the post-editing component from the workflow, as well as the set of entity-based transaction features from our feature
  set. Moreover, both structure and relation classification models are implemented using CRFSuite.

## Usage

### Example
See [`example.py`](feng_hirst_parser/example.py) for a very simple example. Note that this requires both `matplotlib` and `pydot` to run. The plotting functionality is not required to use the parser, hence these packages are not listed as requirements, and you will have to install them yourself.


### More detailed usage

First instantiate the parser:

```python
parser = DiscourseParser(
        verbose,
        skip_parsing,
        global_features,
        save_preprocessed,
        output_dir=output_dir
    )
```

Then parse your file to get a `ParseTree`:
    
```python
pt = parser.parse(os.path.join(current_file_dir, 'example.txt'))
```

You can convert this `ParseTree` to a `networkx` graph:

```python
G = pt.to_networkx()
```

Which should make it much easier to work with or to analyze the tree structure.

Additionally metrics can be extracted:

```python
metrics = extract_metrics(G, relation_ngrams=[(1, 2), (3, 4)])
```
At the moment this gives you the depth of the tree, counts how often each relation occurs, and `relation_ngrams` can tell you how often each 'ngram' is found in the paths from the root node to all the leaf nodes.

### Command-line usage and more

Refer to README_original.md for more information.

## Bugs and comments

If you encounter and bugs using the program, please create an Issue on
the [GitHub repo](https://github.com/ThHuberSG/feng-hirst-rst-parser).

## Developers

* Original author: [Vanessa Wei Feng](mailto:weifeng@cs.toronto.edu), Department of Computer Science, University of
  Toronto, Canada
* [Arne Neumann](mailto:github+spam.or.ham@arne.cl) updated it to use nltk 3.4
  on [this github repo](https://github.com/arne-cl/feng-hirst-rst-parser), and created a Dockerfile.
* [Zining Zhu](mailto:zining@cs.toronto.edu) updated the scripts to use Python 3.
* Thomas Huber, Chair of Data Science and Natural Language Processing, University of St. Gallen, updated the scripts
  further and added the `networkx` functionality.

## References

* Vanessa Wei Feng and Graeme Hirst, 2014. Two-pass Discourse Segmentation with Pairing and Global Features. arXiv:
  1407.8215v1. http://arxiv.org/abs/1407.8215
* Vanessa Wei Feng and Graeme Hirst, 2014. A Linear-Time Bottom-Up Discourse Parser with Constraints and Post-Editing.
  In Proceedings of the 52th Annual Meeting of the Association for Computational Linguistics: Human Language
  Technologies (ACL-2014), Baltimore, USA. http://aclweb.org/anthology/P14-1048
