
type vertex = Num.num * Num.num

type segment = vertex * vertex

type vector = Num.num * Num.num

type polygon = vertex list

type line = { a: Num.num; b: Num.num; c: Num.num }

type area = Num.num


val compare_vertex: vertex -> vertex -> int

val convex_hull: vertex list -> polygon

val fit_poly: polygon -> polygon option

val flip_poly: line -> polygon -> polygon

val flip_vertex: line -> vertex -> vertex

val get_line_y_by_x: line -> Num.num -> Num.num

val compute_line: vertex -> vertex -> line

val hull_area: polygon -> area

val hulls_are_equal: polygon -> polygon -> bool

val line_vertex_relation: line -> vertex -> [ `OnLine | `Above | `Below ]

val intersect_hulls: polygon -> polygon -> polygon option

val cross: vector -> vector -> Num.num
