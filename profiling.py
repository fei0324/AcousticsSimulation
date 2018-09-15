import cProfile
import re
import pstats

from produceWav import produceWav

# cProfile.run('produceWav("newChimeR.0127D4.stl",1,128*10**9,44100)', 'old_stats_d1')
p = pstats.Stats('old_stats_d1')
p.strip_dirs()
p.sort_stats('cumulative').print_stats(15)
p.print_stats()