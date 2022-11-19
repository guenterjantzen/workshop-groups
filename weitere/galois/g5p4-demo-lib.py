#https://github.com/syakoo/galois-field
#pip install git+https://github.com/syakoo/galois-field

from galois_field import GFpn

# Generating the field GF(5^4)
gf = GFpn(5, [1, 0, 0, 0, 2])

# Generating an element in GF(5^4)
el1 = gf.elm([1, 2])  # 1x + 2
el2 = gf.elm([1, 2, 3, 4, 5]) # 2x^3 + 3x^2 + 4x + 3

# Arithmetics
el1 + el2 # 2x^3 + 3x^2
el1 - el2 # 3x^3 + 2x^2 + 2x + 4
el1 * el2 # 2x^3 + 1x + 2
el1 / el2 # 3x^3 + 4x^2

# The Inverse of elements.
el1.inverse() # 3x^3 + 4x^2 + 2x + 1
el2.inverse() # 1x^3 + 1x^2 + 2x + 1

print(el1)
