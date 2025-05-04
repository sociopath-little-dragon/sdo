import inspect
from db import *
import db  # Замени на имя твоего файла (без .py)


def show_db_func_list():
    # Получаем словарь всех имен в модуле your_module_name и их объектов
    module_names = inspect.getmembers(db)

    # Фильтруем только те объекты, которые являются функциями
    functions_list = [name for name, obj in module_names if inspect.isfunction(obj)]

    for i in range(len(functions_list)):
        if i % 5 == 0:
            print()
        print(functions_list[i], end='   ')

def seed_data():
    # test_db.py

    # 1) Пересоздаём БД
    delete_tables()
    create_tables()

    # 2) Добавляем факультет
    with Session() as session:
        it_faculty = Faculty(name="Информационных технологий")
        session.add(it_faculty)
        session.commit()
        fac_id = it_faculty.id

    # 3) Создаём две группы
    with Session() as session:
        g1 = Group(name="231-333", faculty=fac_id)
        g2 = Group(name="231-334", faculty=fac_id)
        session.add_all([g1, g2])
        session.commit()
        gid1, gid2 = g1.id, g2.id

    # 4) Добавляем студентов
    students = [
        ("ivan_petrov", "pass1", "Иван", "Петров", "Иванович", gid1),
        ("anna_smirnova", "pass2", "Анна", "Смирнова", "Петровна", gid1),
        ("oleg_kuznetsov", "pass3", "Олег", "Кузнецов", "Алексеевич", gid2),
        ("elena_volkova", "pass4", "Елена", "Волкова", "Сергеевна", gid2),
    ]
    with Session() as session:
        for username, pwd, fn, ln, mn, grp in students:
            u = User(
                username=username,
                password=pwd,
                first_name=fn,
                last_name=ln,
                middle_name=mn,
                roleType="student",
                form_education="Бюджет",
                studyGroup=grp
            )
            session.add(u)
        session.commit()

    # 5) Создаём дисциплины и привязываем к группам
    subjects = [
        "Объектно-ориентированное программирование",
        "Базы данных",
        "Системы управления разработкой программного обеспечения",
        "Иностранный язык",
    ]
    for name in subjects:
        add_subject(name)  # :contentReference[oaicite:20]{index=20}:contentReference[oaicite:21]{index=21}

    # Получим ID всех дисциплин для удобства
    subj_map = {s.name: s.id for s in get_subjects()}

    # Назначаем предметы группам
    reg_group_in_subject(gid1, "Объектно-ориентированное программирование")
    reg_group_in_subject(gid1, "Базы данных")
    reg_group_in_subject(gid2, "Системы управления разработкой программного обеспечения")
    reg_group_in_subject(gid2, "Иностранный язык")

    # 6) Тестируем функции и печатаем результаты

    print("Группы факультета ИТ:", get_groups_by_faculty(fac_id))
    # → [(231-333), (231-334)] :contentReference[oaicite:22]{index=22}:contentReference[oaicite:23]{index=23}

    print("Студенты в группе 231-333:", get_users_by_group(gid1))
    print("Студенты в группе 231-334:", get_users_by_group(gid2))

    print("Дисциплины для ivan_petrov:", get_user_subjects("ivan_petrov"))

    # Проверим, зачислена ли Анна на «Базы данных»
    bd_id = subj_map["Базы данных"]
    print("Анна зачислена на БД?", is_user_enrolled_in_subject("anna_smirnova", bd_id))

    # Кто учится на «Иностранный язык»
    iy_id = subj_map["Иностранный язык"]
    print("Пользователи по предмету «Иностранный язык»:", get_users_by_subject(iy_id))

    # Задачи: пока мы не добавляли таски, список будет пуст
    print("Статусы заданий у ivan_petrov:", get_student_tasks_with_status(
        next(u.id for u in Session().query(User).filter_by(username="ivan_petrov"))
    ))


def test2():
    delete_tables()
    create_tables()

    # 2) Добавляем факультет
    with Session() as session:
        it_faculty = Faculty(name="Информационных технологий")
        session.add(it_faculty)
        session.commit()
        fac_id = it_faculty.id

    # 3) Создаём две группы
    with Session() as session:
        g1 = Group(name="231-333", faculty=fac_id)
        g2 = Group(name="231-334", faculty=fac_id)
        session.add_all([g1, g2])
        session.commit()
        gid1, gid2 = g1.id, g2.id

    # 4) Добавляем студентов
    students = [
        ("ivan_petrov", "pass1", "Иван", "Петров", "Иванович", gid1),
        ("anna_smirnova", "pass2", "Анна", "Смирнова", "Петровна", gid1),
        ("oleg_kuznetsov", "pass3", "Олег", "Кузнецов", "Алексеевич", gid2),
        ("elena_volkova", "pass4", "Елена", "Волкова", "Сергеевна", gid2),
    ]
    with Session() as session:
        for username, pwd, fn, ln, mn, grp in students:
            u = User(
                username=username,
                password=pwd,
                first_name=fn,
                last_name=ln,
                middle_name=mn,
                roleType="student",
                form_education="Бюджет",
                studyGroup=grp
            )
            session.add(u)
        session.commit()

    # 5) Создаём дисциплины и привязываем к группам
    subjects = [
        "Объектно-ориентированное программирование",
        "Базы данных",
        "Системы управления разработкой программного обеспечения",
        "Иностранный язык",
    ]
    for name in subjects:
        add_subject(name)

    # Получим ID всех дисциплин для удобства
    subj_map = {s.name: s.id for s in get_subjects()}

    # Назначаем предметы группам
    reg_group_in_subject(gid1, "Объектно-ориентированное программирование")
    reg_group_in_subject(gid1, "Базы данных")
    reg_group_in_subject(gid2, "Системы управления разработкой программного обеспечения")
    reg_group_in_subject(gid2, "Иностранный язык")

    # 6) Тестируем функции и печатаем результаты

    print("Группы факультета ИТ:", get_groups_by_faculty(fac_id))

    print("Студенты в группе 231-333:", get_users_by_group(gid1))
    print("Студенты в группе 231-334:", get_users_by_group(gid2))

    print("Дисциплины для ivan_petrov:", get_user_subjects("ivan_petrov"))

    # Проверим, зачислена ли Анна на «Базы данных»
    bd_id = subj_map["Базы данных"]
    print("Анна зачислена на БД?", is_user_enrolled_in_subject("anna_smirnova", bd_id))

    # Кто учится на «Иностранный язык»
    iy_id = subj_map["Иностранный язык"]
    print("Пользователи по предмету «Иностранный язык»:", get_users_by_subject(iy_id))

    # Задачи: пока мы не добавляли таски, список будет пуст
    print("Статусы заданий у ivan_petrov:", get_student_tasks_with_status(
        next(u.id for u in Session().query(User).filter_by(username="ivan_petrov"))
    ))

if __name__ == '__main__':
    test2()
