
open Batteries
open Utils
open Printf


type t = (Geometry.vertex * Geometry.vertex) list


let write_file ~fname sol =
  let cout = open_out fname in
  let print_vertex (x, y) =
    fprintf cout "%s,%s " (Num.string_of_num x) (Num.string_of_num y)
  in

  fprintf cout "%d\n" (List.length sol);
  sol |> List.iter (fst %> print_vertex);
  fprintf cout "\n";

  fprintf cout "1\n";
  let hull = sol |> List.map fst |> Geometry.convex_hull in
  fprintf cout "%d\n" (List.length hull);
  hull |> List.iter print_vertex;
  fprintf cout "\n";

  fprintf cout "%d\n" (List.length sol);
  sol |> List.iter (snd %> print_vertex);
  fprintf cout "\n"


let default =
  List.map (fun v -> (v, v))
    [ (num_0, num_0); (num_0, num_1); (num_1, num_0); (num_1, num_1) ]
