import cv2

from file_cache import cached


DEFAULT_HESSIAN_THRESHOLD = 850

DETECTOR = cv2.xfeatures2d.SURF_create(DEFAULT_HESSIAN_THRESHOLD)
MATCHER = cv2.FlannBasedMatcher.create()


@cached(f"descs.{DEFAULT_HESSIAN_THRESHOLD}ht.cache")
def descriptor_from_path(abs_path):
    img = cv2.imread(abs_path, cv2.IMREAD_GRAYSCALE)
    _, descriptor = DETECTOR.detectAndCompute(img, None)
    return descriptor


@cached(f"matches.{DEFAULT_HESSIAN_THRESHOLD}ht.cache")
def get_matches(img1_path, img2_path):
    desc1 = descriptor_from_path(img1_path)
    desc2 = descriptor_from_path(img2_path)
    good_matches = []
    for m in MATCHER.knnMatch(desc1, desc2, 2):
        dist_ratio = m[0].distance / m[1].distance
        if dist_ratio < 0.5:
            good_matches.append(dist_ratio)
    return good_matches
