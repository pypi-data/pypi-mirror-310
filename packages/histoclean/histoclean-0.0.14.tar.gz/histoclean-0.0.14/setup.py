from setuptools import setup

setup(
    name='histoclean',
    version='0.0.14',
    description='Histoclean (initial package setup)',
    py_modules=["histoclean"],
    package_dir={'': 'src'},
    install_requires=[
        "Pillow", "opencv-python", "imageio",
        "numpy", "numba", "imagecorruptions",
        "openslide-python", "opencv-contrib-python", "scipy", "imgaug",
        "scikit-image"
    ],
    include_package_data=True,
    package_data={"Icon": ["*.png", "*.ico"]}

)
