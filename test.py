import unittest


def test():
    print("Test Start...")
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    print('Done!')


if __name__ == '__main__':
    test()