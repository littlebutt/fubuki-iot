from setuptools import setup


with open("README.md", "r", encoding='UTF-8') as f:
    long_description = f.read()


setup(
    name='fubuki-iot',
    version='0.3',
    python_requires=">=3.8",
    packages=['iot', 'iot.core', 'iot.core.hardware', 'iot.core.acoustics', 'iot.core.semantics', 'iot.integration'],
    install_requires=['keyboard>=0.13.5', 'loguru>=0.6.0', 'paho-mqtt>=1.6.1', 'PyAudio>=0.2.12', 'pydantic>=1.10.2',
                      'python-dotenv>=0.21.0', 'requests>=2.28.1'],
    url='https://github.com/littlebutt/fubuki-iot',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT License',
    author='littlebutt',
    author_email='luogan1996@icloud.com',
    description='An accessable Iot Terminal implementated by Python'
)
