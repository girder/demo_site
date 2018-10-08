from setuptools import setup, find_packages

setup(
    name='girder-demo-site',
    version='1.0.0',
    description='algorithms.kitware.com demo site',
    author='Kitware, Inc.',
    url='https://github.com/girder/demo_site',
    license='Apache 2.0',
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: Web Environment',
      'License :: OSI Approved :: Apache Software License'
    ],
    include_package_data=True,
    package_data={ '': ['dist'] },
    packages=find_packages(exclude=['plugin_tests']),
    zip_safe=False,
    install_requires=[
        'girder>=3.0.0a1',
        'girder-jobs>=3.0.0a1',
        'girder-worker',
        'girder-worker-utils>=0.7.2'
    ],
    entry_points={
        'girder.plugin': [ 'demo_site = girder_demo_site:DemoSitePlugin' ]
    }
)
