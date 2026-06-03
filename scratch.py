from typing import Callable


class A:
    def __del__(self):
        print("Deleting instance of A")

    def test(self):
        print("test A")

    def my_method(self):
        print("my method A")

class B:
    def __del__(self):
        print("Deleting instance of B")
    def test(self):
        print("test B")

    def my_method(self):
        print("my method B")

if __name__ == "__main__":
    a = A()
    b = B()
    print(hash(a.test))
    print(hash(b.test))

    m1: Callable[[], None] = a.my_method
    m2: Callable[[], None] = b.my_method

    tester:dict[int, str] = {}
    tester[1] = "one"
    tester[2] = "two"
    tester[3] = "three"
    tester[4] = "four"

    print(tester)

    if 7 in tester:
        tester.pop(7)
    tester.pop(3, None)
    print(tester)

    del a
    b = None

   