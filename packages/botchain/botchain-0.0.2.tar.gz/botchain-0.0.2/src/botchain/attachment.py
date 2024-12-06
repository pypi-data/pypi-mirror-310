from dataclasses import dataclass


@dataclass
class Attachment:
    filename: str
    data: bytes

    def __str__(self):
        s = f"Attachment: {self.filename}"
        s += f"\nSize: {len(self.data)} bytes"

        return s
