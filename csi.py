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


def calculate_shared_points(points1, points2):
    """Returns the number of points shared by the two collections."""
    return len(set(points1).intersection(set(points2)))


def csi(solution1, solution2):
    """Calculates the point-level centroid similarity index (CSI)."""
    assert len(solution1) == len(solution2)

    total_points1 = sum(len(x) for x in solution1.values())
    total_points2 = sum(len(x) for x in solution2.values())

    assert total_points1 == total_points2

    centroids1 = solution1.keys()
    centroids2 = solution2.keys()
    mapping1 = calculate_mapping(centroids1, centroids2)
    mapping2 = calculate_mapping(centroids2, centroids1)

    num_shared_points = 0

    for centroid, mapping in mapping1.items():
        num_shared_points += calculate_shared_points(
            solution1[centroid],
            solution2[mapping],
        )

    for centroid, mapping in mapping2.items():
        num_shared_points += calculate_shared_points(
            solution1[mapping],
            solution2[centroid],
        )

    return num_shared_points / (2 * total_points1)
