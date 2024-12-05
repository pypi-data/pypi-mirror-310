class File:
    """
    Represents a file with a name, content, and an optional emoji icon.
    """
    def __init__(self, name: str, content: str = "", emoji: str = "❓"):
        self.name = name
        self.content = content
        self.emoji = emoji

    def __repr__(self) -> str:
        return (
            f"  ↳ {self.emoji} {self.name}\n"
            f"      Content:\n"
            f"      ```\n"
            f"      {self.content}\n"
            f"      ```"
        )


class Directory:
    """
    Represents a directory containing files and/or subdirectories.
    """
    def __init__(self, name: str):
        self.name = name
        self.contents: list[File | Directory] = []

    def add_file(self, file: File) -> None:
        if isinstance(file, File):
            self.contents.append(file)
        else:
            raise TypeError("Only File objects can be added to a directory.")

    def add_directory(self, directory: 'Directory') -> None:
        if isinstance(directory, Directory):
            self.contents.append(directory)
        else:
            raise TypeError("Only Directory objects can be added as subdirectories.")

    def find_file(self, file_name: str) -> File | None:
        """
        Searches for a file in the directory by name and returns it.
        """
        for item in self.contents:
            if isinstance(item, File) and item.name == file_name:
                return item
        return None

    def __repr__(self, indent: int = 0) -> str:
        indent_str = "  " * indent
        representation = f"{indent_str}📁 {self.name}\n"
        for item in self.contents:
            if isinstance(item, Directory):
                representation += item.__repr__(indent + 1)
            else:
                representation += f"{item}\n"
        return representation

    def list_contents(self) -> str:
        """
        Provides a simple listing of the directory's contents by name.
        """
        representation = f"📁 {self.name} contains:\n"
        for item in self.contents:
            representation += f"  ↳ {item.name}\n"
        return representation


class Workspace:
    """
    Represents a virtual workspace with a root directory.
    """
    def __init__(self, name: str):
        self.root = Directory(name)

    def create_file(self, name: str, content: str = "", emoji: str = "🐍") -> None:
        """
        Creates a new file and adds it to the root directory.
        """
        new_file = File(name, content, emoji)
        self.root.add_file(new_file)

    def create_directory(self, name: str) -> None:
        """
        Creates a new directory and adds it to the root directory.
        """
        new_directory = Directory(name)
        self.root.add_directory(new_directory)

    def list_contents(self) -> str:
        """
        Lists all contents of the root directory.
        """
        return str(self.root)

    def list_directory_contents(self, directory_name: str) -> str:
        """
        Lists the contents of a specific subdirectory by name.
        """
        for item in self.root.contents:
            if isinstance(item, Directory) and item.name == directory_name:
                return item.list_contents()
        return f"Directory '{directory_name}' not found."

    def read_file_content(self, file_name: str) -> str:
        """
        Reads the content of a file by name in the root directory.
        """
        file = self.root.find_file(file_name)
        if file:
            return file.content
        return f"File '{file_name}' not found in the root directory."
