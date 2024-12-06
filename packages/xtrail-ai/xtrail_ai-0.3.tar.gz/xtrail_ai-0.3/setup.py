from setuptools import setup, find_packages

setup(
    name="xtrail_ai",  # New package name
    version="0.3",
    description="Retrieve machine details, monitor resources, and execute jobs dynamically.",
    author="Harisha P C",
    author_email="info@xtrail.in",
    url="https://xtrail.in",  # Optional: Link to the source code or documentation
    packages=find_packages(),
    install_requires=[
        "psutil>=5.9.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Use the appropriate license
        "Operating System :: OS Independent",
    ],
    keywords="machine-id machine-learning resource-monitoring dynamic-execution",
    python_requires=">=3.6",
)
