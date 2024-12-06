from setuptools import setup, find_packages

setup(
    name="terminal-agent",
    version="0.1.3",  
    packages=find_packages(),
    python_requires=">=3.7",  
    install_requires=[
        "transformers>=4.33.0",  
        "torch>=1.10.0",  
    ],
    entry_points={
        "console_scripts": [
            "terminal-agent=terminal_agent.agent:main",
        ],
    },
    author="Hamza Rehman (CloudDev Technologies)",
    author_email="hamza.rehman.shaikh@gmail.com",  
    description="A lightweight, natural language Linux terminal assistant.",
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown", 
    url="https://github.com/masterwithamza/terminal-agent",
    project_urls={
        "Bug Tracker": "https://github.com/masterwithamza/terminal-agent/issues",
        "Documentation": "https://github.com/masterwithamza/terminal-agent/wiki",
        "Source Code": "https://github.com/masterwithamza/terminal-agent",
    },
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",  
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="linux terminal assistant, natural language processing, command generator, AI assistant",
)
