my_dict = {'a': [1, 2, 3], 'b': {4, 5, 6}, 'c': 123}
my_dict = {'a':[1,2,3], 'b':my_dict, 'c':123}
bla = my_dict.pop('b', None)
print(my_dict)
print(bla)