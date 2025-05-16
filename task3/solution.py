def merge_intervals(intervals):
    """Объединяет пересекающиеся интервалы"""
    if not intervals:
        return []

    intervals.sort()
    merged = [intervals[0]]

    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)
    return merged


def cut_intervals_to_lesson(intervals, lesson_start, lesson_end):
    """Обрезает интервалы по времени урока"""
    result = []
    for start, end in zip(intervals[::2], intervals[1::2]):
        start = max(start, lesson_start)
        end = min(end, lesson_end)
        if start < end:
            result.append([start, end])
    return result


def intersect_intervals(a, b):
    """Находит пересечения двух списков интервалов"""
    result = []
    i = j = 0
    while i < len(a) and j < len(b):
        start = max(a[i][0], b[j][0])
        end = min(a[i][1], b[j][1])
        if start < end:
            result.append([start, end])
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return result


def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Возвращает количество времени, когда ученик и репетитор одновременно
    присутствуют на уроке.
    :param intervals: Словарь с интервалами урока, ученика и репетитора
    :return: Количество времени, когда ученик и репетитор одновременно
             присутствуют на уроке
    """
    lesson_start, lesson_end = intervals["lesson"]

    pupil_intervals = cut_intervals_to_lesson(
        intervals["pupil"], lesson_start, lesson_end
    )
    tutor_intervals = cut_intervals_to_lesson(
        intervals["tutor"], lesson_start, lesson_end
    )

    pupil_intervals = merge_intervals(pupil_intervals)
    tutor_intervals = merge_intervals(tutor_intervals)

    joint_intervals = intersect_intervals(pupil_intervals, tutor_intervals)

    return sum(end - start for start, end in joint_intervals)


tests = [
    {
        "intervals": {
            "lesson": [1594663200, 1594666800],
            "pupil": [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472,
            ],
            "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
        },
        "answer": 3117,
    },
    {
        "intervals": {
            "lesson": [1594702800, 1594706400],
            "pupil": [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641,
            ],
            "tutor": [
                1594700035,
                1594700364,
                1594702749,
                1594705148,
                1594705149,
                1594706463,
            ],
        },
        "answer": 3577,
    },
    {
        "intervals": {
            "lesson": [1594692000, 1594695600],
            "pupil": [1594692033, 1594696347],
            "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
        },
        "answer": 3565,
    },
]


if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test["intervals"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    print("✅ Все тесты пройдены.")
