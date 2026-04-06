from datetime import datetime

_MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля",
    5: "мая", 6: "июня", 7: "июля", 8: "августа",
    9: "сентября", 10: "октября", 11: "ноября", 12: "декабря",
}
_MONTHS_BY = {
    1: "студзеня", 2: "лютага", 3: "сакавіка", 4: "красавіка",
    5: "траўня", 6: "чэрвеня", 7: "ліпеня", 8: "жніўня",
    9: "верасня", 10: "кастрычніка", 11: "лістапада", 12: "снежня",
}
_MONTHS_EN = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}


class News:
    def __init__(
        self,
        id=None,
        name=None,
        date=None,
        description=None,
        name_be=None,
        name_en=None,
        description_be=None,
        description_en=None,
        image_path=None,
    ):
        self.id = id
        self.name = name
        self.date = date
        self.description = description
        self.name_be = name_be
        self.name_en = name_en
        self.description_be = description_be
        self.description_en = description_en
        self.image_path = image_path

    def localized_name(self, lang: str = "ru") -> str:
        lang = (lang or "ru").lower()
        if lang == "be":
            return (self.name_be or self.name or "").strip() or (self.name or "")
        if lang == "en":
            return (self.name_en or self.name or "").strip() or (self.name or "")
        return (self.name or "").strip()

    def localized_description(self, lang: str = "ru") -> str:
        lang = (lang or "ru").lower()
        if lang == "be":
            return (self.description_be or self.description or "").strip() or (self.description or "")
        if lang == "en":
            return (self.description_en or self.description or "").strip() or (self.description or "")
        return (self.description or "").strip()

    def formatted_date(self, lang: str = "ru"):
        """Дата в формате, зависящем от языка интерфейса."""
        lang = (lang or "ru").lower()
        if self.date is None:
            return ""
        dt = self.date
        if isinstance(self.date, str):
            dt = None
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d.%m.%Y"):
                try:
                    dt = datetime.strptime(self.date, fmt)
                    break
                except ValueError:
                    continue
            if dt is None:
                return self.date
        if not isinstance(dt, datetime):
            return str(self.date)

        if lang == "be":
            months = _MONTHS_BY
            return f"{dt.day} {months.get(dt.month, '')} {dt.year}"
        if lang == "en":
            months = _MONTHS_EN
            return f"{months.get(dt.month, '')} {dt.day}, {dt.year}"
        months = _MONTHS_RU
        return f"{dt.day} {months.get(dt.month, '')} {dt.year}"

    @classmethod
    def from_dict(cls, data):
        date_value = data.get("date")
        if isinstance(date_value, str) and not isinstance(date_value, datetime):
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    date_value = datetime.strptime(date_value, fmt)
                    break
                except ValueError:
                    continue

        return cls(
            id=data.get("id"),
            name=data.get("name"),
            date=date_value,
            description=data.get("description"),
            name_be=data.get("name_be"),
            name_en=data.get("name_en"),
            description_be=data.get("description_be"),
            description_en=data.get("description_en"),
            image_path=data.get("image_path"),
        )
