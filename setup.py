import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
    name='pylifx',
    version='0.0.1',
    author='Your Name',
    author_email='your_email@here',
    description='A low-level python wrapper around the LIFX LAN v2 API. Exposes a small synchonous interface with nothing \'going on behind the scenes\'.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marcushultman/lifx-lan-python',
    project_urls = {
        'Bug Tracker': 'https://github.com/marcushultman/lifx-lan-python'
    },
    license='MIT',
    packages=['pylifx'],
    install_requires=[],
)

