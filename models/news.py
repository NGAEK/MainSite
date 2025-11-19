from datetime import datetime


class News:
    def __init__(self, id=None, name=None, date=None, description=None, image_path=None):
        self.id = id
        self.name = name
        self.date = date
        self.description = description
        self.image_path = image_path
    
    def formatted_date(self):
        """Возвращает отформатированную дату"""
        if self.date is None:
            return ""
        if isinstance(self.date, datetime):
            # Форматируем дату на русском языке
            months = {
                1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                5: "мая", 6: "июня", 7: "июля", 8: "августа",
                9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
            }
            return f"{self.date.day} {months.get(self.date.month, '')} {self.date.year}"
        elif isinstance(self.date, str):
            try:
                # Пробуем разные форматы
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d.%m.%Y"]:
                    try:
                        dt = datetime.strptime(self.date, fmt)
                        months = {
                            1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                            5: "мая", 6: "июня", 7: "июля", 8: "августа",
                            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
                        }
                        return f"{dt.day} {months.get(dt.month, '')} {dt.year}"
                    except:
                        continue
                return self.date
            except:
                return self.date
        return str(self.date)
    
    @classmethod
    def from_dict(cls, data):
        """Создает объект News из словаря"""
        date_value = data.get('date')
        # Если дата пришла как строка в формате YYYY-MM-DD, конвертируем в datetime
        if isinstance(date_value, str) and not isinstance(date_value, datetime):
            try:
                # Пробуем разные форматы
                for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                    try:
                        date_value = datetime.strptime(date_value, fmt)
                        break
                    except ValueError:
                        continue
            except:
                pass
        
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            date=date_value,
            description=data.get('description'),
            image_path=data.get('image_path')
        )

