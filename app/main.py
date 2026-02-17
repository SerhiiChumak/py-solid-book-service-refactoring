import json
import xml.etree.ElementTree as ElementTree
from typing import Optional, List, Tuple


class Book:
    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content


class DisplayBook:
    def format(self, book: Book, mode: str) -> str:
        if mode == "console":
            return book.content
        elif mode == "reverse":
            return book.content[::-1]
        else:
            raise ValueError(f"Unknown display type: {mode}")


class PrintBook:
    def __init__(self, display_service: DisplayBook) -> None:
        self.display_service = display_service

    def print_book(self, book: Book, mode: str) -> None:
        formatted_content = self.display_service.format(book, mode)
        print(f"--- Printing Book: {book.title} ({mode} mode) ---")
        print(formatted_content)


class BookSerializer:
    def __init__(self, book: Book) -> None:
        self.book = book

    def to_json(self) -> str:
        return json.dumps(
            {"title": self.book.title,
             "content": self.book.content},
            ensure_ascii=False
        )

    def to_xml(self) -> str:
        root = ElementTree.Element("book")
        ElementTree.SubElement(root, "title").text = self.book.title
        ElementTree.SubElement(root, "content").text = self.book.content
        return ElementTree.tostring(root, encoding="unicode")

    def serialize(self, format_type: str) -> str:
        formats = {
            "json": self.to_json,
            "xml": self.to_xml
        }
        if format_type not in formats:
            raise ValueError(f"Unknown serialize type: {format_type}")
        return formats[format_type]()


class BookManager:
    def run(
            self,
            book: Book,
            commands: List[Tuple[str, str]]
    ) -> Optional[str]:
        display_service = DisplayBook()
        printer = PrintBook(display_service)
        serializer = BookSerializer(book)

        last_result = None

        for cmd, arg in commands:
            if cmd == "display" or cmd == "print":
                printer.print_book(book, arg)
            elif cmd == "serialize":
                last_result = serializer.serialize(arg)

        return last_result
