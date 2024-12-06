from setuptools import setup, find_packages 



setup(
    name="CONTROLE_DE_DESPESAS_PESSOAIS",                     
    version="0.1.0",                        
    author="Claudia Gabriela",                       
    author_email="claudiagabriela578@gmail.com",     
    description="controle de despesas pessoais",
    long_description_content_type="text/markdown",
    url="https://claudiagabriela72.github.io/python/",  
    packages=find_packages(),                
    install_requires=[                       
        "sqlite3",
        "PIL",
        "matplotlib",
        "pandas"
    ],
    classifiers=[                            
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',                 
)