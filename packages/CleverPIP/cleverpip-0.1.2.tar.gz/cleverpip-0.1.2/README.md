<h1>SmartPIP</h1>
<p>
    SmartPIP is a simple tool for automatically updating your PIP requirements.txt file
    in the most practical way possible.
</p>
<h2>Usage</h2>
<p>
    SmartPIP is a command line tool which only needs one argument, and a file.
    A 'smart_requirements.txt' (can be named however you want), has to be created. It is very similar to usual pip requirements.txt file but admits some additional parameters on the versioning.
</p>
    

```
smartpip --file path/to/smart_requirements.txt
```

<h2>Example</h2>
<p>Here is an example of a smart_requirements.txt file</p>

```
django==latest
djangorestframework==3.latest
numpy==1.26.latest    
```

<p>
    SmartPIP fragments the versioning and allows you to get the latest of a specific subversion, or directly the latest version out of every one of them. Of course you can still specify a specific version and it will also work.
</p>

