import argparse
import subprocess

from simimg import DEFAULT_MATCHES_THRESHOLD, SimImg


def main():
    parser = argparse.ArgumentParser(
        description="Compare images and find groups of similar ones"
    )
    parser.add_argument(
        "dir",
        metavar="<images directory>",
        type=str,
        help="Directory with images to compare for similarity",
    )
    parser.add_argument(
        "-t",
        metavar="<matches threshold>",
        type=int,
        default=DEFAULT_MATCHES_THRESHOLD,
        help="How many matches should be found to treat images as similar",
    )
    parser.add_argument(
        "-view",
        metavar="<image viewer>",
        type=str,
        default=None,
        help="Image viewing program to show similar images",
    )

    args = parser.parse_args()
    img_dir = args.dir
    img_viewer = args.view
    threshold = args.t

    si = SimImg(print_progress=True, matches_threshold=threshold)
    si.load(img_dir)
    groups_of_similar = si.find_similar()

    for i, group in enumerate(groups_of_similar):
        print(f"Group of similar images #{i + 1}")
        processes = []

        for img in group:
            print(f"\t- {img}")
            if img_viewer:
                processes.append(subprocess.Popen(f"{img_viewer} {img}", shell=True))

        if img_viewer:
            input(
                "Press enter to close the opened group of similar images and show next one"
            )
            for p in processes:
                p.terminate()

    if not groups_of_similar:
        print(f"No similar images has been found at {img_dir}")


if __name__ == "__main__":
    main()
