import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os


def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    if np.max(np.abs(vec1 - vec2)) < 0.001 or np.max(
            np.abs(vec1 + vec2)) < 0.001:
        return np.eye(3)

    a, b = (vec1 /
            np.linalg.norm(vec1)).reshape(3), (vec2 /
                                               np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s**2))


def plot_unit_sphere(ax: plt.Axes):
    """ Plot a unit sphere centered at the origin
    :param ax: The axes to plot on
    """
    u, v = np.mgrid[0:2 * np.pi:80j, 0:np.pi:80j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_surface(x, y, z, color="w", alpha=0.3)


def plot_shortest_path_3d(start: np.ndarray, end: np.ndarray, steps: int, ax: plt.Axes = None):
    """ Plot the shortest path between two points on a sphere
    :param start: A 3d vector representing the start point
    :param end: A 3d vector representing the end point
    :param steps: The number of steps to take along the path
    """
    # Normalize the vectors
    start, end = start / np.linalg.norm(start), end / np.linalg.norm(end)

    normal_vec = np.cross(start, end)
    rot_mat_1 = rotation_matrix_from_vectors(normal_vec, np.array([0, 0, 1]))
    start_reg = rot_mat_1 @ start
    inv_rot_mat_1 = np.linalg.inv(rot_mat_1)
    rot_mat_2 = rotation_matrix_from_vectors(start_reg, np.array([1, 0, 0]))
    inv_rot_mat_2 = np.linalg.inv(rot_mat_2)

    # angle between start and end
    end_reg = rot_mat_2 @ (rot_mat_1 @ end)
    sign = np.sign(end_reg[1])
    angle = np.arccos(np.dot(start, end))
    theta_steps = sign * np.linspace(0, angle, steps)
    x, y = np.cos(theta_steps), np.sin(theta_steps)
    z = np.zeros_like(x)
    circle_vec = np.row_stack((x, y, z))
    circle_vec = inv_rot_mat_2 @ circle_vec
    circle_vec = inv_rot_mat_1 @ circle_vec

    # fig = plt.figure(figsize=(10, 10))
    # ax = fig.add_subplot(111, projection='3d')
    # plot_unit_sphere(ax)
    ax.plot3D(circle_vec[0], circle_vec[1], circle_vec[2], color="black", linewidth=1)

    ax.scatter(start[0], start[1], start[2], color="g")
    ax.scatter(end[0], end[1], end[2], color="y")


def plot_shortest_path_list(points):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    plot_unit_sphere(ax)

    for i in range(len(points)-1):
        start = points[i]
        end = points[i+1]
        plot_shortest_path_3d(start, end, 100, ax)
    




if __name__ == '__main__':
    # # random a list of 3d points
    # points = np.random.rand(10, 3) * 2 - 1
    # plot_shortest_path_list(points)
    # plt.show()

    action_paths = ["our_output_27"]
    for action_path in action_paths:
        # iterate through files under the action path
        positions = []
        for filename in sorted(os.listdir(action_path)):
            # TODO: check the sequence of the files
            if filename.endswith('.npy'):
                file_path = os.path.join(action_path, filename)
                data = np.load(file_path, allow_pickle=True).item()
                positions.append(data['position'])
                print(file_path)
        plot_shortest_path_list(positions)
        plt.show()
        plt.savefig('foo.png')