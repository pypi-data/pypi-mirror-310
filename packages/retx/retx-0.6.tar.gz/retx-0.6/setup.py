from distutils.core import setup

v = 6

setup(
    name = 'retx',         # How you named your package folder (MyLib)
    packages = ['retx'],   # Chose the same as "name"
    version = f'0.{v}',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'retransform. transforming data',   # Give a short description about your library
    author = 'andy',                   # Type in your name
    author_email = 'andyworms@gmail.com',      # Type in your E-Mail
    url = 'https://github.com/andyil/retx',   # Provide either the link to your github or to your website
    download_url = f'https://github.com/andyil/retx/archive/v_0{v}.tar.gz',    # I explain this later on
    keywords = ['data', 'json', 'csv'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
       # 'validators',
       # 'beautifulsoup4',
    ],
  scripts=['retx/__main__.py'],
    entry_points={
        'console_scripts': [
            'retx = retx.m:main_function',  # 'retx' is the command, 'retx.module_name' is the module, 'main_function' is the function to call
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
