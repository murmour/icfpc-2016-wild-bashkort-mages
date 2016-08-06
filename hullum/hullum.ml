
open Batteries
open Num
open Utils
open Geometry


let interactive = ref false
let input_file = ref ""
let output_file = ref ""
let dissect_step = num_of_int 10
let iterations = ref 10


let gen_dissections (sol: Solution.t) hull =
  let vertexes =
    collect (fun push ->
      let hull = List.tl hull in
      List.combine hull (rotate hull) |> List.iter (fun ((x1, y1), (x2, y2)) ->
         let slope_x = (x2 -/ x1) // dissect_step in
         let slope_y = (y2 -/ y1) // dissect_step in
         push (`Existing, (x1, y1));
         let x0 = ref (x1 + slope_x) in
         let y0 = ref (y1 + slope_y) in
         while !x0 <>/ x2 || !y0 <>/ y2 do
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
            let add_vertex (sol: Solution.t) v =
              { sol with source = v :: sol.source; dest = v :: sol.dest }
            in
            let line = Geometry.compute_line v1 v2 in
            let sol = if kind1 = `New then add_vertex sol v1 else sol in
            let sol = if kind2 = `New then add_vertex sol v2 else sol in
            push (line, sol)
          end)))

let apply_dissection target hull_old
    (relation: [ `Above | `Below | `OnLine ])
    ((l: line), (sol: Solution.t))
  : (Solution.t * area) option =
  let dest = sol.dest |> List.map (fun v ->
    if Geometry.line_vertex_relation l v = relation then
      Geometry.flip_vertex l v
    else
      v)
  in
  let hull_new = dest |> Geometry.convex_hull in
  let hull_union = Geometry.convex_hull (hull_old @ hull_new) in
  if not (Geometry.hulls_are_equal hull_union hull_old) then
    None
  else
    let hull_union = Geometry.convex_hull (hull_new @ target) in
    if not (Geometry.hulls_are_equal hull_union hull_new) then
      None
    else
      Some ({ sol with dest; flips = l :: sol.flips },
            Geometry.hull_area hull_new)

let apply_best_dissection target (sol: Solution.t) : Solution.t option =
  let hull = sol.dest |> Geometry.convex_hull in
  let sects = gen_dissections sol hull in
  let forks1 = sects |> List.filter_map (apply_dissection target hull `Above) in
  let forks2 = sects |> List.filter_map (apply_dissection target hull `Below) in
  let best = ref None in
  let min_area = ref num_2 in
  forks1 @ forks2 |> List.iter (fun (sol, area) ->
    if area </ !min_area then
      (min_area := area;
       best := Some sol));
  !best

let apply_all_dissections target (sol: Solution.t) : unit =
  let hull = sol.dest |> Geometry.convex_hull in
  let sects = gen_dissections sol hull in
  let forks1 = sects |> List.filter_map (apply_dissection target hull `Above) in
  let forks2 = sects |> List.filter_map (apply_dissection target hull `Below) in
  forks1 @ forks2 |> List.iter (fun ((sol: Solution.t), area) ->
    let line = List.hd sol.flips in
    Printf.printf "line: a = %s, b = %s, c = %s; area = %s%!\n"
      (string_of_num line.a)
      (string_of_num line.b)
      (string_of_num line.c)
      (string_of_num area);
    Drawing.draw_line line;
    Drawing.draw_solution target sol)

let rec solve_loop (n: int) target sol : Solution.t =
  Printf.printf "Iteration %d...%!\n" n;
  if n = !iterations then
    sol
  else match apply_best_dissection target sol with
    | Some sol ->
        solve_loop (Pervasives.succ n) target sol
    | None ->
        failwith (Printf.sprintf "Unable to find solution on iteration %d!" n)

let () =
  Arg.parse (Arg.align
    [
      ("-interactive", Arg.Unit (fun () -> interactive := true),
       " Interactive mode");
      ("-iterations", Arg.Int (fun i -> iterations := i),
       " Iteration count");
      ("-in", Arg.String (fun s -> input_file := s),
       " Problem");
      ("-out", Arg.String (fun s -> output_file := s),
       " Solution");
    ])
    (fun _ -> ())
    ("Usage: " ^ Sys.argv.(0) ^ "[options]");

  let (sl, sk) = Problem.read_file ~fname:!input_file in
  if !interactive then
    Drawing.draw_skeleton sk;
  if !interactive then
    Drawing.draw_silhouette sl;

  let target = Geometry.convex_hull (List.concat sl) in
  if !interactive then
    Drawing.draw_poly target;

  let target =
    match Geometry.fit_poly target with
      | Some t -> t
      | None ->
          failwith "Couldn't fit the target!"
  in
  if !interactive then
    Drawing.draw_poly target;

  let sol = solve_loop 0 target Solution.default in
  if !interactive then
    Drawing.draw_solution target sol;
  if !output_file <> "" then
    Solution.write_file ~fname:!output_file sol
