# Timothy Page -  Problem 4
import csv


def load_rated(filename: str) -> set:
    """Return the title and year of each top-rated movie."""
    with open(filename, "r", encoding="utf-8-sig") as file:
        return {
            (row["Title"], row["Year"])
            for row in csv.DictReader(file)
        }


def load_grossing(filename: str) -> dict:
    """Return each top-grossing movie and its box office total."""
    with open(filename, "r", encoding="utf-8-sig") as file:
        return {
            (row["Title"], row["Year"]): int(row["USA Box Office"])
            for row in csv.DictReader(file)
        }


def load_casts(filename: str) -> list:
    """Return movie titles, years, directors, and actors."""
    with open(filename, "r", encoding="utf-8") as file:
        return [
            (row[0], row[1], row[2], row[3:])
            for row in csv.reader(file)
        ]


def display_top_collaborations(rated_file: str, casts_file: str,
                               limit: int = 10) -> None:
    """Display directors and actors with the most collaborations."""
    rated = load_rated(rated_file)
    counts = {}

    for title, year, director, actors in load_casts(casts_file):
        if (title, year) in rated:
            for actor in actors:
                key = (director, actor)
                counts[key] = counts.get(key, 0) + 1

    ranking = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    print("Part A - Top Collaborations")
    for rank, ((director, actor), count) in enumerate(ranking[:limit], 1):
        print(rank, director, "-", actor, "-", count)


def display_top_actors(grossing_file: str, casts_file: str,
                       limit: int = 10) -> None:
    """Display actors ranked by total box office money."""
    grossing = load_grossing(grossing_file)
    totals = {}

    for title, year, director, actors in load_casts(casts_file):
        if (title, year) in grossing:
            for actor in actors:
                totals[actor] = totals.get(actor, 0) + grossing[(title, year)]

    ranking = sorted(totals.items(), key=lambda item: item[1], reverse=True)

    print("\nPart B - Top Actors")
    for rank, (actor, total) in enumerate(ranking[:limit], 1):
        print(rank, actor, "-", total)


def main() -> None:
    """Test Parts A and B."""
    print("Timothy Page - Problem 4\n")

    display_top_collaborations(
        "imdb-top-rated.csv",
        "imdb-top-casts.csv",
        10
    )

    display_top_actors(
        "imdb-top-grossing.csv",
        "imdb-top-casts.csv",
        10
    )


if __name__ == "__main__":
    main()