from setuptools import setup, find_packages
 
setup(
      name='shine_package',
      version='1.0.4',
      description='This is a first-principle calcluation package based on atomic orbital DFT',
      url='https://github.com/IamRocketSwallow/shine',
      author='jingzhe',
      author_email='jingzhe@tianyan3d.com',
      license='Proprietary',
      packages=find_packages(),
      zip_safe=False,
      platforms=["linux"],
      long_description=open('README.rst').read(),
classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],include_package_data=True,
          )


