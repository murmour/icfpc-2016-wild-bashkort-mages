
type t =
  {
    source: Geometry.vertex list;
    dest: Geometry.vertex list;
    prev: (Geometry.line * t) option;
  }

type facet = Geometry.polygon


val write_file: fname: string -> t -> facet list -> unit

val default: t
