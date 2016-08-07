
type t =
  {
    points: Geometry.vertex list;
    area: Geometry.area;
    prev: (Geometry.line * Geometry.orientation * t) option;
  }


val default: t

val draw: target: Geometry.polygon -> t -> unit
