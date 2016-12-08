use strict;
use warnings;
use Directory::Queue::Simple;

my $dirq = Directory::Queue::Simple->new(path => "/tmp/test");
foreach my $count (1 .. 100) {
    my $name = $dirq->add("element $count");
    printf("# added element %d as %s\n", $count, $name);
}
