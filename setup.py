from setuptools import Command, setup, find_packages


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys, subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


setup(
    name='lshhdc',
    version='1.0.0',
    description='LSHHDC : Locality-Sensitive Hashing based High Dimensional Clustering',
    author='Mike Starr',
    url='https://github.com/go2starr/lshhdc',
    packages=['lsh'],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
    ],
)
