# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['antigen', 'antigen.filters', 'antigen.mutators', 'antigen.runners']

package_data = \
{'': ['*']}

install_requires = \
['setuptools>=62.1.0,<63.0.0', 'whatthepatch>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'antigen',
    'version': '0.2.0',
    'description': 'Extendable mutation testing framework',
    'long_description': '# Antigen\nExtendable mutation testing framework\n\n## What is mutation testing?\nMutation testing provides what coverage tries to, it finds logic that is not covered by your test suite.\n\nIt finds such places by applying mutations to your code and running the modified code against your test suite.\nIf the tests succeed with the mutated code, it means the changed expression is likely not covered ny the tests.\n\nIn comparison to coverage:\n\n:green_heart: Checks expressions, not lines.\n\n:green_heart: Checks whether the expression is covered, not whether it was executed.\n\n:x: Can find irrelevant mutants (e.g. mutations in logging or performance optimizations or a mutation that does not break the code)\n    \n:x: Executes the tests many times and therefore **takes much more time**.\n\nThere are mitigations for these downsides:\n\n:star:\tWe can mutate only lines that have changed in a given PR\n\n:star:\tWe can show the failing mutants via comments/warnings, as opposed to failing the whole CI pipeline.\n\nA much more in-depth explanation about the concept can be found in [This blog post by Goran Petrovic](https://testing.googleblog.com/2021/04/mutation-testing.html)\n\n## Why use Antigen?\n\n### Extendability\n\nIn my personal experience, trying to integrate mutation testing into your CI pipeline can be a bit challenging.\nThere are a lot of features you might want to customize to mitigate some of the downsides of mutation testing, or to be able to integrate it to your project and dev environment effectively.\n\nFor example, ignoring mutations on logging logic (which depends on your logging framework and conventions), or showing the results on various platforms (e.g. github, bitbucket, gitlab).\n\nAntigen puts extendability as a top priority so that adding mutation testing to your project is feasible.\n\nHow?\n\n#### Mechine friendly\nThe core of antigen is a pure python package that can be used by scripts.\n\nThe actual CLI uses the core package instead of the logic being coupled to it.\n\n#### Pluginable\nAntigen is written as a pipeline, each stage has an interface (e.g. Mutator, MutantFilter, Runner).\n\nExtending the logic is as simple as creating an object or function that matches that (simple) interface.\n\nThe Antigen CLI utilises [entry points](https://amir.rachum.com/blog/2017/07/28/python-entry-points/) so that antigen plugins can be added just by installing them with pip.\n\n## Usage\n\n*Antigen is currently in development, the API might change between versions.*\n\n```python\nantigen = Antigen(\n    filters=[PatchFilter.from_git_diff("develop")],\n    config=Config(project_root=Path("/home/myuser/myproject/")),\n)\n\nfor path in antigen.find_files("."):\n    for mutation in antigen.gen_mutations(path):\n        result = antigen.test_mutation(\n            mutation,\n            run_command="pytest",\n        )\n        print(result)\n```\n\n\n## Roadmap\n- [ ] Add CLI\n- [ ] Use `parso` instead of the built-in `ast` for cross-version mutations.\n- [ ] Add wrapper class for remote components (i.e. `RemoteFilter(hostname)`, `RemoteRunner(hostname)`).\n- [ ] Add Output component (with `JunitXMLOutput`, `GithubOutput`, `BitbucketOutput` builtins)\n- [ ] Add Cache component (with `FileCache`, `MongoCache` builtins)\n- [ ] Add Sorter component (for selecting the most likely to succeed mutations)\n',
    'author': 'Yanay Goor',
    'author_email': 'yanay.goor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/YanayGoor/Antigen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
