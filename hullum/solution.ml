
open Utils


type t = (Geometry.vertex * Geometry.vertex) list


let write_file ~fname sol =
  ()

let default =
  List.map (fun v -> (v, v))
    [ (num_0, num_0); (num_0, num_1); (num_1, num_0); (num_1, num_1) ]
