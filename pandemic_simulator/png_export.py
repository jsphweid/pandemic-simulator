from typing import List, Optional
import os

import png
from PIL import Image

from shutil import rmtree

from pandemic_simulator.person import Person

default_alpha = 255

white = [255, 255, 255, default_alpha]
cool_grey = [149, 144, 168, default_alpha]
english_violet = [99, 75, 102, default_alpha]
emerald_green = [22, 193, 114, default_alpha]
maximum_yellow = [255, 252, 49, default_alpha]
red = [252, 68, 15, default_alpha]

# TODO: why can't I use the type here? Circular dependency?
State = List[List[Optional[Person]]]

temp_folder_dir = "./temp"


def _remove_temp_dir() -> None:
    rmtree(temp_folder_dir, ignore_errors=True)


# TODO: rename functions
def make_film(states: List[State], filename: str = "movie.mp4"):
    if len(states) >= 10000:
        raise Exception("This many frames isn't supported yet.")

    # remove and recreate temp folder
    _remove_temp_dir()
    os.mkdir(temp_folder_dir)

    # fill it up with sequential pngs that will become frames
    for i, state in enumerate(states):
        _render_person_grid_state_to_temp(i, state)

    # use ffmpeg to combine them into a single mpeg
    # os.system(f"ffmpeg -r 1 -start_number 0 -framerate 25 -i img%05d.png -vcodec mpeg4 -y {filename}")
    os.system(f"ffmpeg -start_number 0 -framerate 20 -i {temp_folder_dir}/img%05d.png -y {filename}")

    # clean up
    # _remove_temp_dir()


def _render_person_grid_state_to_temp(i: int, state: State) -> None:
    rows = []
    for _row in state:
        row = []
        for cell in _row:
            for num in _encode_maybe_person(cell):
                row.append(num)
        rows.append(row)
    filename = f"{temp_folder_dir}/img{'{:05d}'.format(i)}.png"
    png.from_array(rows, 'RGBA').save(filename)

    # increase resolution TODO: this isn't that optimial...
    im = Image.open(filename)
    im_resized = im.resize((1200, 1200), Image.NONE)
    im_resized.save(filename, "PNG")


def _encode_maybe_person(person: Optional[Person]) -> List[int]:
    if person:
        if person.is_infected:
            return maximum_yellow
        elif person.is_recovered:
            return cool_grey
        else:
            return emerald_green
    else:
        return white
