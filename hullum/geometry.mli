
type vertex = Num.num * Num.num

type line = vertex * vertex

type polygon = vertex list


val convex_hull: vertex list -> vertex list
