
type t = silhouette * skeleton
and silhouette = Geometry.polygon list
and skeleton = Geometry.segment list


val read_file: fname: string -> t
