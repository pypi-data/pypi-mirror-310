StupidGen ![version](https://framagit.org/squirrrr/stupidgen/-/badges/release.svg)
=========

Stupidly simple template generator for people that don't want to learn an yet an other way to write a for loop.

Installation 
----

You need to have python installed. Install the latest release with: 
```
pip install stupidgen
```

The development version can be installed with the following commands:

```bash
git clone https://framagit.org/squirrrr/stupidgen.git
cd stupidgen 
pip install .
```

Check your installation with the following command:
```bash 
stupdigen --version
```

Usage 
----

Example for python, but many other languages are supported. Check out the [documentation](http://stupidgen-1b56ce.frama.io/).

```python
#test.py.multi

for i in range(5) : 
	>Hello world {% i %}
```

Then run your program with:

```bash
stupidgen -C --run test.py.multi
```

This produces the following output:

```text
Hello world 0
Hello world 1
Hello world 2
Hello world 3
Hello world 4
```

Development 
---

You can use the ./stupidgen bash script at the source of the repository to make sure that you run the local version of the program, and not the one you might have installed globally.

Some tests are provided in the `tests/`folder to verify that the output remain correct. They can be run with:

```bash
sh tests/runTests.sh
```

Finally, the code for the documentation pages is in the `doc/` folder, and uses mkdocs. To host it locally you will need to install the dependencies with:: 
```
pip install -r doc/requirements.txt 
```
Then a test version of the website that automatically reloads when you make changes can be started with:
```
cd doc && mkdocs serve
```

Contributing
---
Contributions are welcome. Check out the open issues, or open your own if you have suggestions for improvements/bugs to report.

License
----
This software is distributed under the GNU General Public License v3.
