import imghdr
import itertools
from os import path, walk

from feature_matching import get_matches
from temp_print import TempPrint

DEFAULT_DISTANCES_RATIO_THRESHOLD = 0.4
DEFAULT_MATCHES_THRESHOLD = 8


class SimImg:
    """ Compares images and finds groups of similar ones """

    def __init__(
        self,
        print_progress=False,
        dist_ratio_threshold=DEFAULT_DISTANCES_RATIO_THRESHOLD,
        matches_threshold=DEFAULT_MATCHES_THRESHOLD,
    ):

        self.print = TempPrint(print_progress)
        self.dist_ratio_threshold = dist_ratio_threshold
        self.matches_threshold = matches_threshold

        self.image_files = set()
        self.groups_of_similar = []

    def load(self, entry_points):
        """ Finds all images in the dir(s) path(s) """
        self.print.text("Searching for images...")
        for entry_point in entry_points.split():
            for dir_path, _, filenames in walk(entry_point):
                for filename in filenames:
                    abs_path = path.abspath(f"{dir_path}/{filename}")
                    if imghdr.what(abs_path) is not None:
                        self.image_files.add(abs_path)
        self.print.text(f"Found {len(self.image_files)} images")

    def find_similar(self):
        images_len = len(self.image_files)
        combos_len = int(images_len * (images_len - 1) / 2)
        progress_label = f"Comparing {combos_len} image combinations"

        for i, (img1_path, img2_path) in enumerate(
            itertools.combinations(self.image_files, 2)
        ):
            self.print.progress_bar((i + 1) / combos_len, label=progress_label)
            if self._is_similar_pair(img1_path, img2_path):
                self._register_similar_pair(img1_path, img2_path)

        self.print.text(f"Compared {combos_len} image combinations\n")
        return self.groups_of_similar

    def _is_similar_pair(self, img1_path, img2_path):
        # To avoid duplication in the cache
        sorted_img_paths = sorted([img1_path, img2_path])

        good_matches = sum(
            m_dist < self.dist_ratio_threshold
            for m_dist in get_matches(*sorted_img_paths)
        )

        return good_matches >= self.matches_threshold

    def _register_similar_pair(self, path_1, path_2):
        for group_of_similar in self.groups_of_similar:
            if path_1 in group_of_similar or path_2 in group_of_similar:
                # Group with at least one of the images exists,
                # ensuring both images are added to the set and quit func
                group_of_similar.add(path_1)
                group_of_similar.add(path_2)
                return
        # Not found, creating new set
        self.groups_of_similar.append({path_1, path_2})
