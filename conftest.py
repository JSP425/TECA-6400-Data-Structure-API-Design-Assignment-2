import random
import string

import pytest

@pytest.fixture
def random_number():
    num=random.random()
    # print(f"randomnum={num}")

    return num