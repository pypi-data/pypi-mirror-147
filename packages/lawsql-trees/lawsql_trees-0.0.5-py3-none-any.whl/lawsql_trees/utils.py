from dataclasses import dataclass, field
from email.policy import default
from typing import NoReturn


def set_tree_ids(nodes: list[dict], parent_id: str = "1") -> NoReturn:
    """Adds an string id to each deeply nested json whereby each string id is in the following format: "1.1". If node id "1.1" has child nodes, the first child node will be "1.1.1". The root of the tree will always be "1".

    Args:
        nodes (list[dict]): Each dict in the list may have `units` key
        parent_id (str): This is the parent of the node being evaluated

    Returns:
        NoReturn: This function updates the nodes in place since dicts are mutable.
    """
    for counter, node in enumerate(nodes, start=1):
        node["id"] = f"{parent_id}.{str(counter)}"
        if node.get("units", None):
            set_tree_ids(node["units"], node["id"])


def get_tree_node(nodes: list[dict], query_id: str) -> dict | None:
    """Return the first node matching the `query_id`, if it exists

    Args:
        nodes (list[dict]): The deeply nested json list
        query_id (str): The id previously set by `set_tree_ids()`

    Returns:
        dict | None: The first node matching the query_id or None
    """
    for node in nodes:
        if node["id"] == query_id:
            return node
        if units := node.get("units", None):
            if match := get_tree_node(units, query_id):
                return match


@dataclass
class Branch:
    """Create a subtree of the `tree` (list of dicts) based on the `path` (str)"""

    path: str
    tree: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.ids: str = self.partial_paths
        self.leaf: dict = get_tree_node(self.tree, self.path)
        self.units: list[dict] = [self.collected_nodes]
        self.citation, self.content = self.citation_and_content

    def __repr__(self) -> str:
        return self.path

    def __str__(self) -> str:
        return self.citation

    @property
    def partial_paths(self) -> list[str]:
        """With a string delimited by `.` e.g. "1.1.2.6", get a list of partial paths, excluding the first path: ["1.1", "1.1.2", "1.1.2.6"]"""
        points = self.path.split(".")
        paths = []
        for counter, point in enumerate(points):
            if counter == 0:  # exclude the first '1'
                paths.append(str(point))
                continue
            paths.append(f"{paths[-1]}.{str(point)}")
        return paths

    @property
    def collected_nodes(self) -> dict:
        """Based on the text identifier, extract the relevant parts of the tree."""
        self.ids.reverse()  # start with the lowest node
        target_node = None
        for node_id in self.ids:
            if node_id == "1":
                continue
            node_found = get_tree_node(self.tree, node_id)
            content_node = {}
            content_node["id"] = node_found.get("id", None)
            content_node["item"] = node_found.get("item", None)
            content_node["caption"] = node_found.get("caption", None)
            content_node["content"] = node_found.get("content", None)
            if not target_node:  # the lowest node becomes the target node
                target_node = content_node
            else:  # the target node is replaced, it becomes a child of the content_node
                content_node["units"] = [target_node]
                target_node = content_node
        return target_node

    @property
    def citation_and_content(self) -> tuple[str, str]:
        citation_arr = []
        content_arr = []

        def get_location(node: dict):
            return f"{node['item'] or ''}. {node['caption'] or ''}".strip()

        def extract(nodes: list[dict]):
            for node in nodes:
                l = get_location(node)
                citation_arr.append(f"{l.removesuffix('.')}")

                if content := node.get("content", None):
                    content_arr.append(f"{l} {content}")

                if node.get("units", None):
                    extract(node["units"])

        extract(self.units)
        citation_arr.reverse()
        return ", ".join(citation_arr), "<p>x x x</p>".join(content_arr)
