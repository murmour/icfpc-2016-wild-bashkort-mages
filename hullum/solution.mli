
type t =
  {
    source: Geometry.vertex list;
    dest: Geometry.vertex list;
    prev: (Geometry.line * t) option;
  }


val write_file: fname: string -> t -> unit

val default: t
