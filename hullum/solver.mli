
val approximate:
  iterations: int ->
  dissections: int ->
  target: Geometry.polygon ->
  offset: Geometry.fit_offset ->
  State.t

val exact:
  iterations: int ->
  dissections: int ->
  target: Geometry.polygon ->
  offset: Geometry.fit_offset ->
  State.t
