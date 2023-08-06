from setuptools import setup

setup(
    name='gembed',
    version='1.0.1',    
    description='Graph Embedding Package',
    url='https://github.com/pranavacharya/graph_embedding',
    author='Pranav Acharya',
    author_email='apranav.acharya@gmail.com',
    license='MIT License',
    packages=['gembed', 
            'gembed.algorithms', 
            'gembed.walks'],
    install_requires=['gensim==3.6.0',
                      'tqdm'                  
                      ]
)