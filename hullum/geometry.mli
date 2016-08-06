
type vertex = Num.num * Num.num

type segment = vertex * vertex

type vector = Num.num * Num.num

type polygon = vertex list

type line = { a: Num.num; b: Num.num; c: Num.num }

type area = Num.num

type line_relation = Exact | Above | Below

type fit_offset = { shift: vector; mult: vector }

type triangle = vertex * vertex * vertex


val compare_vertex: vertex -> vertex -> int

val print_vertex: vertex -> string

val convex_hull: vertex list -> polygon

val fit_poly: polygon -> (polygon * fit_offset) option

val negate_offset: fit_offset -> fit_offset

val apply_vertex_offset: fit_offset -> vertex -> vertex

val flip_poly: line -> polygon -> polygon

val flip_vertex: line -> vertex -> vertex

val get_line_y_by_x: line -> Num.num -> Num.num

val compute_line: vertex -> vertex -> line

val hull_area: polygon -> area

val hulls_are_equal: polygon -> polygon -> bool

val line_vertex_relation: line -> vertex -> line_relation

val intersect_hulls: polygon -> polygon -> polygon option

val cross: vector -> vector -> Num.num

val line_hull_intersection: line -> polygon ->
  [ `New of vertex | `Existing of vertex ] list
