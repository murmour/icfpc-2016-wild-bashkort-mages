
let () =
  let (sl, sk) = Problem.read_file ~fname:Sys.argv.(1) in
  Drawing.draw_skeleton sk;
  let hull = Geometry.convex_hull (List.concat sl) in
  Drawing.draw_hull hull
