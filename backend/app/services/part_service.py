from fastapi import HTTPException
from app.repositories.part_repository import PartRepository


class PartService:
    def __init__(self, repo: PartRepository):
        self.repo = repo

    def get_tree(self):
        parts = self.repo.get_all()

        parts_map = {
            p.id: {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity,
                "parent_id": p.parent_id,
                "children": []
            }
            for p in parts
        }

        tree = []

        for part in parts_map.values():
            if part["parent_id"]:
                parent = parts_map.get(part["parent_id"])
                if parent:
                    parent["children"].append(part)
            else:
                tree.append(part)

        return [self.build_tree(p) for p in tree]

    def build_tree(self, part):
        return {
            "id": part["id"],
            "name": part["name"],
            "price": part["price"],
            "quantity": part["quantity"],
            "parent_id": part["parent_id"],
            "total_price": self.calculate_price(part),
            "children": [self.build_tree(child) for child in part["children"]],
        }

    def calculate_price(self, part):
        if part["children"]:
            return sum(self.calculate_price(child) for child in part["children"])
        return (part["price"] or 0) * (part["quantity"] or 1)


    def create(self, data):
        self.validate(data)
        return self.repo.create(data)

    def delete(self, part_id):
        part = self.repo.get_by_id(part_id)
        if not part:
            return False
        self.repo.delete(part_id)
        return True

    def update(self, part_id, data):
        part = self.repo.get_by_id(part_id)

        if not part:
            raise HTTPException(404, "Part not found")

        allowed_fields = {"name", "price", "quantity", "parent_id"}
        clean_data = {k: v for k, v in data.items() if k in allowed_fields}

        if "parent_id" in clean_data:
            new_parent_id = clean_data["parent_id"]

            if new_parent_id == part.id:
                raise HTTPException(400, "Cannot set parent to itself")

            if new_parent_id is not None:
                new_parent = self.repo.get_by_id(new_parent_id)

                if not new_parent:
                    raise HTTPException(400, "Parent not found")

                tree = self.get_tree()
                if self.is_descendant(tree, part_id, new_parent_id):
                    raise HTTPException(
                        400,
                        "Cannot move node into its own subtree"
                    )

        return self.repo.update(part_id, clean_data)


    def validate(self, data):
        if data.get("quantity", 1) <= 0:
            raise HTTPException(400, "Quantity must be > 0")

        if data.get("price") is not None and data["price"] < 0:
            raise HTTPException(400, "Price must be >= 0")

        parent_id = data.get("parent_id")

        if parent_id is not None:
            parent = self.repo.get_by_id(parent_id)
            if not parent:
                raise HTTPException(400, "Parent not found")


    def is_descendant(self, tree, node_id, target_id):
        def find(node):
            if node["id"] == node_id:
                return node
            for child in node["children"]:
                res = find(child)
                if res:
                    return res
            return None

        def contains(node, target):
            if node["id"] == target:
                return True
            return any(contains(c, target) for c in node["children"])

        for root in tree:
            node = find(root)
            if node:
                return contains(node, target_id)

        return False