
type vertex = Num.num * Num.num

type segment = vertex * vertex

type vector = Num.num * Num.num

type polygon = vertex list

type line = { a: Num.num; b: Num.num; c: Num.num }

type area = Num.num

type orientation = Zero | Positive | Negative

type fit_offset

type triangle = vertex * vertex * vertex


val compare_vertex: vertex -> vertex -> int

val equal_vertices: vertex -> vertex -> bool

val print_vertex: vertex -> string

val convex_hull: vertex list -> polygon

val fit_poly: polygon -> (polygon * fit_offset) option

val negate_offset: fit_offset -> fit_offset

val apply_vertex_offset: fit_offset -> vertex -> vertex

val flip_poly: line -> polygon -> polygon

val flip_vertex: line -> vertex -> vertex

val get_line_y_by_x: line -> Num.num -> Num.num

val line_from_segment: segment -> line

val poly_edges: polygon -> segment list

val poly_area: polygon -> area

val absolute_poly_area: polygon -> area

val hulls_are_equal: polygon -> polygon -> bool

val line_vertex_orientation: line -> vertex -> orientation

val intersect_hulls: polygon -> polygon -> polygon option

val cross: vector -> vector -> Num.num

val line_hull_intersection: line -> polygon ->
  [ `New of vertex | `Existing of vertex ] list

val is_poly_edge: polygon -> segment -> bool

val line_intersects_hull: line -> polygon -> bool
