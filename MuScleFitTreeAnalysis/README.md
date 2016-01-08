The code has a CMSSW-like structure with the analyzers instantiated like *plugins* in `main.cpp`.
Analyzers have a `analyze()` and a `endjob()` methods.

* Compiling the code 
``` 
make all
```

* Running the ode
```
./main <input_root_tree>
```



