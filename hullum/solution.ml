
open Batteries
open Utils
open Printf


type t =
  {
    source: Geometry.vertex list;
    dest: Geometry.vertex list;
    prev: (Geometry.line * t) option;
  }

type facet = Geometry.polygon


let write_file ~fname sol facets =
  let cout = if fname = "stdout" then stdout else open_out fname in

  let print_vertex (x, y) =
    fprintf cout "%s,%s\n" (Num.string_of_num x) (Num.string_of_num y)
  in

  fprintf cout "%d\n" (List.length sol.source);
  sol.source |> List.iter print_vertex;

  fprintf cout "%d\n" (List.length facets);
  facets |> List.iter (fun f ->
    let f = List.tl f in
    fprintf cout "%d " (List.length f);
    f |> List.iter (fun v ->
      let i = List.index_ofq v sol.source |> Option.get in
      fprintf cout "%d " i);
    fprintf cout "\n");

  sol.dest |> List.iter print_vertex


let square =
  [ (num_0, num_0); (num_0, num_1); (num_1, num_0); (num_1, num_1) ]

let default =
  {
    source = square;
    dest = square;
    prev = None;
  }
