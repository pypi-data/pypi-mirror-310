import shutil

import setuptools
from distutils.extension import Extension

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
import setuptools
from distutils.extension import Extension
from Cython.Build import cythonize
import os


def find_pyx_packages(base_dir):
    extensions = []
    for dirpath, _, filenames in os.walk(base_dir):
        for filename in filenames:
            if filename.endswith(".py"):  # Change to .py for in-place renaming
                if filename == "__init__.py":
                    continue  # Skip __init__.py

                # Rename file to .pyx
                old_path = os.path.join(dirpath, filename)
                new_path = os.path.join(dirpath, filename[:-3] + ".pyx")
                # os.rename(old_path, new_path)
                shutil.copy(old_path, new_path)
                print(f"Renaming {old_path} to {new_path}")

                # Create extension for the renamed file
                module_path = new_path.replace('/', '.').replace('\\', '.')
                module_name = module_path[:-4]  # Remove the .pyx extension
                extensions.append(
                    Extension(name=module_name, language="c++", sources=[new_path]))
                print(f'add Extension: {module_name} {[new_path]}')
    return extensions


base_dir = "ok"
extensions = find_pyx_packages(base_dir)

setuptools.setup(
    name="ok-script",
    version="0.0.337",
    author="ok-oldking",
    author_email="firedcto@gmail.com",
    description="Automation with Computer Vision for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ok-oldking/ok-script",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        'pywin32>=306',
        'darkdetect>=0.8.0',
        'PySideSix-Frameless-Window>=0.4.3',
        'typing-extensions>=4.11.0',
        'PySide6-Essentials>=6.7.0',
        'GitPython>=3.1.43',
        'requests>=2.32.3',
        'psutil>=6.0.0'
    ],
    python_requires='>=3.9',
    ext_modules=cythonize(extensions)
)
