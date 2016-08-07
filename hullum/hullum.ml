
open Batteries
open Num
open Utils
open Geometry


let interactive = ref false
let input_file = ref ""
let output_file = ref "stdout"
let iterations = ref 10
let dissections = ref 10
let exact_only = ref false


let () =
  Arg.parse (Arg.align
    [
      ("-interactive", Arg.Unit (fun () -> interactive := true),
       " Interactive mode");
      ("-iterations", Arg.Int (fun i -> iterations := i),
       " Iteration count");
      ("-dissections", Arg.Int (fun i -> dissections := i),
       " Edge dissection count");
      ("-exact", Arg.Unit (fun () -> exact_only := true),
       " Drop approximate solutions");
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
  let sl_area = Problem.silhouette_area sl in

  let hull = Geometry.convex_hull (List.concat sl) in
  (* if !interactive then *)
  (*   Drawing.draw_poly hull; *)
  let hull_area = Geometry.hull_area hull in

  if !exact_only && (hull_area <>/ sl_area) then
    failwith (Printf.sprintf "Exact solution is impossible! \
                              (hull area: %s, silhouette area: %s)"
                (string_of_num hull_area)
                (string_of_num sl_area));

  let (hull, offset) =
    match Geometry.fit_poly hull with
      | Some t -> t
      | None ->
          failwith "Couldn't fit the hull!"
  in
  (* if !interactive then *)
  (*   Drawing.draw_poly hull; *)

  let iterations = !iterations in
  let dissections = !dissections in
  let best =
    let s1 = Solver.exact ~iterations ~dissections ~target:hull ~offset in
    if s1.area =/ hull_area then s1
    else
      let s2 = Solver.approx ~iterations ~dissections ~target:hull ~offset in
      if s1.area </ s2.area then s1 else s2
  in

  if best.area =/ hull_area then
    (if hull_area =/ sl_area then
       Printf.eprintf "Got exact solution!\n%!"
     else
       Printf.eprintf "Got best possible convex solution!\n%!");

  if !exact_only && (best.area <>/ hull_area) then
    failwith (Printf.sprintf "Got inexact solution! (area = %s of %s)"
                (string_of_num best.area)
                (string_of_num hull_area));

  if !interactive then
    Drawing.draw_state hull best;

  let sol = Solution.recover best offset in
  if !interactive then
    Drawing.draw_poly_list sol.facets;

  if !output_file = "stdout" then
    output_string stdout (Solution.print sol)
  else
    File.with_file_out ~mode:[`create] !output_file (fun ch ->
      IO.nwrite ch (Solution.print sol))
