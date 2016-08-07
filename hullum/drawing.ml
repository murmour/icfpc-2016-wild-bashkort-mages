
open Batteries
open Graphics
open Geometry
open Utils


type shape =
  | Line of Geometry.line
  | Vertex of Geometry.vertex
  | Poly of Geometry.polygon
  | Tri of Geometry.triangle
  | LineList of Geometry.line list
  | VertexList of Geometry.vertex list
  | PolyList of Geometry.polygon list
  | TriList of Geometry.triangle list


let width = 800
let height = 800


let enabled =
  ref false

let wait () =
  let continue = ref false in
  while not !continue do
    if key_pressed () then
      let _ = read_key () in
      continue := true
  done

let with_canvas action =
  if !enabled then
    begin
      open_graph (Printf.sprintf " %dx%d" width height);
      set_color black;
      fill_rect 0 0 width height;
      set_line_width 1;
      action ();
      wait ();
    end

let conv_vertex ((x, y): vertex) : (int * int) =
  (truncate (Num.float_of_num x *. (float_of_int width)),
   truncate (Num.float_of_num y *. (float_of_int height)))

let draw_vertex (v: vertex) =
  let (x, y) = conv_vertex v in
  Graphics.draw_circle x y 10

let draw_segment ((v1, v2): segment) =
  Graphics.draw_poly_line [| conv_vertex v1; conv_vertex v2 |]

let draw_poly (p: polygon) =
  Geometry.poly_edges p |> List.iter draw_segment

let draw_line (l: line) =
  let open Num in
  let (x1, y1, x2, y2) =
    if l.a =/ num_0 then
      let y0 = (minus_num l.c) / l.b in
      let x1 = num_0 in
      let x2 = num_1 in
      (x1, y0, x2, y0)
    else if l.b =/ num_0 then
      let x0 = (minus_num l.c) / l.a in
      let y1 = num_0 in
      let y2 = num_1 in
      (x0, y1, x0, y2)
    else
      let x1 = num_of_int 0 in
      let x2 = num_of_int 1 in
      let y1 = Geometry.get_line_y_by_x l x1 in
      let y2 = Geometry.get_line_y_by_x l x2 in
      (x1, y1, x2, y2)
  in
  draw_segment ((x1, y1), (x2, y2))

let draw_triangle (a, b, c) =
  draw_poly [ a; b; c ]

let draw shapes =
  with_canvas (fun () ->
    shapes |> List.iter (fun (s, c) ->
      set_color c;
      match s with
        | Line l ->
            draw_line l
        | Vertex v ->
            draw_vertex v
        | Poly p ->
            draw_poly p
        | Tri t ->
            draw_triangle t
        | LineList ls ->
            ls |> List.iter draw_line
        | VertexList vs ->
            vs |> List.iter draw_vertex
        | PolyList ps ->
            ps |> List.iter draw_poly
        | TriList ts ->
            ts |> List.iter draw_triangle))
