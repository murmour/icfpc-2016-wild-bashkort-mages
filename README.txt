Salutations!

The proud nation of Bashkortostan warmly welcomes you into the sacred tarball
of our submission to the ICFP Programming Contest 2016. Feel at ease.

The legendary champions are:
  Damir Akhmetzyanov (linesprower@gmail.com),
  Max Mouratov (mmouratov@gmail.com),
  Artem Ripatti (ripatti@inbox.ru).

As you surely know, Bashkortostan is the world leader in technology,
computer science and algebraic topology. With this submission, we expect to
cement the positions of our motherland in the exciting new field of
computational geometry. Don't worry: resistance is very obviously futile.

From young age, our children are trained in the art of convex decomposition
of polyhedra, computing barycenters of weighted point sets, and triangulated
surface mesh skeletonization; hoping, that one day they'd be tasked with a
crucially important problem of tile setting, paper folding, or maybe even trim
carpentry. And now, this day has finally come for us, WILD BASHKORT MAGES,
thanks to you, the authors of this wonderful puzzle. We have immensely enjoyed
solving it, and the three days have passed in a blink. This adventure will
forever imprint in our memory: it was saturated with the purest essence of fun.

As the puzzle in question is quite... puzzling, our scientists have devised
numerous mechanized contraptions that have aided the humans in their crusade.
Each piece of machinery is located in a separate folder, but the true power of
the technology is only unlocked by combining the pieces in the right order and
flipping the correct switches. Too bad, the knowledge of this has long time
faded into oblivion, as many hours have passed since the completion of the
contest, and the sleep-deprived brains are so bad at storing details.

Still, here are some hints:

BORDERSEARCHER is the staple of most of our solutions. First, the program tries
to find sequences of edges that make up a length of 1 (or, more generally, 1/n).
It then tries to combine four of such sequences so they can be used to form the
border of the original square. Various tests are used to reduce the search
space. Also, the program attempts to find edges that connect border points to
interior points so their position can be reconstructed on the original square
from the positions of border vertices and lengths of the edges. As the solver is
written in C++ and uses floating point arithmetic, the input is preprocessed so
that destination points are shifted towards the origin and converted to doubles.

VISUALIZER contains lots of stuff written in Python along with two actual
visualizers. The first one (visual.py) is for input problems, the other
(facet_vis.py) is used to visualize the produced solutions at various stages.
VISUALIZER also contains the preprocessor for BORDERSEARCHER that tries to
reconstruct the solution from the BORDERSEARCHER's output (it tries different
sets of edges in the complicated case where one destination point produces
several original points, or when more than two destination points lie on the
same line). After the vertex positions and edges are reconstructed, an attempt
is made to reconstruct the facets, and if it fails, another set of
edges/paths/whatever is tried until certain limits are reached or a solution is
found. Then follows an optional step of "unfolding" if a 1xN rectangle was
considered. A solution optimizer (rearranging vertex numbers, removing unneeded
vertices) is also included.

CLIENT is our interface to the REST API of the contest server.
It also handles running the solvers in batch mode.

HULLUM is a solver for kinds of problems where the silhouette is a convex
polygon (if it's not, then the solver assumes otherwise by computing the hull).
First, it fits the silhouette into the unit square, which is a convex polygon
itself. Then, it attempts to reduce the exterior hull by splitting it either
over the edges of the silhouette or over some line that minimizes the area.
An invariant is maintained that the outer polygon is always convex. When
possible, the solver produces exact solutions (and does so for more than 700
problems). Otherwise, it gives an approximation. The implementation language is
OCaml, and the author (Max) believes that it was an excellent choice.

NAGIBATOR is the pinnacle of our technology -- the one that might inspire the
nation. It makes us feel proud. In a nutshell: it preprocesses problems by
trying to detect and unfold simple folds (we use a bipartite graph coloring
algorithm to detect which edges go where) and generates a simplified problem
which can be fed to BORDERSEARCHER or any other solver (e.g. HULLUM). The
obtained solution (whether perfect or not) is then postprocessed using the lines
from the preprocessing step into a solution to the original problem. We got this
thing working only about five hours before the end of the contest, but it gave
us exact solutions to hundreds of problems (including some of the nastiest).

HELMETSOLVER is a hard-coded solver for the set of "helmet-shaped" problems by
"kontur.ru". We hope they don't feel too bad about it.

PLANESOLVER is a hard-coded solver for the set of "airplane" problems by
天羽々斬. We're still scared of their unpronounceable name and hope that it
means something harmless, like "beef-flavored ramen".

RECTANGLE is the generator for the ill-fated problems that we submitted and that
have earned us an inordinately small amount of points because the idea of
refreshing the page with the scoring rules hadn't even begun to consider the
possibility of crossing our minds till the end of the contest. No, seriously: we
have actively monitored the official blog and twitter account, but there were no
news about the change, and so we are quite surprised to discover it now. A great
shame, because our problems truly are works of art -- minuscule problems that
require gigantic solutions. Lots of thought and love went into designing these,
and the author (Artem) is now very sad, as we'd have gotten much more points
(and given out much less to competitors) if we had simply submitted the problem
1 with a unit square -- even this primitive "problem" would have given us ~25
points in case 200 teams had solved it. Instead, we got fractions of a point for
each of our crazy problems, while some of the teams earned thousands on them.
For us, this was the only bad moment in the whole contest. Rant over.

OXYETHYLENE is a knot of breathy syllables -- the amalgamation of planetary evil
-- the eternal telescoping transducer of non-manifold horror and topological
disarray -- the device that no human should ever witness in action. For the
safety of our civilization (and especially the participants of ICFPC, which are
a better part of it), we've decided to remove this malicious artifact from the
sacred tarball. Rest at peace, planet.

A piece of trivia for the Russian readers: apparently, the kind of FANCY PANTS
that are usually worn with LOUBOUTINS are typically produced from OXYETHYLENE.


Regarding the Judge's Prize (our self-nomination):

We got the prize last year, in a dramatic turn of events. Frankly speaking, our
chances of getting it twice in a row are quite slim, as the history of ICFPC
doesn't know of such precedents. Still:

1) Our solvers are quite good -- they're efficient and sophisticated.
   And we're certainly some of the top dogs this time.

2) We are very much burned by the unannounced rule change mentioned in the
   RECTANGLE comment above. It affected us much more so than any other team.
   Don't you feel bad about it? :)

3) If we win the prize, we might make you a fun realtime demo for the conference
   presentation. Or we may not, if we're not in the mood. Tough call. That said,
   this year's task, being visual and poetic, seems to be perfectly suitable for
   such an endeavor -- more so than the last year's one -- so we suggest that
   you offer this project to whoever wins the prize (us or not). It might be fun.

4) We're humble and classy.

5) Thanks to us, the Earth is saved from the launch of OXYETHYLENE
   (even despite the devastating rule change mentioned in 2).

Cheers!
