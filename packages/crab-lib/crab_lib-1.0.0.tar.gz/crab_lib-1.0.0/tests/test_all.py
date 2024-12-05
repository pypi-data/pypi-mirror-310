import unittest
from tempfile import NamedTemporaryFile
import os

# Import functions from crab-lib
from crab_lib.io import load_csv, save_csv
from crab_lib.preprocessing import clean_data, filter_data, standardize_comments
from crab_lib.analysis import calculate_distances, find_clusters, summarize_data
from crab_lib.visualization import plot_points, plot_clusters, create_heatmap
from crab_lib.utils import convert_coordinates, calculate_bearing, is_within_bounds


class TestCrabLib(unittest.TestCase):
    def setUp(self):
        # Sample data for testing
        self.sample_data = [
            {'x': '25.774', 'y': '-80.19', 'comment': 'hotspot'},
            {'x': '27.345', 'y': '-82.567', 'comment': 'fishing ground'},
            {'x': '25.774', 'y': '-80.19', 'comment': 'hotspot'}  # Duplicate
        ]
        self.sample_csv = "x,y,comment\n25.774,-80.19,hotspot\n27.345,-82.567,fishing ground\n"

    # ---- IO Tests ----
    def test_load_csv(self):
        with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(self.sample_csv)
            temp_file_path = temp_file.name

        data = load_csv(temp_file_path)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['x'], '25.774')
        os.remove(temp_file_path)

    def test_save_csv(self):
        with NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
            temp_file_path = temp_file.name
            save_csv(temp_file_path, self.sample_data)

        with open(temp_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        self.assertIn("25.774,-80.19,hotspot", content)
        os.remove(temp_file_path)

    # ---- Preprocessing Tests ----
    def test_clean_data(self):
        cleaned_data = clean_data(self.sample_data)
        self.assertEqual(len(cleaned_data), 2)

    def test_filter_data(self):
        filtered_data = filter_data(self.sample_data, 'hotspot')
        self.assertEqual(len(filtered_data), 2)

    def test_standardize_comments(self):
        standardized_data = standardize_comments(self.sample_data)
        self.assertEqual(standardized_data[0]['comment'], 'Hotspot')

    # ---- Analysis Tests ----
    def test_calculate_distances(self):
        distances = calculate_distances(self.sample_data)
        self.assertTrue(len(distances) > 0)

    def test_find_clusters(self):
        clusters = find_clusters(self.sample_data, radius=300)
        self.assertEqual(len(clusters), 1)

    def test_summarize_data(self):
        summary = summarize_data(self.sample_data)
        self.assertIn('total_points', summary)

    # ---- Visualization Tests (Mocked) ----
    def test_plot_points(self):
        # Mocking to ensure it doesn't actually render plots
        try:
            plot_points(self.sample_data)
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_plot_clusters(self):
        clusters = find_clusters(self.sample_data, radius=300)
        try:
            plot_clusters(clusters)
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_create_heatmap(self):
        try:
            create_heatmap(self.sample_data)
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    # ---- Utils Tests ----
    def test_convert_coordinates(self):
        dms = "25°46'26.5\"N"
        decimal = convert_coordinates(dms)
        self.assertAlmostEqual(decimal, 25.77375, places=5)

    def test_calculate_bearing(self):
        coord1 = (25.774, -80.19)
        coord2 = (27.345, -82.567)
        bearing = calculate_bearing(coord1, coord2)
        self.assertIsInstance(bearing, float)

    def test_is_within_bounds(self):
        coord = (25.774, -80.19)
        bounds = (25.0, 26.0, -81.0, -79.0)
        self.assertTrue(is_within_bounds(coord, bounds))


if __name__ == "__main__":
    unittest.main()
