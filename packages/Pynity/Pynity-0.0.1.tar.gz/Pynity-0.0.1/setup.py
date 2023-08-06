from setuptools import setup

setup(
  # Needed to silence warnings (and to be a worthwhile package)
    name='Pynity',
    url='',
    author='Lime_Gradient',
    author_email='limegradientyt@gmail.com',
    # Needed to actually package something
    packages=[
      'unipy'
    ],
    # Needed for dependencies
    install_requires=[
      ''
    ],
    # *strongly* suggested for sharing
    version='0.0.1',
    # The license can be anything you like
    license='MIT',
    description='Bring Unity coding into Python',
    # We will also need a readme eventually (there will be a warning)
    long_description="Bringing Untiy to the Python Language one code block at a time!"
)