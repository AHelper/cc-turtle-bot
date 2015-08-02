from setuptools import setup

setup(
  name = "ccturtle",
  version = "0.1",
  author = "Collin Eggert",
  author_email = "ahelper2@gmail.com",
  description = ("Python backend for CC turtles"),
  license = "GPLv3",
  packages=["ccturtle"],
  install_requires=[
    "tornado"
  ],
  entry_points={
    "console_scripts": ["ccturtlesrv = ccturtle.server:start"]
  }
)