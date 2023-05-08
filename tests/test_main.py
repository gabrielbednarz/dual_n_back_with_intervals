import pytest
from main import return_image, return_sound, compare_expositions
import os
import string


@pytest.fixture
def image_files():
    return [os.path.join(os.getcwd(), 'images', f'{n}.jpg') for n in range(1, 7)]


def test_return_image(mocker, image_files):
    mocker.patch("numpy.random.randint", side_effect=range(1, 7))
    # With the line above, we change how return_image() function works inside this test.

    for expected_path in image_files:
        assert return_image() == expected_path


@pytest.fixture
def sound_files():
    return [os.path.join(os.getcwd(), 'sounds', f'{c}.mp3') for c in string.ascii_lowercase[:12]]


def test_return_sound(mocker, sound_files):
    mocker.patch("numpy.random.choice", side_effect=string.ascii_lowercase[:12])
    for expected_path in sound_files:
        assert return_sound() == expected_path


# Inside the next test function, we will make use of previously defined fixtures. Remember that fixtures can't be
# used inside the @pytest.mark.parametrize. The @pytest.mark.parametrize decorator is evaluated before the tests and
# fixtures are processed. Next, the shadowing of prev_tuple and cur_tuple variables occurs only within the scope of
# test_compare_expositions function.


@pytest.mark.parametrize("prev_tuple, cur_tuple, typed_choice, expected", [
    ((0, 0), (1, 1), 0, True),
    ((0, 0), (0, 1), 1, True),
    ((0, 0), (1, 0), 2, True),
    ((0, 0), (0, 0), 3, True),

    ((0, 0), (1, 1), 1, False),
    ((0, 0), (1, 1), 2, False),
    ((0, 0), (1, 1), 3, False),

    ((0, 0), (0, 1), 0, False),
    ((0, 0), (0, 1), 2, False),
    ((0, 0), (0, 1), 3, False),

    ((0, 0), (1, 0), 0, False),
    ((0, 0), (1, 0), 1, False),
    ((0, 0), (1, 0), 3, False),

    ((0, 0), (0, 0), 0, False),
    ((0, 0), (0, 0), 1, False),
    ((0, 0), (0, 0), 2, False)])
def test_compare_expositions(prev_tuple, cur_tuple, typed_choice, expected, image_files, sound_files):
    prev_tuple = (image_files[prev_tuple[0]], sound_files[prev_tuple[1]])  # Shadow the previous prev_tuple.
    cur_tuple = (image_files[cur_tuple[0]], sound_files[cur_tuple[1]])  # Shadow the previous cur_tuple.
    assert compare_expositions(prev_tuple, cur_tuple, typed_choice) == expected


# This is a more intuitive approach, but it's incorrect. Note that in both examples, the goal is to avoid hard-coding
# the file paths within the @pytest.mark.parametrize decorator, even though it's possible to do so.


# @pytest.mark.parametrize("prev_tuple, cur_tuple, typed_choice, expected", [
#     ((image_files[0], sound_files[0]), (image_files[1], sound_files[1]), 0, True),
#     ((image_files[0], sound_files[0]), (image_files[0], sound_files[1]), 1, True),
#     ((image_files[0], sound_files[0]), (image_files[1], sound_files[0]), 2, True),
#     ((image_files[0], sound_files[0]), (image_files[0], sound_files[0]), 3, True),
#
#     ((image_files[0], sound_files[0]), (image_files[1], sound_files[1]), 1, False),
#     ((image_files[0], sound_files[0]), (image_files[1], sound_files[1]), 2, False),
#     ((image_files[0], sound_files[0]), (image_files[1], sound_files[1]), 3, False),
#
#     ((image_files[0], sound_files[0]), (image_files[0], sound_files[1]), 0, False),
#     ((image_files[0], sound_files[0]), (image_files[0], sound_files[1]), 2, False),
#     ((image_files[0], sound_files[0]), (image_files[0], sound_files[1]), 3, False),
#
#     ((image_files[0], sound_files[0]), (image_files[1], sound_files[0]), 0, False),
#     ((image_files[0], sound_files[0]), (image_files[1], sound_files[0]), 1, False),
#     ((image_files[0], sound_files[0]), (image_files[1], sound_files[0]), 3, False),
#
#     ((image_files[0], sound_files[0]), (image_files[0], sound_files[0]), 0, False),
#     ((image_files[0], sound_files[0]), (image_files[0], sound_files[0]), 1, False),
#     ((image_files[0], sound_files[0]), (image_files[0], sound_files[0]), 2, False)])
# def test_compare_expositions(image_files, sound_files, prev_tuple, cur_tuple, typed_choice, expected):
#     assert compare_expositions(prev_tuple, cur_tuple, typed_choice) == expected
