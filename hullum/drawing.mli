
val draw_skeleton: Problem.skeleton -> unit

val draw_silhouette: Problem.silhouette -> unit

val draw_poly: Geometry.polygon -> unit

val draw_line: Geometry.line -> unit

val draw_line_and_two_vertexes: Geometry.line -> Geometry.vertex -> Geometry.vertex -> unit

val draw_solution: Geometry.polygon -> Solution.t -> unit

val draw_poly_list: Geometry.polygon list -> unit
