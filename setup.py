from setuptools import setup

setup(
    name='fubuki-iot',
    version='0.1',
    python_requires=">=3.8",
    packages=['iot', 'iot.core', 'iot.core.hardware', 'iot.core.acoustics', 'iot.core.semantics', 'iot.integration'],
    url='https://github.com/littlebutt/fubuki-iot',
    license='MIT License',
    author='littlebutt',
    author_email='luogan199686@gmail.com',
    description='An accessable Iot Terminal implementated by Python'
)
