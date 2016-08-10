
open Utils
open Batteries


type t =
  {
    points: Geometry.vertex list;
    area: Geometry.area;
    prev: (Geometry.line * t) option;
  }


let square =
  [ (num_0, num_0); (num_0, num_1); (num_1, num_0); (num_1, num_1) ]

let default =
  {
    points = square;
    area = num_1;
    prev = None;
  }


let get_lines (st: t) =
  collect (fun push ->
    let rec iter (st: t) =
      st.prev |> Option.may (fun (line, st) ->
        push line;
        iter st)
    in
    iter st)

let draw ~target (st: t) =
  if !Drawing.enabled then
    let open Drawing in
    draw [
      (Poly target, Graphics.green);
      (Poly (Geometry.convex_hull st.points), Graphics.white);
      (LineList (get_lines st), Graphics.red);
    ]
