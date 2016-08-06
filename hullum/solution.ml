
open Batteries
open Utils
open Printf
open Geometry


type facet = polygon

type t =
  {
    vertexes: (vertex * vertex) list;
    facets: facet list;
  }


module Vertex = struct
  type t = vertex
  let compare = Geometry.compare_vertex
end

module VSet = Set.Make (Vertex)
module VMap = Map.Make (Vertex)


let get_flipped_facet (l: line) (st: State.t) (prev: State.t) : facet =
  let moved = collect (fun push ->
    st.points |> List.iter (fun v ->
      if Geometry.line_vertex_relation l v = `OnLine then
        push v);
    let set = VSet.of_list st.points in
    prev.points |> List.iter (fun v ->
      if not (VSet.mem v set) then
        push v))
  in
  Geometry.convex_hull moved


let recover (st: State.t) : t =
  let facets = ref [ Geometry.convex_hull st.points ] in

  let vmap = ref VMap.empty in
  st.points |> List.iter (fun v ->
    vmap := VMap.add v v !vmap);

  let add_flipped_facet (l: line) f =
    let f =
      f |> List.map (fun v ->
        match VMap.Exceptionless.find v !vmap with
          | Some vdest ->
              let v' = Geometry.flip_vertex l v in
              vmap := VMap.add v' vdest !vmap;
              v'
          | None ->
              vmap := VMap.add v v !vmap;
              let v' = Geometry.flip_vertex l v in
              vmap := VMap.add v' v !vmap;
              v')
    in
    facets := f :: !facets
  in

  let rec iter (st: State.t) =
    st.prev |> Option.may (fun (line, st_prev) ->
      let f1 = get_flipped_facet line st st_prev in
      let f1' = flip_poly line f1 in
      !facets |> List.iter (fun f2 ->
        Geometry.intersect_hulls f1' f2 |> Option.may (fun f3 ->
          add_flipped_facet line f3));
      iter st_prev)
  in
  iter st;

  let vertexes =
    let valid = !facets |> List.concat |> VSet.of_list in
    collect (fun push ->
      !vmap |> VMap.iter (fun vsrc vdest ->
         if VSet.mem vsrc valid then
           push (vsrc, vdest)))
  in
  { vertexes; facets = !facets }


let write_file ~fname (sol: t) =
  let cout = if fname = "stdout" then stdout else open_out fname in

  let print_vertex (x, y) =
    fprintf cout "%s,%s\n" (Num.string_of_num x) (Num.string_of_num y)
  in

  let (source, dest) = List.split sol.vertexes in

  fprintf cout "%d\n" (List.length source);
  source |> List.iter print_vertex;

  fprintf cout "%d\n" (List.length sol.facets);
  sol.facets |> List.iter (fun f ->
    let f = List.tl f in
    fprintf cout "%d " (List.length f);
    f |> List.iter (fun v ->
      let (i, _) = List.findi (fun i v' ->
        Geometry.compare_vertex v v' = 0) source in
      fprintf cout "%d " i);
    fprintf cout "\n");

  dest |> List.iter print_vertex
