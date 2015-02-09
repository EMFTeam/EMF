#!/usr/bin/perl

# Copyright (C) 2014-2015 Matthew D. Hall <zijistark@gmail.com>
#
# Free for personal modification. Any redistribution, even
# without modification, of this program or its output is
# expressly forbidden without the consent of the author.


use strict;
use warnings;
use Carp;
use Getopt::Long qw(:config gnu_getopt);

my $VERSION = "1.0.0";

my $DEFAULT_N      = 256;
my $DEFAULT_STRIDE = 4;

my %targets = (
	events => \&print_events,
);

####

my $opt_n = $DEFAULT_N;
my $opt_stride = $DEFAULT_STRIDE;
my $opt_target;

GetOptions(
	'n|N=i' => \$opt_n,
	'stride=i' => \$opt_stride,
	'h|help|usage' => \&usage,
	't|target=s' => \$opt_target) or usage();

unless ($opt_target) {
	print STDERR "You must specify a codegen target with --target.  See usage info below:\n\n";
	usage();
}

$opt_target = "\L$opt_target"; # Case-insensitive

unless (exists $targets{$opt_target}) {
	print STDERR "Undefined codegen target '$opt_target'.  See usage info below:\n\n";
	usage();
}

my $handler = $targets{$opt_target};
&$handler();
exit 0;


####

sub usage {	
	print <<EOF;
Usage:
	$0 [OPTIONAL PARAMETERS] -t|--target <TARGET>
	
	OPTIONAL PARAMETERS:
	
		-N <INTEGER>
			Number of distinct classes of realm size [$DEFAULT_N]
			Currently is assumed to be a power of 2.
			
		--stride <holdings/class>
			Number of holdings covered by a single realm size class [$DEFAULT_STRIDE]
			
		--help, --usage  Show this help/usage information.
	
	REQUIRED PARAMETER:
	
		-t, --target <TARGET>
			Specify target code to output by ID.
	
	Valid TARGET identifiers (case-insensitive):
EOF

	for my $t (sort keys %targets) {
		print "\t\t$t\n";
	}

	exit 0;
}


####


sub print_params {
	print "# Written by zijistark via succ_war.pl v$VERSION on ".localtime." (Pacific)\n";
	print "# Code generation parameters:\n";
	print "#   N=$opt_n (total law increments)\n";
	print "#   stride=$opt_stride (holdings per law increment)\n";
	print "\n";
}


####

sub print_events {
	print "# Event to marshal the output of the realm_size trigger into a variable (code-generated)\n\n";
	print_params();
	print <<EOS;
namespace = emf_succ_war

# emf_succ_war.1000
#
# Store the realm size class index (1-based) into the variable "rsz"
character_event = {
	id = emf_succ_war.1000
	desc = HIDE_EVENT
	hide_window = yes
	is_triggered_only = yes
	
	immediate = {
EOS

	print_search_tree(
		0,
		$opt_n,
		2); # start with an indent level of 2

	print <<EOS;
	}
}
EOS
}

sub print_search_tree {
	my $min = shift;
	my $max = shift;
	my $tab = shift;
	
	# Search [$min,$max)
	
	my $range = $max-$min;
	
	if ($range == 1) {
		# base case
		
		my $rsz = $min + 1;
		print "\t" x $tab, "set_variable = { which = rsz value = $rsz }\n";
		print "\t" x $tab, "break = yes\n";
		
		return;
	}
	
	my $mid = $min+($range/2);
	my $rs = $opt_stride*$mid;
	
	print "\t" x $tab, "if = {\n";
	++$tab;
	print "\t" x $tab, "limit = { not = { realm_size = $rs } }\n";
	print_search_tree($min, $mid, $tab);
	--$tab;
	print "\t" x $tab, "}\n";
	print "\t" x $tab, "if = {\n";
	++$tab;
	print "\t" x $tab, "limit = { realm_size = $rs }\n";
	print_search_tree($mid, $max, $tab);
	--$tab;
	print "\t" x $tab, "}\n";
}
