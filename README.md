# Tiny Parser

1. download dependencies with pip:
`pip install -r requirements.txt`
2. install [Graphviz](https://www.graphviz.org/download/)
3. start GUI from [main.py](main.py)

**note:**
The scanner has a disadvantage that it cannot distinguish between this char '-' as a minus operator or as a negative sign, so you must hardcode the difference using spaces as the following example:
- x := -1; {must have no spaces between '-' and '1'}
- x := 3 - 1; {must have a space between '-' and '1'}
