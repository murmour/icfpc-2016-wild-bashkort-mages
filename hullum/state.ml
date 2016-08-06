
open Utils


type t =
  {
    points: Geometry.vertex list;
    prev: (Geometry.line * t) option;
  }


let square =
  [ (num_0, num_0); (num_0, num_1); (num_1, num_0); (num_1, num_1) ]

let default =
  {
    points = square;
    prev = None;
  }
