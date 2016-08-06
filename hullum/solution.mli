
type facet = Geometry.polygon

type t =
  {
    vertexes: (Geometry.vertex * Geometry.vertex) list;
    facets: facet list;
  }


val write_file: fname: string -> t -> unit

val recover: State.t -> t
