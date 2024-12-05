from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cubemap2pano',
    version='0.0.4',
    description='Convert cubemap to equirectangular panorama image',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='serpong',
    author_email='tykim@xrleader.co.kr',
    url='https://github.com/xrleader/cubemap2pano',
    install_requires=[
        'torch',
        'torchvision'
    ],
    packages=find_packages(exclude=[]),
    keywords=['panorama', 'cubemap', 'equirectangular', 'image', '360', 'vr'],
    python_requires='>=3.6',
    package_data={},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Multimedia :: Graphics',
    ],
)
