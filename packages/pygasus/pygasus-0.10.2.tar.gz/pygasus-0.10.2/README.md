# pygasus

A lightweight Sqlite ORM built on top of Pydantic.

## Installation

The easiest way to install Pygasus is to use `pip`, preferably inside a virtual environment:

    pip install pygasus

`pygasus` supports Python 3.7, 3.8, 3.9 and 3.10.

## Getting started

Pygasus allows you to create your models using type annotations.  This model will then be converted to something that can be stored (in a database):

```python
from pygasus import Model

class User(Model):

    """An user."""

    id: int
    name: str
    age: int
    height: float
```

You then need to add this model to Pygasus:

```python
from pygasus.storage import SQLStorageEngine

# The default storage engine is SQLAlchemy, connected to Sqlite3.
storage = SQLStorageEngine("test.sql")
# ... you can also just create the database in memory for testing:
storage = SQLStorageEngine(memory=True)

# Then you need to add your models.
storage.bind_models({User})

# You can call `bind_models` without any argument, but in this case,
# make sure to import your `User` class (and your other models)
# before you do that.

# Create a new user.
user = User.repository.create(name="Vincent", age=33, height=5.7)
# Notice that we don't specify the `id`.  This field will be set by
# the storage engine Pygasus uses.

# At this point, our new user has been created, stored and returned.
print(user.id) # 1
print(user.name) # Vincent
user.age = 21 # Well, why not?
# This will call an immediate update in the storage.

# Of course we can also query a model:
queried = User.repository.get(id=1)

# Due to caching, the queried user will be identical (in terms of reference).
print(user is queried) # True

# You can control the cache to remove this behavior.
```

This should show you some basic concepts.  To learn more, head over to the documentation.

## Contributing

If you wish to develop Pygasus, all you need is:

- Docker: getting a working Docker engine isn't that complicated on Linux, Windows or Mac OS.
- Make: getting Make is more complicated, but it's not exactly required.  If you're on Windows, don't despair.  You might rely on Bash itself, it's available (and easy to access if you have WSL installed).

Pygasus relies on Docker images to make sure it remains usable on the supported Python versions: the idea is that each version will run in a diffferent Docker container, built on a different image.  This process is automated, and you don't really need to understand it to use it, but it might be worth diving into the scripts (see the `scripts` directory).

### Initializes the images

Once you have cloned the `pygasus` repository, you must create the images for the required Python versions.  This is not exactly mandatory, as other scripts will make sure the images exist (and will build them if necessary), but this might make things easier, particularly in case of errors.

Pygasus supports four Python versions: 3.7, 3.8, 3.9 and 3.10.  You can initialize them all at once, though it will take time:

    make init

Get yourself a cup of coffee and stare at the process: each image is downloaded and built in turn.  Additional packages are installed.  Pygasus will install additional dependencies, then install Poetry and let it handle other Python dependencies, so that each image uses the same versions in dependencies.

If you wish to build images individually:

    make init version=3.7

This will build the image only for Python 3.7 (called pygasus-3.7).  Running each build one at a time makes it easier to spot errors.

On the other hand, only panics if a build actually fails: it's not that uncommon to see warnings and even errors during the build process, but most of the time, this can be ignored... unless the build itself fails (you will be warned if that happens, don't worry).

> Curious? Try to look at the images in Docker: `docker images` .  You should see the four `pygasus-VERSION` images along with the `python-VERSION-slim` build (this is the image on which Pygasus images are built).

Don't have Make?  If you have Bash, you can still run the command:

    bash scripts/init.sh

Initializing isn't a "fire and forget" command.  Should Pygasus dependencies change or critical security bugs be fixed in Python images, it is recommended to run `make init` once more.

### Testing

Now that you have your Pygasus images, you can run the test suite in all versions at once:

    make test

This will run the test suite in every Python version and display the result on the screen.  This might take a little while, but you should see the progress.  Obviously, if a test fails in a supported Python version, this is a big deal and something to fix for the next commit.  It is recommended to run `make test` before committing anything.

Don't have Make?  No worries:

    bash scripts/test.sh

You can also run the test suite in a specific version, though this is less useful:

    make test version=3.9

### Linter

Pygasus uses black and flake8 as linters.  If you have written some code, make sure it's properly formatted before committing:

    make check-style

This won't do any modification in your code, this will merely display the errors (if any).  Fix them before committing!

It's also possible to format your code using black:

    make format

This will actually edit your files in a proper format.  However, notice that flake8 isn't involved.  Sometimes, it sees potential errors black will ignore, so make sure `make check-style` is completely empty before committing.

You don't have Make?  No worries:

    bash scripts/check_style.sh
    bash scripts/format.sh

### Debugging

When coding, it can help to actually see what Pygasus does when you execute a line of code.  It is possible to start a shell inside of the container where Pygasus is installed.  You can then access to `pdb` to debug or run some arbitrary code:

    make shell

If no version is specified, run in the first version (that is, 3.7).  It is assumed that it might be harder to break compatibility that way.  You can specify a version though:

    make shell version=3.10

Once connected to the container, you can execute commands (including `poetry`, `python` and such).

Don't have Make?  No worries:

    bash scripts/shell.sh

### Cleaning up

The started containers using the previous commands will not be maintained: once you exit them, they will go away.  However, images are kept.  Although this usually doesn't pose many problems, these images are heavy.  You can remove images without tags (usually, Pygasus images have got only one tag).

    make clean

This shouldn't be necessary.  Keep an eye on the output of the `docker images` command to see if Docker keeps images it shouldn't.

### Updating images

It bears reminding, once built, Pygasus images aren't changed.  If a major security bug is fixed and a new Python image is pushed to Docker hub, you won't have it.  If Pygasus dependencies change, you might run into errors.

At any point, you can force-update the Pygasus images:

    make init

This will pull the Python image from Docker and rebuild the Pygasus image even if you already have one.
