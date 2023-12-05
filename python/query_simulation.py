import math
import sys
import segment_tree


"""
Returns a tuple (begin,end) of start and end indices (inclusive)
"""
def get_timesteps_from_range(data, start: float, end: float, dt: float):
    # TODO: Perform a binary search for the start and end values instead of a linear scan
    # In practice, this probably doesn't matter for simulations with less than a few thousand timesteps...
    retval = list()
    for timestep, _ in data:
        if timestep >= start and round(timestep / dt) < math.ceil(end / dt):
            retval.append(round(timestep / dt))

    return retval


def main():
    if len(sys.argv) != 8:
        print("Improper Number of commandline arguments: $ python query_simulation.py <input filename> <left> <right> <top> <bottom> <start time> <end time>")
        return None

    input_filename = sys.argv[1]
    left = float(sys.argv[2])
    right = float(sys.argv[3])
    top = float(sys.argv[4])
    bottom = float(sys.argv[5])
    start_time = float(sys.argv[6])
    end_time = float(sys.argv[7])
    data = list()

    with open(input_filename) as file:
        simulation_width, simulation_height = file.readline().split(' ')
        num_timesteps, dt = file.readline().split(' ')
        num_timesteps = int(num_timesteps)
        dt = float(dt)
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
        segmented_data.append((i*dt, segment_tree.SegmentTree(segments)))

    # Execute a single query for now... TODO: do something more exciting with the data.
    timestep_index_range = get_timesteps_from_range(segmented_data, start_time, end_time, dt)
    total_segments = set()
    for timestep, tree in segmented_data[timestep_index_range[0]:timestep_index_range[1]]:
        total_segments |= tree.window_query(left, right, top, bottom)

    print(f'{len(total_segments)} distinct particles observed in query box between time {start_time} and time {end_time}')


if __name__ == '__main__':
    main()
