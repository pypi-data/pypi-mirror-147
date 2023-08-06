#!/usr/bin/env python
# coding: utf-8

# In[1]:


import setuptools

with open('C:/Users/Hindy/Desktop/python packages/Container_ForwardStepwiseFeatureSelection/README.md', 'r') as fh:
    long_descripion = fh.read()
    
setuptools.setup(
    name='ForwardStepwiseFeatureSelection', 
    version='1.3.9',
    author='Hindy Yuen', 
    author_email='hindy888@hotmail.com',
    license='MIT',
    description='Performaning feature selection in forward stepwise selection maner.', 
    long_description=long_descripion, 
    long_description_content_type='text/markdown', 
    url='https://github.com/HindyDS/ForwardStepwiseFeatureSelection', 
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
],
    keywords='forward stepwise features feature select selection machine learning data science computer science recursive feature elimination dimentionality reduction ',
    package_dir={"":"ForwardStepwiseFeatureSelection"},
    packages=['ForwardStepwiseFeatureSelection'],
    python_requires='>=3.6'
)

