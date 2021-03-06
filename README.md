# Quantum Unfolding

Unfolding with quantum computing

## Check out package
```
git clone https://github.com/rdisipio/quantum_unfolding.git
```

## Test out calculation

In the file `toy_unfolding_classical.py` you can modify the definition of xedges, of the truth-level vector (`x`) and the response matrix (`R`). The code compares the product `Rx=y` carried out with decimal and binary representation, the latter to be used for the quantum computation.

The response matrix is converted to binary by recognizing that the linear vector space is spanned by `(n_cols X n_bits)` standard basis vectors `v`, i.e.:
```
( 0, 0, ..., 1 )
( 0, 1, ..., 0 )
( 1, 0, ..., 0 )
```
Multiplying `Rv` "extracts" the column corresponding to the non-zero element, e.g. `R x (1,0,...,0)^T` returns the first column of `R`. By iteration, we can convert R from decimal to binary.

The matrix-vector multiplication is carried out as usual, with the only exception that the carry bit has to be taken into account. 

```
./test_matrix_multiplication.py
```

To test the unfolding:

```
./toy_unfolding_classical.py
```

