
type t =
  {
    source: Geometry.vertex list;
    dest: Geometry.vertex list;
    flips: Geometry.line list;
  }


val write_file: fname: string -> t -> unit

val default: t
