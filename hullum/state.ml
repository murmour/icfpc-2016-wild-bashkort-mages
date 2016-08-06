
open Utils


type t =
  {
    points: Geometry.vertex list;
    area: Geometry.area;
    prev: (Geometry.line * t) option;
  }


let square =
  [ (num_0, num_0); (num_0, num_1); (num_1, num_0); (num_1, num_1) ]

let default =
  {
    points = square;
    area = num_1;
    prev = None;
  }
