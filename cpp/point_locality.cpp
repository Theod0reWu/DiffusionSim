#include <iostream>
#include <CGAL/Cartesian.h>
#include <CGAL/Segment_tree_k.h>
#include <CGAL/Range_segment_tree_traits.h>

typedef CGAL::Cartesian<double> K;
typedef CGAL::Segment_tree_map_traits_2<K, char> SegmentTreeTraits;
typedef CGAL::Segment_tree_2<SegmentTreeTraits> SegmentTree;
typedef SegmentTreeTraits::Interval Interval;
typedef SegmentTreeTraits::Pure_interval Pure_interval;
typedef SegmentTreeTraits::Key Key;
typedef K::Point_2 Point;

/**
 * Given a timestep, generate a segment tree containing the movements of each particle between
 * t-1 and t.  Requires timestep > 0.
 */
SegmentTree generateSegmentTreeAtTimestep(const std::vector<std::vector<Point>>& particles, int timestep) {
    assert(timestep > 0);
    assert(particles.size() > 0);

    std::vector<Interval> segments;

    for (int particle = 0; particle < particles.size(); particle++) {
        assert(particles[particle].size() > timestep);
        Key previous_position(particles[particle][timestep - 1].x(), particles[particle][timestep - 1].y());
        Key current_position(particles[particle][timestep].x(), particles[particle][timestep].y());

        // TODO: Apply some randomness to ensure segments are not axis-aligned

        segments.push_back(Interval(Pure_interval(previous_position, current_position), particle));
    }

    return SegmentTree(segments.begin(), segments.end());
}

int main(int argc, char* argv[]) {
    assert(argc == 2);

    // Read metadata from the file
    std::ifstream simulation_results(argv[1]);

    double simulation_width;
    simulation_results >> simulation_width;

    double simulation_height;
    simulation_results >> simulation_height;

    int num_timesteps;
    simulation_results >> num_timesteps;

    double timestep_size;
    simulation_results >> timestep_size;

    int num_particles;
    simulation_results >> num_particles;

    // A hack to allow us to marshal the data as necessary
    // Stores data in the form [particle][timestep]
    std::vector<std::vector<Point>> particles;
    for (int particle = 0; particle < num_particles; particle++) {
        particles.push_back(std::vector<Point>());
        for (int timestep = 0; timestep < num_timesteps; timestep++) {
            std::string point;
            simulation_results >> point;

            // Drop the parentheses
            point = point.substr(1, point.size() - 2);

            // Split the comma-separated point into x and y coordinates
            int split_pos = point.find_first_of(',');
            double x = std::stod(point.substr(0, split_pos));
            double y = std::stod(point.substr(split_pos + 1));

            particles[particle].push_back(Point(x,y));
        }
    }

    // A vector of <timestamp #, segment_tree> pairs, sorted by timestamp.  No initial timestep.
    // Can optionally convert it to the actual timestamp, rather than iteration number if necessary
    std::vector<std::pair<int, SegmentTree>> trees;
    for (int timestep = 1; timestep < num_timesteps; timestep++) {
        trees.push_back(std::make_pair(timestep, generateSegmentTreeAtTimestep(particles, timestep)));
    }

    // TODO: Do something with the data we have now...
}