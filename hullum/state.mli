
type t =
  {
    points: Geometry.vertex list;
    prev: (Geometry.line * t) option;
  }


val default: t
