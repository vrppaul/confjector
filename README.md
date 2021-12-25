# Simple configuration injector

Only purpose of the injector is to parse the config file and inject parsed config object into the function.

- Type hinted.
- Reads only `yaml` files.
- If name of a class corresponds to a section in config file - only that section will be parsed.
- All config file will be parsed otherwise.


## Example

```yaml
# conf.yml
params:
  first: 1
  second: text
  third: true
```

```python
# main.py
from confjector import inject
from pydantic import BaseSettings

class Params(BaseSettings):
    first: int
    second: str
    third: bool

@inject(conf_path="conf.yml")
def main(params: Params) -> None:
    print(params.first)
    print(params.second)
    print(params.third)
    
if __name__ == "__main__":
    main()
```
   
```python 
>>> 1
>>> "text"
>>> True
```