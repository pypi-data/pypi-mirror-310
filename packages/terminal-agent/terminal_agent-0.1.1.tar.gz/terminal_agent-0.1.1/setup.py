from setuptools import setup, find_packages

setup(
    name="terminal-agent",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "transformers",
        "torch",
    ],
    entry_points={
    "console_scripts": [
        "terminal-agent=terminal_agent.agent:main",
    ],
},

    author="Hamza Rehman (CloudDev Technologies)",
    description="A natural language Linux terminal assistant.",
    url="https://github.com/masterwithamza/terminal-agent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
)
