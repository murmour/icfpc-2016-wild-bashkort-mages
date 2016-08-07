
open Batteries
open Num
open Utils
open Geometry


let max_solution_size = 5000


let gen_dissections ~dissections (st: State.t) hull target =
  let vertices =
    collect (fun push ->
      poly_edges hull |> List.iter (fun ((v1, v2) as edge) ->
         if not (Geometry.is_poly_edge target edge) then
           let (x1, y1) = v1 and (x2, y2) = v2 in
           let dissections = num_of_int dissections in
           let slope_x = (x2 - x1) / dissections in
           let slope_y = (y2 - y1) / dissections in
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
    vertices |> List.iter (fun (kind1, v1) ->
      vertices |> List.iter (fun (kind2, v2) ->
        if Geometry.compare_vertex v1 v2 > 0 then
          begin
            let add_vertex (st: State.t) v =
              { st with points = v :: st.points } in
            let line = Geometry.compute_line v1 v2 in
            let st = if kind1 = `New then add_vertex st v1 else st in
            let st = if kind2 = `New then add_vertex st v2 else st in
            push (line, st)
          end)))

let apply_dissection target hull_old (dir: Geometry.orientation)
    ((l: line), (st: State.t)) : State.t option =
  let flipped_at_least_one = ref false in
  let points = st.points |> List.map (fun v ->
    if Geometry.line_vertex_orientation l v <> dir then
      v
    else
      (flipped_at_least_one := true;
       Geometry.flip_vertex l v))
  in
  if not !flipped_at_least_one then
    None
  else
    let hull_new = Geometry.convex_hull points in
    let hull_union = Geometry.convex_hull (hull_old @ hull_new) in
    if not (Geometry.hulls_are_equal hull_union hull_old) then
      None
    else
      let hull_union = Geometry.convex_hull (hull_new @ target) in
      if not (Geometry.hulls_are_equal hull_union hull_new) then
        None
      else
        let area = Geometry.absolute_poly_area hull_new in
        Some ({ points; area; prev = Some (l, dir, st) })

let choose_best_dissection forks : State.t option =
  let best = ref None in
  let min_area = ref num_2 in
  forks |> List.iter (fun (st: State.t) ->
    if st.area </ !min_area then
      (min_area := st.area;
       best := Some st));
  !best

let apply_approx_dissection ~dissections target (st: State.t) : State.t option =
  let hull = Geometry.convex_hull st.points in
  let sects = gen_dissections ~dissections st hull target in
  let ds1 = sects |> List.filter_map (apply_dissection target hull Positive) in
  let ds2 = sects |> List.filter_map (apply_dissection target hull Negative) in
  choose_best_dissection (ds1 @ ds2)

let apply_exact_dissection target (st: State.t) : State.t option =
  let hull = st.points |> Geometry.convex_hull in
  let sects =
    poly_edges target |> List.map (fun (v1, v2) ->
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
  let ds1 = sects |> List.filter_map (apply_dissection target hull Positive) in
  let ds2 = sects |> List.filter_map (apply_dissection target hull Negative) in
  choose_best_dissection (ds1 @ ds2)

let validate_size ~offset (st: State.t) : bool =
  let sol = Solution.recover st offset in
  if Solution.size sol > max_solution_size then
    (Printf.eprintf "Reached maximum solution size!\n%!";
     false)
  else
    true

let approx ~iterations ~dissections ~target ~offset : State.t =
  Printf.eprintf "Solving using \"approx\" strategy \
                  (iterations: %d, dissections: %d)...\n%!"
    iterations dissections;

  let rec iter n (st: State.t) : State.t =
    Printf.eprintf "Iteration %d (area %s)...\n%!" n (string_of_num st.area);
    State.draw target st;
    if n = iterations then
      st
    else match apply_approx_dissection ~dissections target st with
      | Some next_st ->
          if validate_size next_st ~offset then
            iter (Pervasives.succ n) next_st
          else
            st
      | None ->
          Printf.eprintf "Couldn't make another step!\n";
          st
  in
  iter 0 State.default

let exact ~iterations ~dissections ~target ~offset : State.t =
  Printf.eprintf "Solving using \"exact\" strategy \
                  (iterations: %d, dissections: %d)...\n%!"
    iterations dissections;

  let rec iter n (st: State.t) : State.t =
    Printf.eprintf "Iteration %d (area %s)...\n%!" n (string_of_num st.area);
    State.draw target st;
    if n = iterations then
      st
    else match apply_exact_dissection target st with
      | Some next_st ->
          if validate_size next_st ~offset then
            iter (Pervasives.succ n) next_st
          else
            st
      | None ->
          Printf.eprintf "Unable to dissect by edge of the target.\n%!";
          match apply_approx_dissection ~dissections target st with
            | Some next_st ->
                if validate_size next_st ~offset then
                  iter (Pervasives.succ n) next_st
                else
                  st
            | None ->
                Printf.eprintf "Couldn't make another step!\n";
                st
  in
  iter 0 State.default
