# Skinny dpa master thesis project

For the time being, quick and dirty with lots of redundancy.

Mostly text book HW dpa

Everything is created "on the fly", so there is something lacking in the performance department. As well as in the plotting department.

First 16 nibbles of plaintext are generated, then intermediate values are computed by running skinny w/ early exit after round 1. Due to the row operations (p xor k) is in fact shift_rows(mix_col(p xor k)). The round function of skinny.py is changed to avoid having to do this transformation, but a function is made in helpers.py.