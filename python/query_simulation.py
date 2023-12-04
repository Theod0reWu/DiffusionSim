import sys
import segment_tree


def main():
    if len(sys.argv) != 4:
        print("Improper Number of commandline arguments: $ python query_simulation.py <input filename> <lower left "
              "corner> <upper right corner>")
        return None

    input_filename = sys.argv[1]
    lower_left_corner = sys.argv[2]
    upper_right_corner = sys.argv[3]
    data = list()

    with open(input_filename) as file:
        simulation_width, simulation_height = file.readline().split(' ')
        num_timesteps, dt = file.readline().split(' ')
        num_particles = int(file.readline())
        for particle in range(0, num_particles):
            positions = file.readline().strip().split(' ')
            positions = [x[1:-1] for x in positions]  # drop the parentheses
            positions = [x.split(',') for x in positions]
            positions = [segment_tree.Point(float(x[0]), float(x[1])) for x in positions]
            data.append(positions)

    segmented_data = list()  # a list of tuples of the form (timestamp, segment tree)
    for i in range(1, int(num_timesteps)):
        segments = [segment_tree.Segment(data[x][i-1], data[x][i], i) for x in range(num_particles)]
        segmented_data.append(segment_tree.SegmentTree(segments))



# $ python query_simulation.py <input filename> <lower left corner> <upper right corner>
if __name__ == '__main__':
    main()
