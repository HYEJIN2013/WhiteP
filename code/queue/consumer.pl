use strict;
use warnings;
use Directory::Queue::Simple;

my $dirq = Directory::Queue::Simple->new(path => "/tmp/test");
my $done = 0;
for(my $name = $dirq->first(); $name; $name = $dirq->next()) {
    next unless $dirq->lock($name);
    my $data = $dirq->get($name);
    printf("Body: \"%s\"\n", $data);
    $dirq->remove($name);
    $done += 1;
}
printf("Consumed %s elements\n", $done);
