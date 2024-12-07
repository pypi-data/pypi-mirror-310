# Steps

```bash
git clone https://github.com/alemuller/tree-sitter-make.git
cd tree-sitter-make
tree-sitter generate  # Either the `npm` version or the `cargo` version work
gcc -o parser.so -shared -fPIC src/parser.c
```
