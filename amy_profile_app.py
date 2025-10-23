"""Command-line application for generating a profile for Amy.

This module provides a small interactive experience to collect basic
information about Amy and save it to a JSON file. The collected data is
stored in a :class:`Profile` dataclass to make further processing easy.

Example usage::

    python amy_profile_app.py

By default, the script asks a series of questions and saves the resulting
profile in ``amy_profile.json``. Use ``--output`` to change the destination
file and ``--use-defaults`` to skip the interactive prompts.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, List


@dataclass
class Profile:
    """Dataclass representing Amy's profile."""

    name: str
    age: int
    pronouns: str
    occupation: str
    bio: str
    interests: List[str] = field(default_factory=list)
    contact_email: str = ""

    def validate(self) -> None:
        """Validate the profile fields.

        Raises:
            ValueError: If any of the fields contain invalid data.
        """

        if not self.name.strip():
            raise ValueError("Name must not be empty.")
        if self.age < 0:
            raise ValueError("Age must be a non-negative integer.")
        if not self.contact_email or "@" not in self.contact_email:
            raise ValueError("A valid contact email address is required.")

    def to_json(self) -> str:
        """Return the profile serialized as a JSON string."""

        return json.dumps(asdict(self), indent=2, ensure_ascii=False)


DEFAULT_PROFILE = Profile(
    name="Amy Johnson",
    age=28,
    pronouns="she/her",
    occupation="UX Designer",
    bio=(
        "Amy is a curious creative who loves designing meaningful "
        "experiences. She combines empathy with data to craft "
        "accessible digital products."
    ),
    interests=["Design Thinking", "Photography", "Travel", "Coffee"],
    contact_email="amy.johnson@example.com",
)


def prompt(prompt_text: str, default: str) -> str:
    """Prompt the user for input with a default value."""

    response = input(f"{prompt_text} [{default}]: ").strip()
    return response or default


def prompt_interests(default: Iterable[str]) -> List[str]:
    """Prompt the user for a comma-separated list of interests."""

    default_display = ", ".join(default)
    response = input(
        "Interests (comma separated)"
        f" [{default_display}]: "
    ).strip()
    if not response:
        return list(default)
    interests = [interest.strip() for interest in response.split(",")]
    return [interest for interest in interests if interest]


def build_profile(use_defaults: bool = False) -> Profile:
    """Collect profile information from the user."""

    if use_defaults:
        return DEFAULT_PROFILE

    name = prompt("Name", DEFAULT_PROFILE.name)
    while True:
        age_value = prompt("Age", str(DEFAULT_PROFILE.age))
        try:
            age = int(age_value)
            if age < 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a non-negative integer for age.")

    pronouns = prompt("Pronouns", DEFAULT_PROFILE.pronouns)
    occupation = prompt("Occupation", DEFAULT_PROFILE.occupation)
    bio = prompt("Short Bio", DEFAULT_PROFILE.bio)
    interests = prompt_interests(DEFAULT_PROFILE.interests)

    while True:
        contact_email = prompt("Contact Email", DEFAULT_PROFILE.contact_email)
        if "@" in contact_email and "." in contact_email.split("@")[-1]:
            break
        print("Please enter a valid email address.")

    profile = Profile(
        name=name,
        age=age,
        pronouns=pronouns,
        occupation=occupation,
        bio=bio,
        interests=interests,
        contact_email=contact_email,
    )
    profile.validate()
    return profile


def save_profile(profile: Profile, output_path: Path) -> None:
    """Save the profile to the specified path as JSON."""

    output_path.write_text(profile.to_json(), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(description="Create a profile for Amy.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("amy_profile.json"),
        help="Destination file to save the profile (default: amy_profile.json)",
    )
    parser.add_argument(
        "--use-defaults",
        action="store_true",
        help="Skip prompts and use the default profile values.",
    )
    return parser.parse_args()


def main() -> None:
    """Entry point for the command-line application."""

    args = parse_args()
    profile = build_profile(use_defaults=args.use_defaults)
    save_profile(profile, args.output)
    print(f"Profile for {profile.name} saved to {args.output.resolve()}.")


if __name__ == "__main__":
    main()
