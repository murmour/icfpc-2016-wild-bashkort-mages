
type t = (Geometry.vertex * Geometry.vertex) list


val write_file: fname: string -> t -> unit

val default: t
