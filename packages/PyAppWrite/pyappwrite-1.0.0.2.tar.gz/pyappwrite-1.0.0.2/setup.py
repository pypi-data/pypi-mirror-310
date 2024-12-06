import setuptools

long_description: str

# with open("README.md", "r", encoding="utf-8") as readme_file_desc:
    # long_description = readme_file_desc.read()

setuptools.setup(
  name = 'PyAppWrite',
  packages = [
    'PyAppWrite',
    'PyAppWrite/services',
    'PyAppWrite/encoders',
    'PyAppWrite/enums',
  ],
  version = '1.0.0.2',
  license='BSD-3-Clause',
  description = "Third Party Module with Persistent Session",
  long_description = "Third Party Module with Persistent Session\nFor more information, please refer to the official [Appwrite Documentation](https://appwrite.io/docs)",
  long_description_content_type = 'text/markdown',
  author = 'Smit Talsaniya',
  author_email = 'techsmitdevloper@gmail.com',
  maintainer = 'Smit Talsaniya',
  maintainer_email = 'techsmitdevloper@gmail.com',
  url = 'https://appwrite.io/support',
  download_url='',
  install_requires=[
    'requests',
  ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Environment :: Web Environment',
    'Topic :: Software Development',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
