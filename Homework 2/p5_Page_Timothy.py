# Timothy Page
"""Weather Station Analyzer."""

import csv
import datetime
import sys
import unittest


def read_observations(filename: str) -> tuple[dict[str, list[tuple[datetime.datetime, float]]], list[tuple[int, str]]]:
    """Read weather data from a CSV file and return observations plus errors.

    Each valid line must contain the fields: station,date,temperature.
    Malformed rows, out-of-range temperatures, and duplicate station/date
    combinations are reported in the error list. Observations are grouped by
    station and sorted by date using datetime.datetime sorting.
    """
    observations: dict[str, list[tuple[datetime.datetime, float]]] = {}
    errors: list[tuple[int, str]] = []
    seen_dates: set[tuple[str, datetime.datetime]] = set()

    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        for line_number, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line:
                errors.append((line_number, "Malformed line: empty line."))
                continue

            try:
                row = next(csv.reader([line]))
            except csv.Error:
                errors.append((line_number, "Malformed line: invalid CSV syntax."))
                continue

            if len(row) != 3:
                errors.append((line_number, "Malformed line: expected 3 fields."))
                continue

            station, date_text, temperature_text = (value.strip() for value in row)
            if not station or not date_text or not temperature_text:
                errors.append((line_number, "Malformed line: missing station, date, or temperature."))
                continue

            try:
                parsed_date = datetime.datetime.strptime(date_text, "%I:%M:%S %p %m/%d/%Y")
            except ValueError:
                errors.append((line_number, f"Malformed date: {date_text}"))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, f"Invalid temperature: {temperature_text}"))
                continue

            if not -100.0 <= temperature <= 150.0:
                errors.append((line_number, f"Temperature out of range: {temperature_text}"))
                continue

            station_date_key = (station, parsed_date)
            if station_date_key in seen_dates:
                errors.append((line_number, f"Duplicate station/date combination: {station}, {date_text}"))
                continue

            seen_dates.add(station_date_key)
            observations.setdefault(station, []).append((parsed_date, temperature))

    for station_readings in observations.values():
        station_readings.sort(key=lambda item: item[0])

    return observations, errors


def station_statistics(observations: dict[str, list[tuple[datetime.datetime, float]]]) -> dict[str, dict[str, float]]:
    """Return minimum, maximum, and mean temperature for each station."""
    statistics: dict[str, dict[str, float]] = {}

    for station, readings in observations.items():
        temperatures = [temperature for _, temperature in readings]
        if not temperatures:
            continue

        statistics[station] = {
            "min": min(temperatures),
            "max": max(temperatures),
            "mean": sum(temperatures) / len(temperatures),
        }

    return statistics


def station_outliers(observations: dict[str, list[tuple[datetime.datetime, float]]]) -> dict[str, tuple[datetime.datetime, float, float]]:
    """Return stations whose latest temperature is above the station mean."""
    statistics = station_statistics(observations)

    return {
        station: (
            readings[-1][0],
            readings[-1][1],
            statistics[station]["mean"],
        )
        for station, readings in observations.items()
        if readings and readings[-1][1] > statistics[station]["mean"]
    }


def write_statistics(filename: str, statistics: dict[str, dict[str, float]]) -> None:
    """Write station statistics to a CSV file in sorted order with one decimal place."""
    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["station", "min", "max", "mean"])

        for station in sorted(statistics):
            station_stats = statistics[station]
            writer.writerow([
                station,
                f"{station_stats['min']:.1f}",
                f"{station_stats['max']:.1f}",
                f"{station_stats['mean']:.1f}",
            ])


def print_station_summary(station_name: str, data: dict[str, float]) -> None:
    """Display one station's minimum, maximum, and mean values."""
    print(
        f"{station_name}: min={data['min']:.1f}, "
        f"max={data['max']:.1f}, mean={data['mean']:.1f}"
    )


def print_outlier_summary(outliers: dict[str, tuple[datetime.datetime, float, float]]) -> None:
    """Display outlier stations and their latest reading details."""
    if not outliers:
        print("No outliers.")
        return

    for station in sorted(outliers):
        latest_date, latest_temperature, mean_value = outliers[station]
        print(
            f"{station}: latest={latest_date.strftime('%I:%M:%S %p %m/%d/%Y')}, "
            f"temperature={latest_temperature:.1f}, mean={mean_value:.1f}"
        )


