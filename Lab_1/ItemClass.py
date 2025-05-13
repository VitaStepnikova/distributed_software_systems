class Item:
    def __init__(self, id, name, description, tags, metadata, history):
        self.id = id
        self.name = name
        self.description = description
        self.tags = tags
        self.metadata = metadata
        self.history = history

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "tags": self.tags,
            "metadata": self.metadata,
            "history": self.history,
        }


