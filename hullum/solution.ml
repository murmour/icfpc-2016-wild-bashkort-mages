
open Batteries
open Utils
open Printf


type t = (Geometry.vertex * Geometry.vertex) list


let write_file ~fname sol =
  let cout = open_out fname in
  let print_vertex (x, y) =
    fprintf cout "%s,%s " (Num.string_of_num x) (Num.string_of_num y)
  in

  let orig = sol |> List.map snd in
  fprintf cout "%d\n" (List.length sol);
  orig |> List.iter print_vertex;
  fprintf cout "\n";

  fprintf cout "1\n";
  let hull = sol |> List.map fst |> Geometry.convex_hull in
  fprintf cout "%d " (List.length hull);
  hull |> List.tl |> List.iter (fun v ->
    let i = List.index_ofq v orig |> Option.get in
    fprintf cout "%d " i);
  fprintf cout "\n";

  sol |> List.iter (fst %> print_vertex);
  fprintf cout "\n"


let default =
  List.map (fun v -> (v, v))
    [ (num_0, num_0); (num_0, num_1); (num_1, num_0); (num_1, num_1) ]
