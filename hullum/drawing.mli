
type shape =
  | Line of Geometry.line
  | Vertex of Geometry.vertex
  | Poly of Geometry.polygon
  | Tri of Geometry.triangle
  | LineList of Geometry.line list
  | VertexList of Geometry.vertex list
  | PolyList of Geometry.polygon list
  | TriList of Geometry.triangle list


val enabled: bool ref

val draw: (shape * Graphics.color) list -> unit
