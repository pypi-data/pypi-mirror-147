from argparse import ArgumentParser, Namespace

name: str = "CLIME"
authors: list = ["Nicholas M. Synovic", "George K. Thiruvathukal"]


def mainArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Metric Badge Creator",
        description="A tool to create a badge from a metric's graph",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "-g",
        "--graph",
        required=True,
        type=str,
        help="The graph SVG file to be the badge logo",
    )
    parser.add_argument(
        "-lc",
        "--left-color",
        required=True,
        type=str,
        help="Left side color",
    )
    parser.add_argument(
        "-lt",
        "--left-text",
        required=True,
        type=str,
        help="Text to go on the left side of the badge",
    )
    parser.add_argument(
        "-u",
        "--link",
        required=False,
        type=str,
        help='Link to a specific URL that will open when the badge is clicked/ DEFAULT: ""',
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        type=str,
        help='The output filename of the badge. NOTE: Must end in .svg. DEFAULT: "badge.svg"',
        default="badge.svg"
    )
    parser.add_argument(
        "-rt",
        "--right-text",
        required=False,
        type=str,
        help='Text to go on the right side of the badge. DEFAULT ""',
    )
    parser.add_argument(
        "-rc"
        "--right-color",
        required=True,
        type=str,
        help="Right side color",
    )

    return parser.parse_args()
