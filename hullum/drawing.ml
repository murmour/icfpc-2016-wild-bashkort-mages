
open Geometry
open Graphics


let wait () =
  let continue = ref false in
  while not !continue do
    if key_pressed () then
      if read_key () = 'q' then
        continue := true
  done

let width = 800
let height = 800

let conv_vertex ((x, y): vertex) : (int * int) =
  (truncate (Num.float_of_num x *. (float_of_int width)),
   truncate (Num.float_of_num y *. (float_of_int height)))

let with_canvas action =
  open_graph (Printf.sprintf " %dx%d" width height);
  set_color black;
  fill_rect 0 0 width height;
  action ();
  wait ()

let draw_skeleton sk =
  with_canvas (fun () ->
    set_color white;
    set_line_width 1;
    sk |> List.iter (fun (v1, v2) ->
      draw_poly_line [| conv_vertex v1; conv_vertex v2 |]))
