#!/usr/bin/perl

use strict;
use warnings;
use Carp;
use Getopt::Long qw(:config gnu_getopt);
use File::Spec;

my $ROOT_PATH = File::Spec->catdir(qw( /cygdrive c cygwin64 home ), $ENV{USER}, 'g');
my $LOC_PATH = File::Spec->catdir($ROOT_PATH, qw( EMF EMF localisation ));
my $LOC_FILE = File::Spec->catfile($LOC_PATH, '1_emf_cost_tooltips_codegen.csv');

my $CSV_HDR = "#CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x\r\n";
my $CSV_EOL = ";;;;;;;;;;;;;x\r\n";

my $opt_force = 0;
GetOptions('f|force' => \$opt_force) or croak;

croak "output file exists (use -f or --force to overwrite): $LOC_FILE" if (!$opt_force && -e $LOC_FILE);

my %cost = ();

add_series({ min => 0, max => 25,   step => 5   });
add_series({ min => 0, max => 100,  step => 10  });
add_series({ min => 0, max => 200,  step => 25  });
add_series({ min => 0, max => 500,  step => 50  });
add_series({ min => 0, max => 1500, step => 100 });
add_series({ min => 0, max => 2000, step => 200 });
add_series({ min => 0, max => 3000, step => 250 });
add_series({ min => 0, max => 5000, step => 500 });

open(my $fh, '>', $LOC_FILE) or croak "open: $!: $LOC_FILE";
$fh->print($CSV_HDR);

for my $cost (sort { $a <=> $b } keys %cost) {
	my $dec_cost = $cost.'.0';
	$fh->print("NEEDS_${cost}_GOLD_COST;Can afford cost of §R${dec_cost}§!¤\\n$CSV_EOL") or croak "print: $!: $LOC_FILE";
	$fh->print("HOLDER_NEEDS_${cost}_GOLD_COST;Holder can afford cost of §R${dec_cost}§!¤\\n$CSV_EOL") or croak "print: $!: $LOC_FILE";
	$fh->print("NEEDS_${cost}_PIETY_COST;Can afford cost of §R${dec_cost}§! [This.Religion.GetPietyName]\\n$CSV_EOL") or croak "print: $!: $LOC_FILE";
	$fh->print("HOLDER_NEEDS_${cost}_PIETY_COST;Holder can afford cost of §R${dec_cost}§! [This.Holder.Religion.GetPietyName]\\n$CSV_EOL") or croak "print: $!: $LOC_FILE";
	$fh->print("NEEDS_${cost}_PRESTIGE_COST;Can afford cost of §R${dec_cost}§! Prestige\\n$CSV_EOL") or croak "print: $!: $LOC_FILE";
	$fh->print("HOLDER_NEEDS_${cost}_PRESTIGE_COST;Holder can afford cost of §R${dec_cost}§! Prestige\\n$CSV_EOL") or croak "print: $!: $LOC_FILE";
}

close $fh or croak "close: $!: $LOC_FILE";

exit 0;

sub add_series {
	my $opt = shift;

	my $n = $opt->{min};
	$n += $opt->{step} if !$n;

	while ($n <= $opt->{max}) {
		$cost{$n} = 1;
		$n += $opt->{step};
	}
}
