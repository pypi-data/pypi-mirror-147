# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funer', 'funer.aggregators', 'funer.annotators', 'funer.converters']

package_data = \
{'': ['*']}

install_requires = \
['CJKwrap>=2.2,<3.0',
 'pyahocorasick>=1.4.4,<2.0.0',
 'spacy>=3.2.4,<4.0.0',
 'texttable>=1.6.4,<2.0.0',
 'wcwidth>=0.2.5,<0.3.0']

setup_kwargs = {
    'name': 'funer',
    'version': '0.0.2',
    'description': 'Rule based Named Entity Recognition tool.',
    'long_description': '# funer\n\n`funer` is Rule based Named Entity Recognition tool.\n\nWith `funer`, you can do the following:\n\n- Create rule based NER model.\n- Improve the rule and labeled data by comparing both.\n- Labeling data with labeling functioins. \n\n## Example\n\n- [Quick Example](./examples/example.ipynb)\n- [Quick Example [JP]](/examples/example_jp.ipynb)\n\n## Install\n\n## How to use\n\nCreate Document.\n\n```python\nfrom funer.document import Document\nimport spacy\n\n# Create documents\nnlp = spacy.load("en_core_web_sm")\n\nlabeled_document_1 = Document.from_spacy_doc(\n    nlp("Donald John Trump was born in New York."),\n    gold_entities=[\n        (0, 17, "PER"), # Donald John Trump\n        (30, 38, "LOC") # New York\n    ]\n)\nlabeled_document_2 = Document.from_spacy_doc(\n    nlp("Abe Rosenthal was editor-in-chief of the New York Times in 1998."),\n    gold_entities=[\n        (0, 13, "PER"),   # Abe Rosenthal\n        (41, 55, "ORG"),  # New York Times\n        (59, 63, "DATE"), # 1998\n    ]\n)\nnolabeled_document = Document.from_spacy_doc(\n    nlp("I want to go to New York."),\n)\ndocuments = [labeled_document_1, labeled_document_2, nolabeled_document]\n\n## Option: Tokenized\ntokenized_labeled_document_1 = Document(\n    tokens=[\'Donald\', \'John\', \'Trump\', \'was\', \'born\', \'in\', \'New\', \'York\', \'.\'],\n    spaces=[True, True, True, True, True, True, True, False, False],\n    gold_label=[\'B-PER\', \'I-PER\', \'I-PER\', \'O\', \'O\', \'O\', \'B-LOC\', \'I-LOC\', \'O\'],\n)\n```\n\nDefine Labeling Functions.\n\n```python\nfrom funer.annotators.dictionary_annotator import DictionaryAnnotator\nfrom funer.annotators.token_condition_annotator import (\n    TokensConditionAnnotator, generate_token_conditions_function)\nfrom funer.annotators.span_condition_annotator import SpanConditionAnnotator\n\n# Labeling functions\n## Define  Labeling Functions\n\n# f1: Per-token labeling function\ndef detect_name(tokens):\n    for i in range(len(tokens) - 3):\n        if tokens[i:i + 3] == ["Donald", "John", "Trump"]:\n            yield i, i + 3\nf1 = TokensConditionAnnotator(\n    name="person_f",\n    f=detect_name,\n    label="PER"\n)\n\n# f2: Per-token labeling function using generate_token_conditions_function\nf2 = TokensConditionAnnotator(\n    name="year_f",\n    f=generate_token_conditions_function([\n        lambda token_1: re.search(r"(19|20)\\d{2}", token_1) is not None,\n    ]),\n    label="DATE"\n)\n\n# f3: Per-character labeling functions\ndef span_condition_function(text: str):\n    for m in re.finditer(r"Abe Rosenthal", text):\n        yield m.start(), m.end()\nf3 = SpanConditionAnnotator(\n    name="person_f2",\n    f=span_condition_function,\n    label="PER"\n)\n\n\n# f4: Labeling functions with dictionary\n#   : (Note) Example of mistakenly extracting New York of New York Times as LOC\nloc_dictionary = ["New York", "Minneapolis"]\nf4 = DictionaryAnnotator(\n    name="city_f",\n    words=loc_dictionary,\n    label="LOC"\n)\n```\n\nApply labeling functions to documents.\n\n```python\nfrom funer.labeling_function_applier import LabelingFunctionApplier\nfrom funer.aggregators.majority_voting_aggregators import MajorityVotingAggregator\nfrom funer.utils import show_labels\n\n# Apply of labeling functions\nlf_applier = LabelingFunctionApplier(lfs=[f1, f2, f3, f4])\ndocuments = lf_applier.apply(documents)\n\n# Integration of labeling results\naggregator = MajorityVotingAggregator()\ndocuments = aggregator.aggregate(documents)\n\n# Output Results\nprint(show_labels(documents[0]))\n# > tokens       Donald   John    Trump   was   born   in   New     York    .\n# > =========================================================================\n# > gold_label   B-PER    I-PER   I-PER   O     O      O    B-LOC   I-LOC   O\n# > -------------------------------------------------------------------------\n# > person_f     B-PER    I-PER   I-PER   O     O      O    O       O       O\n# > city_f       O        O       O       O     O      O    B-LOC   I-LOC   O\n# > -------------------------------------------------------------------------\n# > aggregate    B-PER    I-PER   I-PER   O     O      O    B-LOC   I-LOC   O\n\n# Show stats\nprint(lf_applier.show_stats())\n# > f_name    | pos | neg | hit\n# > ==========+=====+=====+====\n# > person_f  | 1   | 0   | 1  \n# > year_f    | 1   | 0   | 1  \n# > person_f2 | 1   | 0   | 1  \n# > city_f    | 1   | 1   | 2  \n\n# Get label\nprint(documents[0].export_bio_label())\n# > [\'B-PER\', \'I-PER\', \'I-PER\', \'O\', \'O\', \'O\', \'B-LOC\', \'I-LOC\', \'O\']\n```',
    'author': 'Koga Kobayashi',
    'author_email': 'kajyuuen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
