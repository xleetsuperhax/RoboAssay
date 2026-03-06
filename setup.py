from setuptools import setup, find_packages

setup(
    name='robotframework-roboassay',
    version='0.1.0',
    description='Robot Framework library for testing LLM-powered applications',
    author='RoboAssay Contributors',
    url='https://github.com/xleetsuperhax/RoboAssay',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=[
        'robotframework>=4.0.0',
        'requests>=2.25.0',
    ],
    keywords='robot framework testing llm ai accessibility',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Robot Framework',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
