from setuptools import find_packages, setup

with open("README.md", "r") as f:
    description_md = f.read()
    
setup(
    name='ds_tomato',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        "openai",
        "langchain",
        "langchain-openai",
        "pinecone-client",
        "langchain-community",
        "langchain-pinecone"
    ],
    long_description=description_md,
    long_description_content_type="text/markdown"
)
