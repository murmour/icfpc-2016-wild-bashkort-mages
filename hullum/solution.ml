
open Batteries
open Utils
open Printf
open Geometry


type facet = polygon

type t =
  {
    vertices: (vertex * vertex) list;
    facets: facet list;
  }


module Vertex = struct
  type t = vertex
  let compare = Geometry.compare_vertex
end

module VSet = Set.Make (Vertex)
module VMap = Map.Make (Vertex)


let get_unflipped_facet (l: line) (st: State.t) (prev: State.t) : facet =
  let moved = collect (fun push ->
    st.points |> List.iter (fun v ->
      if Geometry.line_vertex_orientation l v = Zero then
        push v);
    let set = VSet.of_list st.points in
    prev.points |> List.iter (fun v ->
      if not (VSet.mem v set) then
        push v))
  in
  Geometry.convex_hull moved

let flip_back_vertex lines v : vertex =
  let v = ref v in
  lines |> List.iter (fun l ->
    if Geometry.line_vertex_orientation l !v = Positive then
      v := Geometry.flip_vertex l !v);
  !v

let recover (st: State.t) (off: Geometry.fit_offset) : t =
  let facets = ref [ Geometry.convex_hull st.points ] in

  let vmap = ref VMap.empty in
  st.points |> List.iter (fun v ->
    vmap := VMap.add v v !vmap);

  let calc_flipped_facet (l: line) back_lines f : facet =
    f |> List.map (fun v ->
      let v' = Geometry.flip_vertex l v in
      begin
        match VMap.Exceptionless.find v !vmap with
          | Some vdest ->
              vmap := VMap.add v' vdest !vmap;
          | None ->
              let vdest = flip_back_vertex back_lines v in
              vmap := VMap.add v vdest !vmap;
              vmap := VMap.add v' vdest !vmap
      end;
      v')
  in

  let rec iter line_acc (st: State.t) =
    st.prev |> Option.may (fun (line, st_prev) ->
      let f1 = get_unflipped_facet line st st_prev in
      let f1' = flip_poly line f1 in
      !facets |> List.iter (fun f2 ->
        Geometry.intersect_hulls f1' f2 |> Option.may (fun f3 ->
          let f = calc_flipped_facet line line_acc f3 in
          facets := f :: !facets));
      iter (line :: line_acc) st_prev)
  in
  iter [] st;

  let vertices =
    let off' = Geometry.negate_offset off in
    let valid = !facets |> List.concat |> VSet.of_list in
    collect (fun push ->
      !vmap |> VMap.iter (fun vsrc vdest ->
         if VSet.mem vsrc valid then
           let vdest' = Geometry.apply_vertex_offset off' vdest in
           push (vsrc, vdest')))
  in
  { vertices; facets = !facets }

let print (sol: t) =
  let b = Buffer.create 1000 in
  let (source, dest) = List.split sol.vertices in

  let print_vertex (x, y) =
    bprintf b "%s,%s\n" (Num.string_of_num x) (Num.string_of_num y) in

  bprintf b "%d\n" (List.length source);
  source |> List.iter print_vertex;

  bprintf b "%d\n" (List.length sol.facets);
  sol.facets |> List.iter (fun f ->
    bprintf b "%d " (List.length f);
    f |> List.iter (fun v ->
      let (i, _) = source |> List.findi (fun i v' ->
        Geometry.equal_vertices v v') in
      bprintf b "%d " i);
    bprintf b "\n");

  dest |> List.iter print_vertex;

  Buffer.contents b

let size (sol: t) : int =
  let s = print sol in
  let ct = ref 0 in
  s |> String.iter (fun c ->
    if not (Char.is_whitespace c) then
      incr ct);
  !ct
