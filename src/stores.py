from dto import objects

global user_store
user_store: list[objects.User] = [
    objects.User(full_name="User 1", email="h.phung@goalist.co.jp", password="123456")
]

global projects_store
projects_store: list[objects.Project] = [
    objects.Project(id=1, project_name="Project A", project_overview="This is project A overview"),
    objects.Project(id=2, project_name="Project B", project_overview="This is project B overview"),
    objects.Project(id=3, project_name="Project C", project_overview="This is project C overview"),
]