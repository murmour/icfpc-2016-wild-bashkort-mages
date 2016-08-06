
open Batteries
open Num
open Utils


type vertex = num * num

type segment = vertex * vertex

type vector = num * num

type polygon = vertex list

type line = { a: num; b: num; c: num }

type area = num

type line_relation = Exact | Above | Below

type fit_offset = { shift: vector; mult: vector }

type triangle = vertex * vertex * vertex


let compare_vertex (x1, y1) (x2, y2) =
  match compare_num x1 x2 with
    | 0 ->
        compare_num y1 y2
    | etc ->
        etc

let equal_vertexes v1 v2 =
  compare_vertex v1 v2 = 0

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

let vector_of_ints (x, y) : vector =
  (num_of_int x, num_of_int y)

let for_each_poly_mult action : unit =
  [ (1, 1); (1, -1); (-1, 1); (-1, -1) ]
  |> List.map vector_of_ints
  |> List.iter action

let apply_poly_mult (p: polygon) ((mult_x, mult_y): vector) =
  p |> List.map (fun (x, y) -> (x * mult_x, y * mult_y))

let vertex_fits (x, y) : bool =
  x >=/ num_0 && x <=/ num_1 && y >=/ num_0 && y <=/ num_1

let poly_fits p : bool =
  p |> List.for_all vertex_fits

let gen_poly_shift p : vector =
  let min_x = p |> List.map fst |> List.reduce min_num in
  let min_y = p |> List.map snd |> List.reduce min_num in
  (minus_num min_x, minus_num min_y)

let apply_poly_shift (p: polygon) ((shift_x, shift_y): vector) =
  p |> List.map (fun (x, y) -> (x + shift_x, y + shift_y))

let fit_poly p : (polygon * fit_offset) option =
  Return.label (fun l ->
    for_each_poly_mult (fun (mult: vector) ->
      let p = apply_poly_mult p mult in
      let shift = gen_poly_shift p in
      let p = apply_poly_shift p shift in
      if poly_fits p then
        Return.return l (Some (p, { mult; shift })));
    None)

let negate_offset (off: fit_offset) : fit_offset =
  let (shift_x, shift_y) = off.shift in
  { mult = off.mult; shift = (minus_num shift_x, minus_num shift_y) }

let apply_vertex_offset (off: fit_offset) ((x, y): vertex) : vertex =
  let (mult_x, mult_y) = off.mult in
  let (shift_x, shift_y) = off.shift in
  ((x + shift_x) * mult_x, (y + shift_y) * mult_y)

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

let cross ((ax, ay): vector) ((bx, by): vector) : num =
  ax*by - ay*bx

let vec ((ax, ay): vertex) ((bx, by): vertex) =
  (bx - ax, by - ay)

let hull_area (p: polygon) : area =
  let sum = ref num_0 in
  List.combine p (rotate p) |> List.iter (fun (v1, v2) ->
    sum := !sum + cross v1 v2);
  num_1_by_2 * abs_num !sum

let hulls_are_equal (p1: polygon) (p2: polygon) : bool =
  let rec iter = function
    | ([], []) ->
        true
    | (_, []) | ([], _) ->
        false
    | (v1 :: v1s, v2 :: v2s) ->
        if equal_vertexes v1 v2 then iter (v1s, v2s) else false
  in
  iter (p1, p2)

let line_vertex_relation (l: line) ((x, y): vertex) : line_relation =
  let res = compare_num (l.a*x + l.b*y + l.c) num_0 in
  if res < 0 then
    Below
  else if res > 0 then
    Above
  else
    Exact

let segment_intersection (s1: segment) (s2: segment) : vertex option =
  let (a, b) = s1 and (c, d) = s2 in
  let (ax, ay) = a and (bx, by) = b and (cx, cy) = c and (dx, dy) = d in
  if not ((gt_num (cross (vec c b) (vec c d) *
                   cross (vec c d) (vec c a)) num_0) &&
          (gt_num (cross (vec a c) (vec a b) *
                   cross (vec a b) (vec a d)) num_0)) then
    None
  else
    let dt = (bx - ax)*(cy - dy) - (cx - dx)*(by - ay) in
    let t = (num_1 / dt) * ((cx - ax)*(cy - dy) - (cx - dx)*(cy - ay)) in
    let x = ax + (bx - ax)*t in
    let y = ay + (by - ay)*t in
    Some (x, y)

let triangulate_hull (h: polygon) : triangle list =
  collect (fun push ->
    match h with
      | skipped :: v1 :: rest ->
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
  lt_num ((x1 - x3)*(y2 - y3)) ((x2 - x3)*(y1 - y3))

let point_on_segment ((ox, oy) as o) ((ax, ay) as a) ((bx, by) as b) =
  if (ox </ ax && ox </ bx) || (ox >/ ax && ox >/ bx) ||
     (oy </ ay && oy </ by) || (oy >/ ay && oy >/ by) then
    false
  else
    cross (vec o a) (vec o b) =/ num_0

let point_in_triangle ((a, b, c): triangle) (v: vertex) : bool =
  if point_on_segment v a b ||
     point_on_segment v b c ||
     point_on_segment v a c then
    true
  else
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
  let set1 = triangulate_hull h1 in
  let set2 = triangulate_hull h2 in
  let h3 = h1 @ h2 @ inter_points |> List.filter (fun v ->
    set1 |> List.exists (fun t -> point_in_triangle t v) &&
    set2 |> List.exists (fun t -> point_in_triangle t v))
  in
  let h3 = convex_hull h3 in
  if hull_area h3 =/ num_0 then
    None
  else
    Some h3

let gen_huge_segment (l: line) : segment =
  if l.a =/ num_0 then
    let y0 = (minus_num l.c) / l.b in
    ((num_neg2, y0), (num_2, y0))
  else if l.b =/ num_0 then
    let x0 = (minus_num l.c) / l.a in
    ((x0, num_neg2), (x0, num_2))
  else
    ((num_neg2, get_line_y_by_x l num_neg2),
     (num_2, get_line_y_by_x l num_2))

let point_on_line ((x, y): vertex) (l: line) : bool =
  l.a*x + l.b*y + l.c =/ num_0

let line_hull_intersection (l: line) (h: polygon) =
  let seg1 = gen_huge_segment l in
  collect (fun push ->
    let h = List.tl h in
    List.combine h (rotate h) |> List.iter (fun ((v3, v4) as seg2) ->
      if point_on_line v3 l then
        push (`Existing v3)
      else
        segment_intersection seg1 seg2 |> Option.may (fun v ->
          push (`New v))))

let polymorphic_segments ((v1, v2): segment) ((v3, v4): segment) : bool =
  (equal_vertexes v1 v3 && equal_vertexes v2 v4) ||
  (equal_vertexes v1 v4 && equal_vertexes v2 v3)

let is_poly_edge (p: polygon) (s: segment) : bool =
  Return.label (fun l ->
    List.combine p (rotate p) |> List.iter (fun s' ->
      if polymorphic_segments s s' then
        Return.return l true);
    false)
