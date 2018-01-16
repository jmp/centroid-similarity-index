from math import sqrt


def calculate_distance(p, q):
    """Calculates the Euclidean distance between the points p and q."""
    return sqrt(sum((x - y) ** 2 for x, y in zip(p, q)))


def find_nearest(point, points, distance_function=calculate_distance):
    """Of the set of points, finds the one nearest to the given point."""
    nearest_point = None
    nearest_distance = None
    for other in points:
        distance = distance_function(point, other)
        if nearest_distance is None or distance < nearest_distance:
            nearest_point = other
            nearest_distance = distance
    return nearest_point


def calculate_mapping(points1, points2):
    """Maps each point in points1 to its nearest point in points2."""
    return dict((p, find_nearest(p, points2)) for p in points1)


def csi(solution1, solution2):
    """Calculates the point-level centroid similarity index (CSI)."""
    assert len(solution1) == len(solution2)

    centroids1 = solution1.keys()
    centroids2 = solution2.keys()
    mapping1 = calculate_mapping(centroids1, centroids2)
    mapping2 = calculate_mapping(centroids2, centroids1)

    num_shared_points = 0

    for centroid, mapping in mapping1.items():
        s1 = set(solution1[centroid])
        s2 = set(solution2[mapping])
        num_shared_points += len(s1.intersection(s2))

    for centroid, mapping in mapping2.items():
        s2 = set(solution2[centroid])
        s1 = set(solution1[mapping])
        num_shared_points += len(s2.intersection(s1))

    total_points = sum(len(x) for x in solution1.values())

    return num_shared_points / (2 * total_points)
