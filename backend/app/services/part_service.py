from fastapi import HTTPException
from app.repositories.part_repository import PartRepository
from app.models.part import Part

class PartService:
    def __init__(self, repo: PartRepository):
        self.repo = repo

    def calculate_price(self, part):
        if part.children:
            return sum(self.calculate_price(child) for child in part.children)
        
        return (part.price or 0) * (part.quantity or 1)

    def build_tree(self, part: Part):
        return {
            "id": part.id,
            "name": part.name,
            "price": part.price,
            "quantity": part.quantity,
            "total_price": self.calculate_price(part), 
            "parent_id": part.parent_id,
            "children": [self.build_tree(child) for child in part.children]
        }

    def get_tree(self):
        roots = self.repo.get_roots()
        return [self.build_tree(r) for r in roots]

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

        clean_data = {
            k: v for k, v in data.items()
            if k in allowed_fields
        }

        if "parent_id" in clean_data:
            new_parent_id = clean_data["parent_id"]

            if new_parent_id == part.id:
                raise HTTPException(400, "Cannot set parent to itself")

            if new_parent_id is not None:
                new_parent = self.repo.get_by_id(new_parent_id)

                if not new_parent:
                    raise HTTPException(400, "Parent not found")

                if self.is_descendant(part, new_parent_id):
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
    
    def is_descendant(self, node, target_id):
        if not node.children:
            return False

        for child in node.children:
            if child.id == target_id:
                return True
            if self.is_descendant(child, target_id):
                return True

        return False