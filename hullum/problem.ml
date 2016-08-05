
open Batteries


type t = silhouette * skeleton
and silhouette = Geometry.polygon list
and skeleton = Geometry.segment list


let read_file ~fname : t =
  let cin = Q.Scanf.Scanning.open_in fname in
  let scan_int () = Scanf.bscanf cin "%d " identity in

  let scan_vertex () : Geometry.vertex =
    Scanf.bscanf cin "%s " (fun s0 ->
      let (s1, s2) = String.split ~by:"," s0 in
      (Num.num_of_string s1, Num.num_of_string s2))
  in

  let npolys = scan_int () in
  let silhouette = List.init npolys (fun _ ->
    let nvertex = scan_int () in
    List.init nvertex (fun _ ->
      scan_vertex ()))
  in

  let nsegments = scan_int () in
  let skeleton = List.init nsegments (fun _ ->
    let a = scan_vertex () in
    let b = scan_vertex () in
    (a, b))
  in

  (silhouette, skeleton)
