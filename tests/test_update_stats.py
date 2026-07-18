from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.update_stats import (
    END_MARKER,
    START_MARKER,
    GitHubClient,
    Package,
    PackageStats,
    discover_packages,
    fetch_github_stats,
    paginated_total,
    render_contributor_count,
    render_stats,
    replace_stats_block,
    update_readme,
)


SAMPLE_README = f"""# Packages

## Package statistics

{START_MARKER}
{END_MARKER}

## Core packages

### Alpha - [GitHub](https://github.com/example/alpha), [Docs](https://example.com)

Description.

## Specialist packages

### Beta Tool - [GitHub](https://github.com/other/beta)

Description.
"""


class FakeClient(GitHubClient):
    def __init__(self) -> None:
        pass

    def get(self, path, query=None):
        if path.endswith("/commits"):
            if query and query.get("page") == "42":
                return (
                    [
                        {
                            "commit": {
                                "author": {
                                    "date": "2019-01-02T08:00:00Z"
                                }
                            }
                        }
                    ],
                    {},
                )
            return (
                [{"commit": {"committer": {"date": "2026-07-17T12:00:00Z"}}}],
                {
                    "link": (
                        '<https://api.github.com/repositories/1/commits?'
                        'sha=main&per_page=1&page=42>; rel="last"'
                    )
                },
            )
        if path.endswith("/contributors"):
            return (
                [{"login": "example"}],
                {
                    "link": (
                        '<https://api.github.com/repositories/1/contributors?'
                        'anon=1&per_page=1&page=7>; rel="last"'
                    )
                },
            )
        return {"default_branch": "main", "stargazers_count": 123}, {}


class UpdateStatsTests(unittest.TestCase):
    def test_discovers_packages_in_readme_order(self):
        self.assertEqual(
            discover_packages(SAMPLE_README),
            [
                Package("Alpha", "example/alpha"),
                Package("Beta Tool", "other/beta"),
            ],
        )

    def test_rejects_readme_without_packages(self):
        with self.assertRaisesRegex(ValueError, "No package"):
            discover_packages("# Empty")

    def test_parses_github_response_and_last_page(self):
        stats = fetch_github_stats(Package("Alpha", "example/alpha"), FakeClient())
        self.assertEqual(stats.stars, 123)
        self.assertEqual(stats.first_commit, "2019-01-02")
        self.assertEqual(stats.last_commit, "2026-07-17")
        self.assertEqual(stats.commits, 42)
        self.assertEqual(stats.contributors, 7)
        self.assertEqual(stats.default_branch, "main")

    def test_pagination_count_handles_unpaginated_and_empty_responses(self):
        self.assertEqual(paginated_total([{}], None), 1)
        self.assertEqual(paginated_total([], None), 0)

    def test_contributor_count_uses_thousands_separator(self):
        self.assertEqual(render_contributor_count(1939), "1,939")

    def test_renders_stable_markdown(self):
        rendered = render_stats(
            [
                PackageStats(
                    package=Package("Alpha", "example/alpha"),
                    stars=1234,
                    first_commit="2019-01-02",
                    last_commit="2026-07-17",
                    commits=42,
                    lines_of_code=9876,
                    contributors=7,
                )
            ],
            date(2026, 7, 18),
        )
        self.assertIn("_Last refreshed: **2026-07-18**_", rendered)
        self.assertIn(
            "| [Alpha](https://github.com/example/alpha) "
            "| 1,234 | 2019-01-02 | 2026-07-17 | 42 | 9,876 | 7 |",
            rendered,
        )

    def test_replaces_only_generated_block(self):
        generated = f"{START_MARKER}\nnew table\n{END_MARKER}"
        updated = replace_stats_block(SAMPLE_README, generated)
        self.assertIn(generated, updated)
        self.assertIn("## Alpha", updated)

    def test_rejects_missing_markers(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            replace_stats_block("# README", "generated")

    def test_update_is_noop_when_generated_content_matches(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "README.md"
            path.write_text(SAMPLE_README, encoding="utf-8")
            counter = lambda package, branch: 100
            client = FakeClient()

            self.assertTrue(
                update_readme(path, client, date(2026, 7, 18), counter)
            )
            first_update = path.read_text(encoding="utf-8")
            self.assertFalse(
                update_readme(path, client, date(2026, 7, 18), counter)
            )
            self.assertEqual(path.read_text(encoding="utf-8"), first_update)


if __name__ == "__main__":
    unittest.main()
