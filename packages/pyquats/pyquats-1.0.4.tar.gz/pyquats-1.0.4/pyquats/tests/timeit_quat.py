#!/usr/bin/env python3
#
# Results for N = 1000000
#
# Quat from pyquats.quats
# 1000000 1.67090892792 (sum)
# 1000000 3.70148396492 (invert)
#
# Quat from pyquats.numpyquats
# 1000000 3.11191797256 (sum)
# 1000000 13.8228509426 (invert)

import random
import timeit
from pyquats.quats import Quat
#from pyquats.numpyquats import Quat

N = 1000000

a = [Quat(i) for i in range(1, N+1)]

print ( "Testing Quat (sum)..." )
t1 = timeit.Timer(lambda: sum(a))
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

print ( "Testing Quat (invert)..." )
t1 = timeit.Timer(lambda: [~q for q in a])
print ( "{} {}".format(N, t1.timeit(1)) )   # single run

# EOF
