import datetime

from bs4 import BeautifulSoup
from markdown import markdown
from telethon.tl.tlobject import TLObject
from telethon.tl.types import MessageEntityPre
from telethon.utils import add_surrogate

import pyAyiin

class Format:
    async def paste_message(self: "pyAyiin.pyAyiin", text, pastetype="p", extension=None, markdown=True):
        if markdown:
            text = self.md_to_text(text)
        response = await self.pastetext(text, pastetype, extension)
        if "url" in response:
            return response["url"]
        return "Error while pasting text to site"


    def md_to_text(self: "pyAyiin.pyAyiin", md):
        html = markdown(md)
        soup = BeautifulSoup(html, features="html.parser")
        return soup.get_text()


    def mentionuser(self: "pyAyiin.pyAyiin", name, userid):
        return f"[{name}](tg://user?id={userid})"


    def htmlmentionuser(self: "pyAyiin.pyAyiin", name, userid):
        return f"<a href='tg://user?id={userid}'>{name}</a>"


    # kanged from uniborg @spechide
    # https://github.com/SpEcHiDe/UniBorg/blob/d8b852ee9c29315a53fb27055e54df90d0197f0b/uniborg/utils.py#L250


    def reformattext(self: "pyAyiin.pyAyiin", text):
        return text.replace(
            "~",
            "").replace(
            "_",
            "").replace(
                "*",
                "").replace(
                    "`",
            "")


    def replacetext(self: "pyAyiin.pyAyiin", text):
        return (
            text.replace(
                '"',
                "",
            )
            .replace(
                "\\r",
                "",
            )
            .replace(
                "\\n",
                "",
            )
            .replace(
                "\\",
                "",
            )
        )


    def parse_pre(self: "pyAyiin.pyAyiin", text):
        text = text.strip()
        return (
            text, [
                MessageEntityPre(
                    offset=0, length=len(
                        add_surrogate(text)), language="")], )


    def yaml_format(self: "pyAyiin.pyAyiin", obj: float, indent=0, max_str_len=256, max_byte_len=64):
        # sourcery no-metrics
        """
        Pretty formats the given object as a YAML string which is returned.
        (based on TLObject.pretty_format)
        """
        result = []
        if isinstance(obj, TLObject):
            obj = obj.to_dict()

        if isinstance(obj, dict):
            if not obj:
                return "dict:"
            items = obj.items()
            has_items = len(items) > 1
            has_multiple_items = len(items) > 2
            result.append(obj.get("_", "dict") + (":" if has_items else ""))
            if has_multiple_items:
                result.append("\n")
                indent += 2
            for k, v in items:
                if k == "_" or v is None:
                    continue
                formatted = self.yaml_format(v, indent)
                if not formatted.strip():
                    continue
                result.extend(
                    (" " * (indent if has_multiple_items else 1), f"{k}:"))
                if not formatted[0].isspace():
                    result.append(" ")
                result.extend((f"{formatted}", "\n"))
            if has_items:
                result.pop()
            if has_multiple_items:
                indent -= 2
        elif isinstance(obj, str):
            # truncate long strings and display elipsis
            result = repr(obj[:max_str_len])
            if len(obj) > max_str_len:
                result += "…"
            return result
        elif isinstance(obj, bytes):
            # repr() bytes if it's printable, hex like "FF EE BB" otherwise
            if all(0x20 <= c < 0x7F for c in obj):
                return repr(obj)
            return "<…>" if len(obj) > max_byte_len else " ".join(
                f"{b:02X}" for b in obj)
        elif isinstance(obj, datetime.datetime):
            # ISO-8601 without timezone offset (telethon dates are always UTC)
            return datetime.datetime.fromtimestamp(obj).strftime("%Y-%m-%d %H:%M:%S")
        elif hasattr(obj, "__iter__"):
            # display iterables one after another at the base indentation level
            result.append("\n")
            indent += 2
            for x in obj:
                result.append(f"{' ' * indent}- {self.yaml_format(x, indent + 2)}")
                result.append("\n")
            result.pop()
            indent -= 2
        else:
            return repr(obj)

        return "".join(result)
