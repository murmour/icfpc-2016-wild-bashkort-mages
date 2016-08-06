
open Batteries
open Utils
open Printf


type t =
  {
    source: Geometry.vertex list;
    dest: Geometry.vertex list;
    flips: Geometry.line list;
  }


let write_file ~fname sol =
  let cout = open_out fname in
  let print_vertex (x, y) =
    fprintf cout "%s,%s " (Num.string_of_num x) (Num.string_of_num y)
  in

  fprintf cout "%d\n" (List.length sol.source);
  sol.source |> List.iter print_vertex;
  fprintf cout "\n";

  fprintf cout "1\n";
  let hull = sol.dest |> Geometry.convex_hull in
  fprintf cout "%d " (List.length hull);
  hull |> List.tl |> List.iter (fun v ->
    let i = List.index_ofq v sol.source |> Option.get in
    fprintf cout "%d " i);
  fprintf cout "\n";

  sol.dest |> List.iter print_vertex;
  fprintf cout "\n"


let square =
  [ (num_0, num_0); (num_0, num_1); (num_1, num_0); (num_1, num_1) ]

let default =
  {
    source = square;
    dest = square;
    flips = [];
  }
