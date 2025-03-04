from setuptools import find_packages,setup

setup(
    name='information_reterival_system',
    version='0.0.1',
    author='sai',
    author_email='sailaxmi.tumu06@gmail.com',
    install_requires=["python-dotenv","langchain","google-generativeai","streamlit","faiss-cpu","PyPDF2"],
    packages=find_packages()
)