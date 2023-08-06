# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_captcha']

package_data = \
{'': ['*'], 'fast_captcha': ['fonts/*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0']

setup_kwargs = {
    'name': 'fast-captcha',
    'version': '0.1.3',
    'description': 'fast to use captcha',
    'long_description': '# fast_captcha\n\nfast to use captcha\n\n# install\n\n```shell\npip install fast-captcha\n```\n\n## text_captcha\n\n```python\nfrom fast_captcha import text_captcha\n\nprint(text_captcha())  # BnZU\n```\n\n## img_captcha\n\n```python\nfrom fast_captcha import img_captcha\n\nimg, text = img_captcha()\n\nprint(img)  # <_io.BytesIO object at 0x000002366AB93DB0>\nprint(text)  # 2z22\n```\n\n# FastAPI\n\n```python\nfrom fastapi import FastAPI\nfrom fastapi.responses import StreamingResponse\n\nfrom fast_captcha import img_captcha\n\napp = FastAPI()\n\n@app.get(\'/captcha\', summary=\'captcha\', name=\'captcha\')\ndef get_captcha():\n    img, text = img_captcha()\n    return StreamingResponse(content=img, media_type=\'image/jpeg\')\n```\n\n# Django-Ninja\n\n```python\nfrom ninja import NinjaAPI\nfrom django.http import StreamingHttpResponse\n\nfrom fast_captcha import img_captcha\n\napp = NinjaAPI()\n\n@app.get(\'/captcha\', summary=\'captcha\', url_name=\'captcha\')\ndef get_captcha(request):\n    img, text = img_captcha()\n    return StreamingHttpResponse(streaming_content=img, content_type=\'image/jpeg\')\n```\n\n# License\nMIT License\n\nCopyright (c) 2022 xiaowu\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.',
    'author': 'wu',
    'author_email': 'jianhengwu0407@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitee.com/wu_cl/fast_captcha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
