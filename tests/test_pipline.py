import project2pipline as proj

def test_random(random_number):
    print(random_number)
    assert type(random_number) == float
