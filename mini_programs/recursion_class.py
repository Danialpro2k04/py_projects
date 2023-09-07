class RecursiveFunction:
    def __init__(self, n):
        self.n = n
        print("Recursive function initialized with n =", n)

    def run(self, n=None):
        if n is None:
            n = self.n
        if n <= 0:
            return
        print("Running recursive function with n =", n)
        self.run(n-1)

    def __del__(self):
        print("Recursive function object destroyed")


# Create an object of the class
obj = RecursiveFunction(5)

# Call the recursive function
obj.run()

# Destroy the object
del obj
