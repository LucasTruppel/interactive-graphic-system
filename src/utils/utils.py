def format_point_list(points_list: list[tuple[float, float]]) -> str:
    return (str(points_list)
            .replace("[", "")
            .replace("]", "")
            .replace(".0,", ",")
            .replace(".0)", ")"))