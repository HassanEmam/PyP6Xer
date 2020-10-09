# PyP6Xer Python Primavera P6 XER parser
PyXer is an open source project to parse Primavera xer files in python. The project is work in progress and open for community contributions. 

In order to install a copy in your system you can use pip package manager as follows:

``` 
pip install PyP6XER
```

The usage of the library is fairly simple and the import examples can be:

```
from xerparser.reader import Reader
```

Here are some examples of reading and parsing xer files:

```
xer = Reader("<filename>") # this returns a reader object  
```

to reade all projects in file as one xer file may have multiple projects stored into it:

```
for project in xer.projects:
  print(project)
```
