
open Batteries
open Num
open Utils
open Geometry


let interactive = ref false
let input_file = ref ""
let output_file = ref "stdout"
let iterations = ref 10
let dissections = ref 10


let () =
  Arg.parse (Arg.align
    [
      ("-interactive", Arg.Unit (fun () -> interactive := true),
       " Interactive mode");
      ("-iterations", Arg.Int (fun i -> iterations := i),
       " Iteration count");
      ("-dissections", Arg.Int (fun i -> dissections := i),
       " Edge dissection count");
      ("-in", Arg.String (fun s -> input_file := s),
       " Problem");
      ("-out", Arg.String (fun s -> output_file := s),
       " Solution");
    ])
    (fun _ -> ())
    ("Usage: " ^ Sys.argv.(0) ^ "[options]");

  let (sl, sk) = Problem.read_file ~fname:!input_file in
  (* if !interactive then *)
  (*   Drawing.draw_skeleton sk; *)
  (* if !interactive then *)
  (*   Drawing.draw_silhouette sl; *)

  let target = Geometry.convex_hull (List.concat sl) in
  (* if !interactive then *)
  (*   Drawing.draw_poly target; *)

  let (target, offset) =
    match Geometry.fit_poly target with
      | Some t -> t
      | None ->
          failwith "Couldn't fit the target!"
  in
  (* if !interactive then *)
  (*   Drawing.draw_poly target; *)

  let st = Solver.exact
      ~iterations:!iterations
      ~dissections:!dissections
      ~target
      ~offset
  in
  if !interactive then
    Drawing.draw_state target st;

  let sol = Solution.recover st offset in
  if !interactive then
    Drawing.draw_poly_list sol.facets;

  if !output_file = "stdout" then
    output_string stdout (Solution.print sol)
  else
    File.with_file_out ~mode:[`create] !output_file (fun ch ->
      IO.nwrite ch (Solution.print sol))
