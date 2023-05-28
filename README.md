# PyCustomScript (0.1.0)

## Custom Sintax

- Dictionary Destructuration
```py
obj = {
    "name" : "Jonh",
    "age" : 21,
    "email" : "jonh@sample-email.com",
    "role" : "Developer"
}

{name, role} = obj

print(name, role) # Jonh Developer
```
- JS-like Anonimous Functions
```py
even_numbers: List[int] = list(filter(
    (n) => { n%2 == 0 },
    numbers
))
```
## Optimization
- To Cython Convertion. 
```toml
# config.toml
...
to_cython = true
```
