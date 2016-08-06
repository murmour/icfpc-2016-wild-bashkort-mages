
open Batteries
open Num
open Utils


type vertex = num * num

type segment = vertex * vertex

type polygon = vertex list

type line = { a: Num.num; b: Num.num; c: Num.num }

type area = num

type triangle = vertex * vertex * vertex


let compare_vertex (x1, y1) (x2, y2) =
  match compare_num x1 x2 with
    | 0 ->
        compare_num y1 y2
    | etc ->
        etc

let print_vertex (x, y) =
  Printf.sprintf "%s,%s" (string_of_num x) (string_of_num y)

let triple_orientation (ox, oy) (ax, ay) (bx, by) : [ `CW | `CCW | `COLL ] =
  let res = compare_num ((ax - ox) * (by - oy)) ((ay - oy) * (bx - ox)) in
  if res = 0 then
    `COLL
  else if res < 0 then
    `CW
  else
    `CCW

let convex_hull points : polygon =
  let sorted = List.sort compare_vertex points in
  let rsorted = List.rev sorted in
  let drop_first l = match l with [] -> [] | h :: t -> t in

  let rec clean x l =
    match l with
      | a :: (b :: _ as rest) when triple_orientation b a x <> `CCW ->
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
  x >=/ num_0 && x <=/ num_1 && y >=/ num_0 && y <=/ num_1

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
  let x' = x + num_neg2 * ((l.a*d)/ab2) in
  let y' = y + num_neg2 * ((l.b*d)/ab2) in
  (x', y')

let flip_poly (l: line) p =
  p |> List.map (flip_vertex l)

let get_line_y_by_x (l: line) x =
  (minus_num (l.a*x) - l.c) / l.b

let compute_line ((x1, y1): vertex) ((x2, y2): vertex) : line =
  let a = y2 - y1 in
  let b = x1 - x2 in
  let c = minus_num (a*x1) - b*y1 in
  { a; b; c }

let hull_area (p: polygon) : area =
  let sum = ref num_0 in
  List.combine p (rotate p) |> List.iter (fun ((x1, y1), (x2, y2)) ->
    sum := !sum + x1*y2 - x2*y1);
  num_1_by_2 * abs_num !sum

let hulls_are_equal (p1: polygon) (p2: polygon) : bool =
  let rec iter = function
    | ([], []) ->
        true
    | (_, []) | ([], _) ->
        false
    | (v1 :: v1s, v2 :: v2s) ->
        if compare_vertex v1 v2 = 0 then iter (v1s, v2s) else false
  in
  iter (p1, p2)

let line_vertex_relation (l: line) ((x, y): vertex) =
  let res = compare_num (l.a*x + l.b*y + l.c) num_0 in
  if res < 0 then
    `Below
  else if res > 0 then
    `Above
  else
    `OnLine

let dot_product ((ax, ay): vertex) ((bx, by): vertex) : num =
  ax*by - ay*bx

let vec ((ax, ay): vertex) ((bx, by): vertex) =
  (bx - ax, by - ay)

let segment_intersection (s1: segment) (s2: segment) : vertex option =
  let (a, b) = s1 and (c, d) = s2 in
  let (ax, ay) = a and (bx, by) = b and (cx, cy) = c and (dx, dy) = d in
  if not ((gt_num (dot_product (vec c b) (vec c d) *
                   dot_product (vec c d) (vec c a)) num_0) &&
          (gt_num (dot_product (vec a c) (vec a b) *
                   dot_product (vec a b) (vec a d)) num_0)) then
    None
  else
    let dt = (bx - ax)*(cy - dy) - (cx - dx)*(by - ay) in
    let t = (num_1 // dt) * ((cx - ax)*(cy - dy) - (cx - dx)*(cy - ay)) in
    let x = ax + (bx - ax)*t in
    let y = ay + (by - ay)*t in
    Some (x, y)

let triangulate_hull (h: polygon) : triangle list =
  collect (fun push ->
    match h with
      | v1 :: rest ->
          let rec iter = function
            | v2 :: ((v3 :: _) as rest) ->
                push (v1, v2, v3);
                iter rest
            | _ -> ()
          in
          iter rest
      | _ -> ())

let triangle_is_negative ((a, b, c): triangle) : bool =
  let (x1, y1) = a and (x2, y2) = b and (x3, y3) = c in
  le_num ((x1 - x3) * (y2 - y3)) ((x2 - x3) * (y1 - y3))

let point_in_triangle ((a, b, c): triangle) (v: vertex) : bool =
  let b1 = triangle_is_negative (v, a, b) in
  let b2 = triangle_is_negative (v, b, c) in
  let b3 = triangle_is_negative (v, c, a) in
  (b1 = b2) && (b2 = b3)

let get_hull_inter_points (h1: polygon) (h2: polygon) : vertex list =
  let h1 = List.tl h1 and h2 = List.tl h2 in
  collect (fun push ->
    List.combine h1 (rotate h1) |> List.iter (fun seg1 ->
      List.combine h2 (rotate h2) |> List.iter (fun seg2 ->
        segment_intersection seg1 seg2 |> Option.may push)))

let intersect_hulls h1 h2 : polygon option =
  let inter_points = get_hull_inter_points h1 h2 in
  inter_points |> List.iter (fun v ->
    Printf.printf "%s\n" (print_vertex v));
  let set1 = triangulate_hull h1 in
  let set2 = triangulate_hull h2 in
  let h3 = h1 @ h2 @ inter_points |> List.filter (fun v ->
    set1 |> List.exists (fun t -> point_in_triangle t v) &&
    set2 |> List.exists (fun t -> point_in_triangle t v))
  in
  if h3 = [] then None else Some (convex_hull h3)
