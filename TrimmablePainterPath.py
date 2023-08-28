from PySide6.QtCore import QPointF, QLineF
from PySide6.QtGui import QPainterPath


class TrimmablePainterPath(QPainterPath):
    @staticmethod
    def trim(path: QPainterPath, start_percentage: float, end_percentage: float) -> QPainterPath:
        if start_percentage < 0.0 or start_percentage > 1.0 or end_percentage < 0.0 or end_percentage > 1.0:
            raise ValueError("Percentage values must be between 0 and 1.")
        if start_percentage == end_percentage:
            return QPainterPath()

        trimmed_path = QPainterPath()
        total_length = path.length()
        # Calculate the start and end points based on percentages
        start_length = total_length * start_percentage
        end_length = total_length * end_percentage
        current_length = 0

        i = 0
        while i < path.elementCount() and current_length < end_length:
            path_element: QPainterPath.Element = path.elementAt(i)
            element_type = 0
            if path_element.isLineTo():
                element_type = 1
            elif path_element.isCurveTo():
                element_type = 3

            if not path_element.isMoveTo():
                segment_length = 0
                if path_element.isLineTo():
                    segment = QLineF(path.elementAt(i-1), path_element)
                    segment_length = segment.length()
                elif path_element.isCurveTo():
                    p0, p1, p2, p3 = [QPointF(path.elementAt(j).x, path.elementAt(j).y) for j in range(i-1, i+3)]

                    bezier_path = QPainterPath()
                    bezier_path.moveTo(p0)
                    bezier_path.cubicTo(p1, p2, p3)
                    segment_length = bezier_path.length()

                if current_length < start_length and current_length + segment_length <= start_length:
                    current_length += segment_length
                    i += element_type
                    continue

            if path_element.isMoveTo():
                trimmed_path.moveTo(path_element.x, path_element.y)
                i += 1
            elif path_element.isLineTo():
                segment = QLineF(path.elementAt(i - 1), path_element)
                # Segment must be trimmed
                if current_length <= start_length < current_length + segment_length or current_length <= end_percentage < current_length + segment_length:
                    _start = (start_length - current_length)/segment_length
                    if _start < 0:
                        _start = 0
                    _end = (end_length - current_length) / segment_length
                    if _end > 1:
                        _end = 1
                    start_point = segment.pointAt(_start)
                    end_point = segment.pointAt(_end)
                    trimmed_path.moveTo(start_point)
                    trimmed_path.lineTo(end_point.x(), end_point.y())
                    current_length += segment_length
                    i += element_type
                # Segment must be added entirely
                else:
                    trimmed_path.lineTo(path_element.x, path_element.y)
                    current_length += segment_length
                    i += element_type
            elif path_element.isCurveTo():
                p0, p1, p2, p3 = [QPointF(path.elementAt(j).x, path.elementAt(j).y) for j in range(i-1, i+3)]

                new_points = None
                # Segment should be trimmed from right
                if current_length < start_length:
                    start_percentage = (start_length - current_length) / segment_length
                    if start_percentage > 1:
                        start_percentage = 1
                    new_points = TrimmablePainterPath.trim_cubic_bezier_curve(start_percentage, p0, p1, p2, p3)[1]
                # Segment shouldn't be trimmed
                elif current_length + segment_length <= end_length:
                    new_points = [p0, p1, p2, p3]
                # Segment should be trimmed from left
                else:
                    end_percentage = (end_length - current_length)/segment_length
                    new_points = TrimmablePainterPath.trim_cubic_bezier_curve(end_percentage, p0, p1, p2, p3)[0]

                if trimmed_path.isEmpty():
                    trimmed_path.moveTo(new_points[0])
                trimmed_path.cubicTo(*new_points[1:])
                current_length += segment_length
                i += element_type
        return trimmed_path

    @staticmethod
    def trim_cubic_bezier_curve(u0, p0, p1, p2, p3):
        if u0 < 0.0 or u0 > 1.0:
            raise ValueError("Percentage value must be between 0 and 1.")

        def lerp(p0, p1, u):
            return (1 - u) * p0 + u * p1

        r0 = lerp(p0, p1, u0)
        r1 = lerp(p1, p2, u0)
        r2 = lerp(p2, p3, u0)

        s0 = lerp(r0, r1, u0)
        s1 = lerp(r1, r2, u0)

        t0 = lerp(s0, s1, u0)

        return [[p0, r0, s0, t0], [t0, s1, r2, p3]]