def main() -> None:
    """Read weather data, print results, and write statistics to a file."""
    if len(sys.argv) != 3:
        print("Usage: python p5_Page_Timothy.py input_file.csv output_file.csv")
        return

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
    except FileNotFoundError:
        print(f"Error: file not found: {input_filename}")
        return
    except OSError as error:
        print(f"Error accessing file: {input_filename} - {error}")
        return

    if errors:
        for line_number, message in errors:
            print(f"Line {line_number}: {message}")

    statistics = station_statistics(observations)
    outliers = station_outliers(observations)

    if statistics:
        print("Station statistics:")
        for station in sorted(statistics):
            print_station_summary(station, statistics[station])
    else:
        print("Station statistics:")
        print("No valid observations.")

    print("\nOutliers:")
    print_outlier_summary(outliers)

    try:
        write_statistics(output_filename, statistics)
        print(f"\nStatistics written to {output_filename}")
    except OSError as error:
        print(f"Error writing file: {output_filename} - {error}")


class WeatherStationAnalyzerTests(unittest.TestCase):
    """Tests for the weather station analyzer."""

    def test_read_observations_multiple_stations_and_sorting(self) -> None:
        """Read and sort multiple stations by date."""
        with open("test_weather_1.csv", "w", encoding="utf-8", newline="") as file:
            file.write("Alpha,09:28:09 AM 04/20/2026,20.5\n")
            file.write("Bravo,01:15:00 PM 04/19/2026,-5.0\n")
            file.write("Alpha,09:00:00 AM 04/18/2026,15.0\n")

        try:
            observations, errors = read_observations("test_weather_1.csv")
            self.assertEqual(errors, [])
            self.assertEqual(observations["Alpha"][0][0], datetime.datetime(2026, 4, 18, 9, 0, 0))
            self.assertEqual(observations["Alpha"][1][1], 20.5)
            self.assertEqual(observations["Bravo"][0][1], -5.0)
        finally:
            import os
            if os.path.exists("test_weather_1.csv"):
                os.remove("test_weather_1.csv")

    def test_negative_temperatures_are_allowed(self) -> None:
        """Negative values remain valid within the allowed range."""
        with open("test_weather_2.csv", "w", encoding="utf-8", newline="") as file:
            file.write("North,09:00:00 AM 04/15/2026,-12.5\n")
            file.write("South,07:30:00 PM 04/15/2026,-100.0\n")

        try:
            observations, errors = read_observations("test_weather_2.csv")
            self.assertEqual(errors, [])
            self.assertEqual(observations["North"][0][1], -12.5)
            self.assertEqual(observations["South"][0][1], -100.0)
        finally:
            import os
            if os.path.exists("test_weather_2.csv"):
                os.remove("test_weather_2.csv")

    def test_duplicate_station_and_date_is_rejected(self) -> None:
        """Repeated stations on the same date should be rejected."""
        with open("test_weather_3.csv", "w", encoding="utf-8", newline="") as file:
            file.write("Central,09:00:00 AM 04/10/2026,10.0\n")
            file.write("Central,09:00:00 AM 04/10/2026,12.0\n")

        try:
            observations, errors = read_observations("test_weather_3.csv")
            self.assertEqual(len(observations["Central"]), 1)
            self.assertIn("Duplicate station/date combination", errors[0][1])
        finally:
            import os
            if os.path.exists("test_weather_3.csv"):
                os.remove("test_weather_3.csv")

    def test_temperature_outside_range_is_rejected(self) -> None:
        """Temperature values below -100 or above 150 are invalid."""
        with open("test_weather_4.csv", "w", encoding="utf-8", newline="") as file:
            file.write("West,11:11:11 AM 04/16/2026,150.1\n")
            file.write("East,09:00:00 AM 04/16/2026,-100.1\n")

        try:
            observations, errors = read_observations("test_weather_4.csv")
            self.assertEqual(observations, {})
            self.assertEqual(len(errors), 2)
            self.assertTrue(all("Temperature out of range" in message for _, message in errors))
        finally:
            import os
            if os.path.exists("test_weather_4.csv"):
                os.remove("test_weather_4.csv")

    def test_station_statistics_are_calculated_correctly(self) -> None:
        """Mean, min, and max should be computed from all valid readings."""
        observations = {
            "Alpha": [
                (datetime.datetime(2026, 4, 1, 9, 0, 0), 10.0),
                (datetime.datetime(2026, 4, 2, 9, 0, 0), 20.0),
                (datetime.datetime(2026, 4, 3, 9, 0, 0), 30.0),
            ],
            "Beta": [
                (datetime.datetime(2026, 4, 1, 9, 0, 0), -10.0),
                (datetime.datetime(2026, 4, 2, 9, 0, 0), 0.0),
            ],
        }

        statistics = station_statistics(observations)
        self.assertAlmostEqual(statistics["Alpha"]["min"], 10.0)
        self.assertAlmostEqual(statistics["Alpha"]["max"], 30.0)
        self.assertAlmostEqual(statistics["Alpha"]["mean"], 20.0)
        self.assertAlmostEqual(statistics["Beta"]["mean"], -5.0)

    def test_station_outliers_uses_latest_temperature_and_mean(self) -> None:
        """Only stations whose latest reading exceeds their average are outliers."""
        observations = {
            "A": [
                (datetime.datetime(2026, 4, 1, 9, 0, 0), 10.0),
                (datetime.datetime(2026, 4, 2, 9, 0, 0), 25.0),
            ],
            "B": [
                (datetime.datetime(2026, 4, 1, 9, 0, 0), 10.0),
                (datetime.datetime(2026, 4, 2, 9, 0, 0), 9.0),
            ],
        }

        outliers = station_outliers(observations)
        self.assertIn("A", outliers)
        self.assertNotIn("B", outliers)
        self.assertEqual(outliers["A"][0], datetime.datetime(2026, 4, 2, 9, 0, 0))
        self.assertAlmostEqual(outliers["A"][1], 25.0)
        self.assertAlmostEqual(outliers["A"][2], 17.5)

    def test_station_outliers_handles_zero_temperature(self) -> None:
        """A latest temperature of 0.0 should still be evaluated correctly."""
        observations = {
            "ZeroCase": [
                (datetime.datetime(2026, 4, 1, 9, 0, 0), -10.0),
                (datetime.datetime(2026, 4, 2, 9, 0, 0), 0.0),
            ],
            "BelowMean": [
                (datetime.datetime(2026, 4, 1, 9, 0, 0), -5.0),
                (datetime.datetime(2026, 4, 2, 9, 0, 0), -5.0),
            ],
        }

        outliers = station_outliers(observations)
        self.assertIn("ZeroCase", outliers)
        self.assertNotIn("BelowMean", outliers)
        self.assertAlmostEqual(outliers["ZeroCase"][1], 0.0)
        self.assertAlmostEqual(outliers["ZeroCase"][2], -5.0)

    def test_write_statistics_writes_sorted_csv_with_one_decimal(self) -> None:
        """Statistics output must be sorted and formatted with one decimal place."""
        statistics = {
            "Bravo": {"min": -5.0, "max": 12.0, "mean": 4.5},
            "Alpha": {"min": 0.0, "max": 10.0, "mean": 5.0},
        }

        output_name = "test_statistics_output.csv"
        try:
            write_statistics(output_name, statistics)
            with open(output_name, "r", encoding="utf-8", newline="") as file:
                rows = list(csv.reader(file))

            self.assertEqual(rows[0], ["station", "min", "max", "mean"])
            self.assertEqual(rows[1], ["Alpha", "0.0", "10.0", "5.0"])
            self.assertEqual(rows[2], ["Bravo", "-5.0", "12.0", "4.5"])
        finally:
            import os
            if os.path.exists(output_name):
                os.remove(output_name)

    def test_missing_input_file_raises_file_not_found(self) -> None:
        """A missing input file should raise FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            read_observations("file_does_not_exist.csv")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main()
    else:
        unittest.main()
