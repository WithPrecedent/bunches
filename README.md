The goal of bunches is provide lightweight, turnkey, extensible data containers.
bunches's framework supports a wide range of coding styles. You can create 
complex multiple inheritance structures with mixins galore or simpler, 
compositional objects.

The current classes available (as bunches.ContainerThatIWant) are:
    Listing: list-like class with 'add', 'prepend', and 'subset' methods. The
        'add' method tries to intelligently decide whether the passed item(s)
        to add should be appended or extended on the stored list.
    Hybrid: list-like class that also has a full dict interface. Stored items
        must have a 'name' attribute or allow name inference via the 'get_name'
        function.
    Dictionary: dict-like class with 'add' and 'subset' methods. It also 
        includes a 'default_factory' parameter providing the same functionality
        as a defaultdict.
    Catalog: dict-like class that allows lists of keys to be used for its
        various methods (including dunder access methods) and supports three
        wildcard keys: 'none', 'default', and 'all'. If lists of keys are 
        passed or the 'default' and 'all' keys are used, a list of values is
        returned.
    Library: dict-like class that includes two chained dicts: 'instances' and
        'classes'. Users can deposit classes and instances in a Library and
        they are stored and accessed intelligently. When instances are 
        deposited, it is stored in 'instances' and its class is stored in 
        'classes'.

The project is also highly documented so that users and developers and make
bunches work with their projects. It is designed for Python coders at all 
levels. Beginners should be able to follow the readable code and internal
documentation to understand how it works. More advanced users should find
complex and tricky problems addressed through efficient code.
