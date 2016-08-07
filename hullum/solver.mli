
val approximate:
  iterations: int ->
  target: Geometry.polygon ->
  offset: Geometry.fit_offset ->
  State.t

val exact:
  iterations: int ->
  target: Geometry.polygon ->
  offset: Geometry.fit_offset ->
  State.t
