
open Batteries
open Num
open Utils


let interactive = ref false
let problem_file = ref ""
let dissect_step = num_of_int 10


let gen_dissections (sol: Solution.t) =
  let hull = sol |> List.map fst |> Geometry.convex_hull in
  let vertexes =
    collect (fun push ->
      let hull = List.tl hull in
      List.combine hull (rotate hull) |> List.iter (fun ((x1, y1), (x2, y2)) ->
         let slope_x = (x2 -/ x1) // dissect_step in
         let slope_y = (y2 -/ y1) // dissect_step in
         push (`Existing, (x1, y1));
         let x0 = ref (x1 + slope_x) in
         let y0 = ref (y1 + slope_y) in
         while !x0 <> x2 || !y0 <> y2 do
           push (`New, (!x0, !y0));
           x0 := !x0 + slope_x;
           y0 := !y0 + slope_y;
         done))
  in
  collect (fun push ->
    vertexes |> List.iter (fun (kind1, v1) ->
      vertexes |> List.iter (fun (kind2, v2) ->
        if Geometry.compare_vertex v1 v2 > 0 then
          begin
            let line = Geometry.compute_line v1 v2 in
            let sol = if kind1 = `New then (v1, v1) :: sol else sol in
            let sol = if kind2 = `New then (v2, v2) :: sol else sol in
            push (line, sol)
          end)))


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

  let target = Geometry.convex_hull (List.concat sl) in
  if !interactive then
    Drawing.draw_poly target;

  let fitted_target =
    match Geometry.fit_poly target with
      | Some t -> t
      | None ->
          failwith "Couldn't fit the target"
  in
  if !interactive then
    Drawing.draw_poly fitted_target;

  let sol = Solution.default in
  Printf.printf "%s\n" (dump (gen_dissections sol))
