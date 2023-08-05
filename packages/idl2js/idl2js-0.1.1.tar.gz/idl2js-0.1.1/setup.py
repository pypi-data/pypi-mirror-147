# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idl2js',
 'idl2js.intermediate',
 'idl2js.js',
 'idl2js.js.built_in',
 'idl2js.webidl',
 'idl2js.webidl.generated']

package_data = \
{'': ['*'], 'idl2js.js.built_in': ['mime/*']}

install_requires = \
['antlr4-python3-runtime>=4.9.3,<5.0.0',
 'attrs>=21.4.0,<22.0.0',
 'click>=8.0.4,<9.0.0',
 'graphviz>=0.19.1,<0.20.0',
 'more-itertools>=8.12.0,<9.0.0',
 'stringcase>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'idl2js',
    'version': '0.1.1',
    'description': 'Grammar-based Fuzzer that uses WebIDL as a grammar.',
    'long_description': "# idl2js\n\n**Grammar-based Fuzzer that uses WebIDL as a grammar.**\n\n[![Build Status](https://img.shields.io/travis/PrVrSs/idl2js/master?style=plastic)](https://travis-ci.org/github/PrVrSs/idl2js)\n[![Codecov](https://img.shields.io/codecov/c/github/PrVrSs/idl2js?style=plastic)](https://codecov.io/gh/PrVrSs/idl2js)\n[![Python Version](https://img.shields.io/badge/python-3.10-blue?style=plastic)](https://www.python.org/)\n[![License](https://img.shields.io/cocoapods/l/A?style=plastic)](https://github.com/PrVrSs/idl2js/blob/master/LICENSE)\n\n\n## Quick start\n\n```shell script\npip install idl2js\n```\n\n\n### Build from source\n\n*Get source and install dependencies*\n```shell script\ngit clone https://gitlab.com/PrVrSs/idl2js.git\ncd idl2js\npoetry install\n```\n\n*Download ANTLR tool*\n```shell script\nwget https://www.antlr.org/download/antlr-4.9.3-complete.jar\n```\n\n*Generate parser*\n```shell script\nmake grammar\n```\n\n*Run tests*\n```shell script\nmake unit\n```\n\n\n### Examples\n\n```python\nfrom pathlib import Path\nfrom pprint import pprint\n\nfrom idl2js import InterfaceTarget, Transpiler\n\n\nclass Blob(InterfaceTarget):\n    kind = 'Blob'\n\n\ndef main():\n    transpiler = Transpiler(idls=(str(Path('blob.webidl').resolve()),))\n    transpiler.transpile(\n        targets=[\n            Blob,\n        ]\n    )\n\n    pprint(transpiler.js_instances)\n\n\nif __name__ == '__main__':\n    main()\n```\n\n\n#### Output\n\n```js\ntry {v_e94935e94c7945829b5caeb9ba0201b8 = ['cwg']} catch(e){},\ntry {v_4291cb5afec94ab3a460aefec633a11e = {type: 'wwny', endings: 'transparent'}} catch(e){},\ntry {v_21068e2708dd47cd8c147e7ada78a3a0 = new Blob(v_e94935e94c7945829b5caeb9ba0201b8, v_4291cb5afec94ab3a460aefec633a11e)} catch(e){},\ntry {v_58e162f31a56467cab976d37a37c4811 = ['p', v_21068e2708dd47cd8c147e7ada78a3a0]} catch(e){},\ntry {v_5b148aa1d99e47d08642f65b2506d8e6 = {type: 'nrlsqlvc', endings: 'transparent'}} catch(e){},\ntry {v_9828d85447f94e67accf856e0c09d2f9 = new Blob(v_58e162f31a56467cab976d37a37c4811, v_5b148aa1d99e47d08642f65b2506d8e6)} catch(e){},\ntry {v_181663ba04e740699e6b59e8cb6bf49c = [v_9828d85447f94e67accf856e0c09d2f9, 'rkffvhfhtx']} catch(e){},\ntry {v_c40591cfedec48cc8f367b32b92157fc = {type: 'jl', endings: 'native'}} catch(e){},\ntry {v_6a1bcadcadbb4985b4a2951c4600f8b7 = new Blob(v_181663ba04e740699e6b59e8cb6bf49c, v_c40591cfedec48cc8f367b32b92157fc)} catch(e){},\ntry {v_9c73ddd4f3f845c3a39e6cc908047b4e = [v_6a1bcadcadbb4985b4a2951c4600f8b7, 'bafassyvz']} catch(e){},\ntry {v_9f8d17f370924cbb87314b057600f348 = {type: 'utnlst', endings: 'transparent'}} catch(e){},\ntry {v_26948eb73f774ac39365c5b09229d4cd = new Blob(v_9c73ddd4f3f845c3a39e6cc908047b4e, v_9f8d17f370924cbb87314b057600f348)} catch(e){}\n```\n\n\n### Links\n\n* [searchfox - webidl](https://searchfox.org/mozilla-central/source/dom/webidl)\n* [original webidl parser](https://github.com/w3c/webidl2.js)\n* [TSJS-lib-generator](https://github.com/microsoft/TSJS-lib-generator/tree/master/inputfiles/idl)\n* [ECMAScript® 2021 Language Specification](https://tc39.es/ecma262/)\n* [Web IDL](https://heycam.github.io/webidl)\n* [Web IDL Spec](https://webidl.spec.whatwg.org/)\n\n\n## Contributing\n\nAny help is welcome and appreciated.\n\n\n## License\n\n*idl2js* is licensed under the terms of the Apache-2.0 License (see the file LICENSE).\n",
    'author': 'Sergey Reshetnikov',
    'author_email': 'resh.sersh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/PrVrSs/idl2js',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
