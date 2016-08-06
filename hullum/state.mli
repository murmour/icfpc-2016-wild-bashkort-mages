
type t =
  {
    points: Geometry.vertex list;
    area: Geometry.area;
    prev: (Geometry.line * Geometry.line_relation * t) option;
  }


val default: t
