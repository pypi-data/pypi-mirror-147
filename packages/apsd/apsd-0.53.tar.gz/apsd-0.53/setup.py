from setuptools import setup



setup(
    name='apsd',                    # package name
    version='0.53',                          # version
    description='Package Description',      # short description
    author_email='inspiredbycatdreams@gmail.com',
    install_requires=[''],                    # list of packages this package depends
    long_description = '''Random generation of TIN for legal entities and individuals
                    To generate a INN, you must specify InnType('YUR') for legal entities and 
                    InnType('FIZ') for individuals.\n 
                    In inn_withdrawal() the INN of the selected type is displayed\n
                    Example:\n
                            from apsd.inn import InnType\n
                            x = InnType('FIZ').inn_withdrawal()\n
                            print(x)\n
                            #904836365687

                    
                        ''',
    packages=['apsd'],              # List of module names that installing

) 