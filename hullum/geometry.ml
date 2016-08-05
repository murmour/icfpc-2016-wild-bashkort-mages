
open Num


type vertex = num * num

type line = vertex * vertex

type polygon = vertex list


let compare_vertex (x1, y1) (x2, y2) =
  match compare_num x1 x2 with
    | 0 ->
        compare_num y1 y2
    | etc ->
        etc

let does_cw (ox, oy) (ax, ay) (bx, by) =
  (ax -/ ox) */ (by -/ oy) -/ (ay -/ oy) */ (bx -/ ox) <=/ num_of_int 0

let convex_hull points : polygon =
  let sorted = List.sort compare_vertex points in
  let rsorted = List.rev sorted in
  let drop_first l = match l with [] -> [] | h :: t -> t in

  let rec clean x l =
    match l with
      | a :: (b :: _ as rest) when does_cw b a x ->
          clean x rest
      | _ ->
          l
  in

  let part_hull pts = List.fold_right (fun x acc -> x :: (clean x acc)) pts [] in
  let lower = part_hull sorted in
  let upper = part_hull rsorted in

  (List.rev (drop_first lower)) @ (List.rev upper)
