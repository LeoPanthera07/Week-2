# Test every conversion the AI suggested
# Mark each as CORRECT / WRONG / MISSING EDGE CASE

# int -> others
print(float(42))        # 42.0
print(str(42))          # '42'
print(bool(42))         # True
print(bool(0))          # False
print(list(42))         # TypeError!
print(tuple(42))        # TypeError!

# float -> others
print(int(3.99))        # 3 (truncates, does NOT round)
print(int(-3.99))       # -3 (truncates toward zero)
print(str(3.99))        # '3.99'
print(bool(0.0))        # False

# str -> others
print(int("42"))        # 42
print(int("3.99"))      # ValueError!
print(int("hello"))     # ValueError!
print(float("3.99"))    # 3.99
print(bool("False"))    # True  (non-empty string!)
print(bool(""))         # False
print(list("abc"))      # ['a', 'b', 'c']
print(tuple("abc"))     # ('a', 'b', 'c')

# bool -> others
print(int(True))        # 1
print(int(False))       # 0
print(float(True))      # 1.0
print(str(True))        # 'True'

# list -> others
print(tuple([1, 2, 3]))     # (1, 2, 3)
print(bool([]))             # False
print(bool([0]))            # True (non-empty list!)

# tuple -> others
print(list((1, 2, 3)))      # [1, 2, 3]
print(bool(()))             # False