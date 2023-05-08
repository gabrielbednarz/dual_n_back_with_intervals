import matplotlib.pyplot as plt
from playsound import playsound
from pathlib import Path
import multiprocessing
from PIL import Image
import numpy as np
import time
import os


'''
First, you should load six pictures named 1.jpg, 2.jpg,..., 6.jpg into the images folder. This is 
a dual n-back game, where "dual" means you will receive a picture and a piano sound. You also have 
to type the interval between the current and previous sound. There are 12 sounds, all different and 
within one octave, and 6 pictures. When dealing with intervals, you type the number n (-11 <= n <= 11), 
which signifies how many semitones apart the presented piano sounds are. Due to some issues with 
the playsound() function, files containing sounds are named using alphabet letters.
'''


def return_image():
    n = np.random.randint(1, 7)  # In most cases, stochastic functions should be mocked.
    image_path = os.path.join(os.getcwd(), 'images', f'{n}.jpg')  # To create platform-independent file paths.
    return image_path  # Supposedly, it is generally not recommended to mock such fundamental functions as os.path.join.


def task_image(i):
    numpied = np.asarray(Image.open(i))
    plt.axis('off')
    plt.imshow(numpied)
    # exit_event.set()
    plt.pause(2)


def return_sound():
    m = np.random.choice(list('abcdefghijkl'))
    sound_path = os.path.join(os.getcwd(), 'sounds', f'{m}.mp3')
    return sound_path


def task_sound(j):
    playsound(j)


def compare_expositions(prev_tuple, cur_tuple, typed_choice):

    picture_match = cur_tuple[0] == prev_tuple[0]
    sound_match = cur_tuple[1] == prev_tuple[1]

    typed_choice_effect = False

    if not any([picture_match, sound_match]) and typed_choice == 0:
        typed_choice_effect = True

    elif picture_match and not sound_match and typed_choice == 1:
        typed_choice_effect = True

    elif not picture_match and sound_match and typed_choice == 2:
        typed_choice_effect = True

    elif all([picture_match, sound_match]) and typed_choice == 3:
        typed_choice_effect = True

    return typed_choice_effect


points = 0

paired_stimuli_tuples = []


if __name__ == '__main__':

    the_n_back = int(input('Your level of n in the n-back game is: '))
    while the_n_back < 1:
        the_n_back = int(input('Your level of n in the n-back game is (n should be above 0): '))

    number_of_trials = int(input('Type how many trials you want to play: '))
    while number_of_trials < the_n_back + 2:
        number_of_trials = int(input(f'The number of trials should be at least {the_n_back + 2}. '
                                     f'Type how many trials you want to play: '))

    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console or terminal screen depending on the OS.

    for _ in range(number_of_trials):

        exposition = (i := return_image(), j := return_sound())
        paired_stimuli_tuples.append(exposition)

        process1 = multiprocessing.Process(target=task_image, args=(i,))
        process2 = multiprocessing.Process(target=task_sound, args=(j,))

        process1.start()
        process2.start()

        process1.join()
        process2.join()

        if len(paired_stimuli_tuples) == the_n_back + 1:

            print('Type 0 if none, 1 if picture, 2 if sound, 3 if both occurred n-back.')
            answer = int(input('Here: '))

            compared = compare_expositions(paired_stimuli_tuples[0], exposition, answer)
            interval = ord(Path(exposition[1]).stem) - ord(Path(paired_stimuli_tuples[0][1]).stem)

            if compared:
                points += 1
                print('Correct.')
            else:
                print('Incorrect.')

            print(your_interval_answer := int(input('Type the interval: ')))

            if interval == your_interval_answer:
                points += 1
                print('Correct interval.')
            else:
                print(f'Incorrect. The interval was {interval}.')

            paired_stimuli_tuples.pop(0)

        os.system('cls' if os.name == 'nt' else 'clear')

    print(f'Your score: {round(points * 50 / (number_of_trials - the_n_back))}%.')
