course_data = {
    "name": "Имя курса",
    "modules": [
        {
            "name": "Модуль 1",
            "id": 1,
            "lections": [
                {"name": "Лекция 1", "id": 1, "path": "path/to/lection1"},
                {"name": "Лекция 2", "id": 2, "path": "path/to/lection2"},
                {"name": "Лекция 3", "id": 3, "path": "path/to/lection3"},
                {"name": "Лекция 4", "id": 4, "path": "path/to/lection4"},
                {"name": "Лекция 5", "id": 5, "path": "path/to/lection5"},
                {"name": "Лекция 6", "id": 6, "path": "path/to/lection6"},
                {"name": "Лекция 7", "id": 7, "path": "path/to/lection7"},
            ]
        },
        {
            "name": "Модуль 2",
            "id": 2,
            "lections": [
                {"name": "Лекция 1", "id": 1, "path": "path/to/lection1"},
                {"name": "Лекция 2", "id": 2, "path": "path/to/lection2"},
                {"name": "Лекция 3", "id": 3, "path": "path/to/lection3"},
                {"name": "Лекция 4", "id": 4, "path": "path/to/lection4"},
                {"name": "Лекция 5", "id": 5, "path": "path/to/lection5"},
                {"name": "Лекция 6", "id": 6, "path": "path/to/lection6"},
                {"name": "Лекция 7", "id": 7, "path": "path/to/lection7"},
            ]
        },
        {
            "name": "Модуль 3",
            "id": 3,
            "lections": [
                {"name": "Лекция 1", "id": 1, "path": "path/to/lection1"},
                {"name": "Лекция 2", "id": 2, "path": "path/to/lection2"},
                {"name": "Лекция 3", "id": 3, "path": "path/to/lection3"},
                {"name": "Лекция 4", "id": 4, "path": "path/to/lection4"},
                {"name": "Лекция 5", "id": 5, "path": "path/to/lection5"},
                {"name": "Лекция 6", "id": 6, "path": "path/to/lection6"},
                {"name": "Лекция 7", "id": 7, "path": "path/to/lection7"},
            ]
        }
    ]
}
def get_module_by_id(module_id: int) -> dict | None:
    for module in course_data.get("modules", []):
        if module.get("id") == module_id:
            return module
    return None

def get_lection_by_id(module_id: int, lection_id: int) -> dict | None:
    module = get_module_by_id(module_id)
    if not module:
        return None
    for lection in module.get("lections", []):
        if lection.get("id") == lection_id:
            return lection
    return None