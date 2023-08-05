import setuptools


setuptools.setup(
     name='cli-changelog-md',
     author="Y. Chudakov",
     author_email="kappasama.ks@gmail.com",
     version='1.0.1',
     description="A package for automatization work with changelog.md",
     packages=setuptools.find_packages(),
     package_dir={'cli-changelog-md': 'cli-changelog-md/'},
     install_requires=['click>=8.1.2', 'python-gitlab>=2.10.0'],
     classifiers=[
         "Programming Language :: Python :: 3",
     ],
     scripts=['bin/changelog'],
     python_requires='>=3.8'
)
