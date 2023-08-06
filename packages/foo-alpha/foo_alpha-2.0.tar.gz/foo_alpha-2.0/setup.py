from setuptools import setup

setup(
   name='foo_alpha',
   version='2.0',
   description='A useful module',
   author='Man foo_alpha',
   author_email='foomail@foo.com',
   packages=['foo_alpha'],  #same as name
   install_requires=[], #external packages as dependencies
)