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


def calculate_num_points_in_solution(solution):
    """Calculates the number of data points in the given solution."""
    return sum(len(points) for points in solution.values())


def calculate_num_shared_points(points1, points2):
    """Returns the number of points shared by the two collections."""
    return len(set(points1).intersection(set(points2)))


def csi(solution1, solution2):
    """Calculates the point-level centroid similarity index (CSI)."""
    total_points1 = calculate_num_points_in_solution(solution1)
    total_points2 = calculate_num_points_in_solution(solution2)

    centroids1 = solution1.keys()
    centroids2 = solution2.keys()
    mapping1 = calculate_mapping(centroids1, centroids2)
    mapping2 = calculate_mapping(centroids2, centroids1)

    num_shared_points = 0

    for centroid, mapping in mapping1.items():
        num_shared_points += calculate_num_shared_points(
            solution1.get(centroid, []),
            solution2.get(mapping, []),
        )

    for centroid, mapping in mapping2.items():
        num_shared_points += calculate_num_shared_points(
            solution1.get(mapping) or [],
            solution2.get(centroid) or [],
        )

    return 1.0 * num_shared_points / (total_points1 + total_points2)
