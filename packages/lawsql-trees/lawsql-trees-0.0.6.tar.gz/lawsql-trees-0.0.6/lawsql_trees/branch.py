from copy import deepcopy
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

from .utils import get_tree_node


@dataclass
class Branch:
    """Create a subtree of the `tree` (list of dicts) based on the `path` (str).

    Assumes previous configuration through `utils.set_tree_ids()` to generate paths.

    The properties of this structure that can be used in lawsql are:

    1. `@units` - for structured data
    2. `@shorthand` - for the truncated headline consisting of citations
    3. `str(self)` - for the complete headline consisting of citations
    4. `@content` - for the complete content
    """

    path: str
    tree: list[dict] = field(default_factory=list)
    citation_texts: list[str] = field(default_factory=list)
    content_texts: list[str] = field(default_factory=list)

    def __post_init__(self):
        # finalize the list of ids
        self.ids: str = self.partial_paths  # use given path
        self.ids.reverse()  # start with the lowest node ("e.g. 1.1.5.4") vs. the highest one ("1")
        self.ids.pop()  # remove "1"

        self.units: list[dict] = [
            self.get_hierarchical_path_to_leaf_node(self.ids)
        ]

        self.leaf: dict = get_tree_node(self.tree, self.path)

        # set citation_texts and content_texts
        self.extract(self.units)
        self.citation_texts.reverse()
        self.shorthand = (
            f"{str(self)[:25]} {'...' if len(str(self)) >= 20 else ''}".strip()
        )
        self.content = self.converted_text

    def __repr__(self) -> str:
        return str(self.units)

    def __str__(self) -> str:
        return ", ".join(self.citation_texts)

    @property
    def partial_paths(self) -> list[str]:
        """With a string delimited by `.` e.g. "1.1.2.6", get a list of partial paths, excluding the first path: ["1.1", "1.1.2", "1.1.2.6"]"""
        points = self.path.split(".")
        paths = []
        for counter, point in enumerate(points):
            if counter == 0:  # set the first '1'
                paths.append(str(point))
                continue
            next_path = f"{paths[-1]}.{str(point)}"
            paths.append(next_path)  # attach most recent to next
        return paths

    def get_hierarchical_path_to_leaf_node(self, ids: list[str]) -> dict:
        """Based on the text identifier, extract the relevant parts of the tree."""
        origin = None
        for id in ids:
            latest_node = deepcopy(get_tree_node(self.tree, id))
            if not origin:  # the lowest node becomes the target node
                origin = latest_node
            else:  # the origin node is replaced, it becomes a child of the latest node
                latest_node["units"] = [origin]
                origin = latest_node  # move the latest node as new origin
        return origin

    def extract(self, nodes: list[dict]):
        """Recursive function to set the citation_texts and content_texts from the hierarhical nodes"""

        def can_ignore(text):
            return "Paragraph" in text or "Proviso" in text or "Clause" in text

        for node in nodes:
            l = f"{node.get('item', '')}. {node.get('caption', '')}".strip()
            self.citation_texts.append(f"{l.removesuffix('.')}")

            if content := node.get("content", None):
                if can_ignore(node.get("item", "")):
                    self.content_texts.append(f"{content}")
                else:
                    self.content_texts.append(f"{l} {content}")

            if node.get("units", None):
                self.extract(node["units"])

    @property
    def converted_text(self):
        html = "".join(self.content_texts)
        soup = BeautifulSoup(html, "html5lib")
        text = soup.get_text(strip=True, separator=" ")
        return text
