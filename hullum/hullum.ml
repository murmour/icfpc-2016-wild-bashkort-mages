
open Batteries
open Num
open Utils
open Geometry


let input_file = ref ""
let output_file = ref "stdout"
let iterations = ref 100
let dissections = ref 10
let exact_only = ref false


let () =
  Arg.parse (Arg.align
    [
      ("-interactive", Arg.Unit (fun () -> Drawing.enabled := true),
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
  let sl_area = Problem.silhouette_area sl in
  let sl_points = List.concat sl in

  let (sl_points, offset) =
    match Geometry.fit_poly sl_points with
      | Some t -> t
      | None ->
          failwith "Couldn't fit the silhouette!"
  in

  let hull = Geometry.convex_hull sl_points in
  let hull_area = Geometry.absolute_poly_area hull in

  Drawing.draw [
    (Poly sl_points, Graphics.white);
    (Poly hull, Graphics.green);
  ];

  if !exact_only && (hull_area <>/ sl_area) then
    failwith (Printf.sprintf "Exact solution is impossible! \
                              (hull area: %s, silhouette area: %s)"
                (string_of_num hull_area)
                (string_of_num sl_area));

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

  let sol = Solution.recover best offset in
  Drawing.draw [ (PolyList sol.facets, Graphics.white) ];

  if !output_file = "stdout" then
    output_string stdout (Solution.print sol)
  else
    File.with_file_out ~mode:[`create] !output_file (fun ch ->
      IO.nwrite ch (Solution.print sol))
