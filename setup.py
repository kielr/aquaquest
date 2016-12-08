from distutils.core import setup

setup(name="Aquaquest!", # The package/module name
	  version="1.0",	 # The version
	  author="Kiel Regusters",
	  author_email="regustersk@gmail.com",
	  py_modules=["aquaquest_play"],
	  packages=["data", "data.libs", "data.states"],
          package_data={"data":["resources/graphics/*", "resources/music/*", "resources/maps/*",
            "resources/tilesets/*", "resources/sfx/*"]},
	  )
