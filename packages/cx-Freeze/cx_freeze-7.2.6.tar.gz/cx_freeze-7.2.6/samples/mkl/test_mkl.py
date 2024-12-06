from __future__ import annotations

import numexpr as ne
import numpy as np

print("numexpr version", ne.__version__)
print("numpy version", np.__version__)

a = np.random.rand(1000000)
b = np.random.rand(1000000)

ne.set_vml_num_threads(4)

result = ne.evaluate("3 * a + 4 * b")
print("result", result)
