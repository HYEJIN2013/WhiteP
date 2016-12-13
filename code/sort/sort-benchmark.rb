#!/usr/bin/ruby

require 'benchmark'

ary = []
1000.times { 
  ary << {:bar => rand(1000)} 
}

n = 500
Benchmark.bm(20) do |x|
  x.report("sort")               { n.times { ary.sort{ |a,b| b[:bar] <=> a[:bar] } } }
  x.report("sort reverse")       { n.times { ary.sort{ |a,b| a[:bar] <=> b[:bar] }.reverse } }
  x.report("sort_by -a[:bar]")   { n.times { ary.sort_by{ |a| -a[:bar] } } }
  x.report("sort_by a[:bar]*-1") { n.times { ary.sort_by{ |a| a[:bar]*-1 } } }
  x.report("sort_by.reverse!")   { n.times { ary.sort_by{ |a| a[:bar] }.reverse } }
end

                          user     system      total        real
sort                  3.960000   0.010000   3.970000 (  3.990886)
sort reverse          4.040000   0.000000   4.040000 (  4.038849)
sort_by -a[:bar]      0.690000   0.000000   0.690000 (  0.692080)
sort_by a[:bar]*-1    0.700000   0.000000   0.700000 (  0.699735)
sort_by.reverse!      0.650000   0.000000   0.650000 (  0.654447)
