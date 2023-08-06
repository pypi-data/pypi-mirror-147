from argparse import Namespace
from base64 import b64encode

from pybadges import badge
from clime_badges.args import mainArgs

def createBadge(
    leftText: str = "Hello",
    rightText: str = "World",
    link: str = "https://github.com/SoftwareSystemsLaboratory/",
    logo: str = "",
    leftColor: str = "maroon",
    rightColor: str = "gold",
) -> str:
    return badge(
        left_text=leftText,
        right_text=rightText,
        whole_link=link,
        logo=logo,
        left_color=leftColor,
        right_color=rightColor,
        embed_logo=True,
    )


def main() -> None:
    args: Namespace = mainArgs()

    if args.graph[-4::] != ".png":
        print("Invalid graph file extension. File must end in .png")
        quit(1)

    if args.output[-4::] != ".svg":
        print("Invalid output file extension. File must end in .svg")
        quit(2)

    base64EncodedStr: str
    with open(file=args.graph, mode="r", encoding="utf8") as file:
        byteStream: bytes = bytes(file.read(), "utf8")
        base64EncodedByteStream: bytes = b64encode(byteStream)
        base64EncodedStr: str = (
            "data:image/svg+xml;base64," + base64EncodedByteStream.decode("utf8")
        )
        file.close()

    badge: str = createBadge(
        leftText=args.left_text,
        rightText=args.right_text,
        link=args.link,
        logo=base64EncodedStr,
        leftColor=args.left_color,
        rightColor=args.right_color,
        title=args.title,
    )

    with open(file=args.output, mode="w") as svg:
        svg.write(badge)
        svg.close()


if __name__ == "__main__":
    main()
