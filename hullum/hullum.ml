
let interactive = ref false
let problem_file = ref ""

let () =
  Arg.parse (Arg.align
    [
      ("-interactive", Arg.Unit (fun () -> interactive := true),
       " Interactive mode");
    ])
    (fun s -> problem_file := s)
    ("Usage: " ^ Sys.argv.(0) ^ "[options]");

  let (sl, sk) = Problem.read_file ~fname:!problem_file in
  if !interactive then
    Drawing.draw_skeleton sk;

  let hull = Geometry.convex_hull (List.concat sl) in
  if !interactive then
    Drawing.draw_poly hull;

  let fitted =
    match Geometry.fit_poly hull with
      | Some hull ->
          hull
      | None ->
          failwith "Couldn't fit the hull"
  in
  if !interactive then
    Drawing.draw_poly fitted
