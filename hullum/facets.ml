
open Batteries
open Geometry
open Utils


type t = polygon


module VSet = Set.Make (struct
    type t = vertex
    let compare = compare_vertex
  end)


let get_flipped_facet (l: line) (sol: Solution.t) (prev: Solution.t) : t =
  let moved = collect (fun push ->
    sol.dest |> List.iter (fun v ->
      if Geometry.line_vertex_relation l v = `OnLine then
        push v);
    let set = VSet.of_list sol.dest in
    prev.dest |> List.iter (fun v ->
      if not (VSet.mem v set) then
        push v))
  in
  Geometry.convex_hull moved


let recover (sol: Solution.t) : t list =
  let facets = ref [] in

  let rec iter (sol: Solution.t) =
    sol.prev |> Option.may (fun (line, sol_prev) ->
      let f1 = get_flipped_facet line sol sol_prev in
      let f1' = flip_poly line f1 in
      !facets |> List.iter (fun f2 ->
        Geometry.intersect_hulls f1' f2 |> Option.may (fun f3 ->
          facets := flip_poly line f3 :: !facets));
      facets := f1 :: !facets;
      iter sol_prev)
  in
  iter sol;

  let main_facet = Geometry.convex_hull sol.dest in
  main_facet :: !facets
