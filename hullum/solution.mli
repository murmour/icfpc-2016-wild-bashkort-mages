
type facet = Geometry.polygon

type t =
  {
    vertices: (Geometry.vertex * Geometry.vertex) list;
    facets: facet list;
  }


val print: t -> string

val size: t -> int

val recover: State.t -> Geometry.fit_offset -> t
