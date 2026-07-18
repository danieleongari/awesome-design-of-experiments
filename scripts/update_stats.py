#!/usr/bin/env python3
"""Refresh package repository statistics in README.md."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Callable, Mapping, Sequence


START_MARKER = "<!-- package-stats:start -->"
END_MARKER = "<!-- package-stats:end -->"
PACKAGE_HEADING = re.compile(
    r"^#{2,3}\s+(?P<name>.+?)\s+-\s+\[GitHub\]"
    r"\(https://github\.com/(?P<slug>[^/\s)]+/[^/\s)#?,]+?)(?:\.git)?\)"
    r"(?:,|$)",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Package:
    name: str
    slug: str


@dataclass(frozen=True)
class GitHubStats:
    stars: int
    last_commit: str
    commits: int
    default_branch: str


@dataclass(frozen=True)
class PackageStats:
    package: Package
    stars: int
    last_commit: str
    commits: int
    lines_of_code: int


class GitHubClient:
    """Minimal GitHub REST API client using only the Python standard library."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token

    def get(
        self, path: str, query: Mapping[str, str] | None = None
    ) -> tuple[object, dict[str, str]]:
        url = f"https://api.github.com{path}"
        if query:
            url = f"{url}?{urllib.parse.urlencode(query)}"

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-design-of-experiments-stats",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.load(response)
                response_headers = {
                    key.lower(): value for key, value in response.headers.items()
                }
                return payload, response_headers
        except urllib.error.HTTPError as error:
            message = error.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"GitHub API request failed ({error.code}) for {path}: {message}"
            ) from error


def discover_packages(readme: str) -> list[Package]:
    """Discover package display names and GitHub repositories from README headings."""
    packages = [
        Package(match.group("name").strip(), match.group("slug"))
        for match in PACKAGE_HEADING.finditer(readme)
    ]
    if not packages:
        raise ValueError("No package GitHub links were found in README headings")
    return packages


def total_commits(commits: Sequence[object], link_header: str | None) -> int:
    """Read a total count from GitHub's pagination Link header."""
    if not commits:
        return 0
    if not link_header:
        return len(commits)

    for link in link_header.split(","):
        if 'rel="last"' not in link:
            continue
        match = re.search(r"[?&]page=(\d+)", link)
        if match:
            return int(match.group(1))
    return len(commits)


def fetch_github_stats(package: Package, client: GitHubClient) -> GitHubStats:
    """Fetch repository metadata and latest default-branch commit information."""
    encoded_slug = "/".join(
        urllib.parse.quote(part, safe="") for part in package.slug.split("/")
    )
    repository, _ = client.get(f"/repos/{encoded_slug}")
    if not isinstance(repository, dict):
        raise RuntimeError(f"Unexpected repository response for {package.slug}")

    default_branch = str(repository["default_branch"])
    commits, headers = client.get(
        f"/repos/{encoded_slug}/commits",
        {"sha": default_branch, "per_page": "1"},
    )
    if not isinstance(commits, list) or not commits:
        raise RuntimeError(f"No commits found for {package.slug}")

    commit = commits[0]
    if not isinstance(commit, dict):
        raise RuntimeError(f"Unexpected commit response for {package.slug}")
    commit_details = commit.get("commit")
    if not isinstance(commit_details, dict):
        raise RuntimeError(f"Missing commit details for {package.slug}")
    identity = commit_details.get("committer") or commit_details.get("author")
    if not isinstance(identity, dict) or not identity.get("date"):
        raise RuntimeError(f"Missing latest commit date for {package.slug}")

    return GitHubStats(
        stars=int(repository["stargazers_count"]),
        last_commit=str(identity["date"])[:10],
        commits=total_commits(commits, headers.get("link")),
        default_branch=default_branch,
    )


def count_lines_of_code(package: Package, default_branch: str) -> int:
    """Shallow-clone a repository and count source lines with cloc."""
    with tempfile.TemporaryDirectory(prefix="doe-package-stats-") as temp_dir:
        checkout = Path(temp_dir) / "repository"
        subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                "--depth",
                "1",
                "--single-branch",
                "--branch",
                default_branch,
                f"https://github.com/{package.slug}.git",
                str(checkout),
            ],
            check=True,
        )
        result = subprocess.run(
            ["cloc", "--json", "--quiet", str(checkout)],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(result.stdout)
        summary = report.get("SUM", {})
        if "code" not in summary:
            raise RuntimeError(f"cloc returned no code count for {package.slug}")
        return int(summary["code"])


def collect_stats(
    packages: Sequence[Package],
    client: GitHubClient,
    line_counter: Callable[[Package, str], int] = count_lines_of_code,
) -> list[PackageStats]:
    """Collect all metrics while preserving README package order."""
    rows = []
    for package in packages:
        github = fetch_github_stats(package, client)
        rows.append(
            PackageStats(
                package=package,
                stars=github.stars,
                last_commit=github.last_commit,
                commits=github.commits,
                lines_of_code=line_counter(package, github.default_branch),
            )
        )
    return rows


def render_stats(rows: Sequence[PackageStats], refreshed_on: date) -> str:
    """Render the generated Markdown between the README markers."""
    lines = [
        START_MARKER,
        f"_Last refreshed: **{refreshed_on.isoformat()}**_",
        "",
        "| Package | Stars | Last commit | Commits | Lines of code |",
        "| --- | ---: | --- | ---: | ---: |",
    ]
    for row in rows:
        repository_url = f"https://github.com/{row.package.slug}"
        lines.append(
            f"| [{row.package.name}]({repository_url}) "
            f"| {row.stars:,} | {row.last_commit} | {row.commits:,} "
            f"| {row.lines_of_code:,} |"
        )
    lines.append(END_MARKER)
    return "\n".join(lines)


def replace_stats_block(readme: str, generated_block: str) -> str:
    """Replace exactly one generated statistics block."""
    if readme.count(START_MARKER) != 1 or readme.count(END_MARKER) != 1:
        raise ValueError("README must contain exactly one statistics marker pair")
    start = readme.index(START_MARKER)
    end = readme.index(END_MARKER, start) + len(END_MARKER)
    return f"{readme[:start]}{generated_block}{readme[end:]}"


def update_readme(
    readme_path: Path,
    client: GitHubClient,
    refreshed_on: date,
    line_counter: Callable[[Package, str], int] = count_lines_of_code,
) -> bool:
    """Refresh the README and return whether its contents changed."""
    original = readme_path.read_text(encoding="utf-8")
    packages = discover_packages(original)
    rows = collect_stats(packages, client, line_counter)
    updated = replace_stats_block(original, render_stats(rows, refreshed_on))
    if updated == original:
        return False
    readme_path.write_text(updated, encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--readme",
        type=Path,
        default=Path("README.md"),
        help="README file to update (default: README.md)",
    )
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=datetime.now(timezone.utc).date(),
        help="refresh date in YYYY-MM-DD format (default: current UTC date)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    changed = update_readme(args.readme, GitHubClient(token), args.date)
    print("README statistics updated" if changed else "README statistics unchanged")


if __name__ == "__main__":
    main()
