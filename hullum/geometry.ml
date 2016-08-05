
open Batteries
open Num


type vertex = num * num

type segment = vertex * vertex

type polygon = vertex list

type line = { a: Num.num; b: Num.num; c: Num.num }


let compare_vertex (x1, y1) (x2, y2) =
  match compare_num x1 x2 with
    | 0 ->
        compare_num y1 y2
    | etc ->
        etc

let does_cw (ox, oy) (ax, ay) (bx, by) =
  (ax - ox) * (by - oy) - (ay - oy) * (bx - ox) <= num_of_int 0

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

let vertex_of_ints (x, y) =
  (num_of_int x, num_of_int y)

let gen_poly_rotations (p: polygon) : polygon list =
  [ (1, 1); (1, -1); (-1, 1); (-1, -1) ]
  |> List.map vertex_of_ints
  |> List.map (fun (rot_x, rot_y) ->
      p |> List.map (fun (x, y) ->
        (x * rot_x, y * rot_y)))

let vertex_fits (x, y) : bool =
  x >= num_of_int 0 && x <= num_of_int 1 &&
  y >= num_of_int 0 && y <= num_of_int 1

let poly_fits p : bool =
  p |> List.for_all vertex_fits

let shift_poly p : polygon =
  let min_x = p |> List.map fst |> List.reduce min_num in
  let min_y = p |> List.map snd |> List.reduce min_num in
  p |> List.map (fun (x, y) ->
    (x - min_x, y - min_y))

let fit_poly p : polygon option =
  Return.label (fun l ->
    gen_poly_rotations p |> List.iter (fun (p: polygon) ->
      let p = shift_poly p in
      if poly_fits p then
        Return.return l (Some p));
    None)

let flip_vertex (l: line) ((x, y): vertex) : vertex =
  let d = l.a*x + l.b*y + l.c in
  let ab2 = l.a*l.a + l.b*l.b in
  let x' = x + num_of_int (-2) * ((l.a*d)/ab2) in
  let y' = y + num_of_int (-2) * ((l.b*d)/ab2) in
  (x', y')

let flip_poly (l: line) p =
  p |> List.map (flip_vertex l)

let get_line_y_by_x (l: line) x =
  (minus_num (l.a*x) - l.c) / l.b
