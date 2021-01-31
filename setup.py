from setuptools import setup
import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = ''
with open('DiscordMegaBot/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(name='DiscordMegaBot',
      author='Connor',
      url='https://github.com/ConnorTippets/DiscordMegaBot',
      project_urls={
        "Issue tracker": "https://github.com/ConnorTippets/DiscordMegaBot/issues",
      },
      version=version,
      license='MIT',
      description='A Discord bot with tons of commands',
      long_description=readme,
      long_description_content_type="text/x-md",
      include_package_data=True,
      install_requires=requirements,
      python_requires='>=3.8.0',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
      ]
)
