
open Batteries


type t = silhouette * skeleton
and silhouette = Geometry.polygon list
and skeleton = Geometry.line list


let read_file ~fname : t =
  let cin = Q.Scanf.Scanning.open_in fname in
  let scan_int () = Scanf.bscanf cin "%d " identity in

  let scan_vertex () : Geometry.vertex =
    (Num.of_int 0, Num.of_int 0)
  in

  let npolys = scan_int () in
  let silhouette = List.init npolys (fun _ ->
    let nvertex = scan_int () in
    List.init nvertex (fun _ ->
      scan_vertex ()))
  in

  let nlines = scan_int () in
  let skeleton = List.init nlines (fun _ ->
    let a = scan_vertex () in
    let b = scan_vertex () in
    (a, b))
  in

  (silhouette, skeleton)
