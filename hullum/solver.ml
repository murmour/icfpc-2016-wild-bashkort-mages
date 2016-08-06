
open Batteries
open Num
open Utils
open Geometry


let dissect_step = num_of_int 10


let gen_dissections (st: State.t) hull =
  let vertexes =
    collect (fun push ->
      let hull = List.tl hull in
      List.combine hull (rotate hull) |> List.iter (fun ((x1, y1), (x2, y2)) ->
         let slope_x = (x2 - x1) / dissect_step in
         let slope_y = (y2 - y1) / dissect_step in
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
            let add_vertex (st: State.t) v =
              { st with points = v :: st.points } in
            let line = Geometry.compute_line v1 v2 in
            let st = if kind1 = `New then add_vertex st v1 else st in
            let st = if kind2 = `New then add_vertex st v2 else st in
            push (line, st)
          end)))

let apply_dissection target hull_old
    (relation: Geometry.line_relation)
    ((l: line), (st: State.t)) : State.t option =
  let flipped_at_least_one = ref false in
  let points = st.points |> List.map (fun v ->
    if Geometry.line_vertex_relation l v <> relation then
      v
    else
      (flipped_at_least_one := true;
       Geometry.flip_vertex l v))
  in
  if not !flipped_at_least_one then
    None
  else
    let hull_new = points |> Geometry.convex_hull in
    let hull_union = Geometry.convex_hull (hull_old @ hull_new) in
    if not (Geometry.hulls_are_equal hull_union hull_old) then
      None
    else
      let hull_union = Geometry.convex_hull (hull_new @ target) in
      if not (Geometry.hulls_are_equal hull_union hull_new) then
        None
      else
        let area = Geometry.hull_area hull_new in
        Some ({ points; area; prev = Some (l, relation, st) })

let choose_best_dissection forks : State.t option =
  let best = ref None in
  let min_area = ref num_2 in
  forks |> List.iter (fun (st: State.t) ->
    if st.area </ !min_area then
      (min_area := st.area;
       best := Some st));
  !best

let apply_approx_dissection target (st: State.t) : State.t option =
  let hull = st.points |> Geometry.convex_hull in
  let sects = gen_dissections st hull in
  let forks1 = sects |> List.filter_map (apply_dissection target hull Above) in
  let forks2 = sects |> List.filter_map (apply_dissection target hull Below) in
  choose_best_dissection (forks1 @ forks2)

let apply_exact_dissection target (st: State.t) : State.t option =
  let hull = st.points |> Geometry.convex_hull in
  let sects =
    let target = List.tl target in
    List.combine target (rotate target) |> List.map (fun (v1, v2) ->
      let line = Geometry.compute_line v1 v2 in
      let inter = Geometry.line_hull_intersection line hull in
      let rec append_new = function
        | [] ->
            st
        | `New v :: vs ->
            let st = append_new vs in
            { st with points = v :: st.points }
        | `Existing v :: vs ->
            append_new vs
      in
      (line, append_new inter))
  in
  let forks1 = sects |> List.filter_map (apply_dissection target hull Above) in
  let forks2 = sects |> List.filter_map (apply_dissection target hull Below) in
  choose_best_dissection (forks1 @ forks2)

let approximate ~iterations ~target : State.t =
  let rec iter n (st: State.t) : State.t =
    Printf.eprintf "Iteration %d (area %s)...%!\n" n (string_of_num st.area);
    if n = iterations then
      st
    else match apply_approx_dissection target st with
      | Some st ->
          iter (Pervasives.succ n) st
      | None ->
          Printf.eprintf "Found a perfect solution!\n";
          st
  in
  iter 0 State.default

let exact ~iterations ~target : State.t =
  let rec iter n (st: State.t) : State.t =
    Printf.eprintf "Iteration %d (area %s)...%!\n" n (string_of_num st.area);
    if n = iterations then
      st
    else match apply_exact_dissection target st with
      | Some st ->
          iter (Pervasives.succ n) st
      | None ->
          match apply_approx_dissection target st with
            | Some st ->
                iter (Pervasives.succ n) st
            | None ->
                Printf.eprintf "Found a perfect solution!\n";
                st
  in
  iter 0 State.default
