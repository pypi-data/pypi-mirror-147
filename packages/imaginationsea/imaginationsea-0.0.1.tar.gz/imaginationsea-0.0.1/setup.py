from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='imaginationsea',
  version='0.0.1',
  description='This creates a very fast and easy-to-use virtual assistant that is completely customizable, at the same time has some tools that make controlling computers simple',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://python.imaginationsea.in/',  
  author='shivansh seth',
  author_email='inshivansh2008@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='fast app maker', 
  packages=find_packages(),
  install_requires=[
   'pyjokes',
   'DateTime'
   'pytz'
   'pycopy-webbrowser'
   'pyttsx3'
   'SpeechRecognition'
   'wikipedia'
]
)
