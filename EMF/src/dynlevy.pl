#!/usr/bin/perl

use strict;
use warnings;
use Carp;
use Getopt::Long qw(:config gnu_getopt);

my $VERSION = "0.9.2";

my %targets = (
	laws => \&print_laws,
	i18n => \&print_i18n,
	events => \&print_events,
);

my $opt_n = 64;
my $opt_stride = 4;
my $opt_offset = 24;
my $opt_modifier_max = 1.0;
my $opt_modifier_min = 0.5;

my $opt_target;

GetOptions(
	'n|N=i' => \$opt_n,
	'stride=i' => \$opt_stride,
	'offset=i' => \$opt_offset,
	'max-modifier=f' => \$opt_modifier_max,
	'min-modifier=f' => \$opt_modifier_min,
	'h|help|usage' => \&usage,
	't|target=s' => \$opt_target) or usage();
unless ($opt_target) {
	print STDERR "You must specify a codegen target with --target.  See usage info below:\n\n";
	usage();
}

$opt_target = "\L$opt_target";

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
	
		-N <num_laws>
			Number of distinct classes of dynamic levy laws [$opt_n]
			Currently is assumed to be a power of 2.
			
		--stride <holdings/law>
			Number of holdings covered by a single class on the curve [$opt_stride]
			
		--offset <max. holdings for exempt>
			The realm_size-scaled curve starts here. [$opt_offset]
			
		--max-modifier <max. vassal_levy_law modifier value>
			Maximum levy law applied by curve. [$opt_modifier_max]
			
		--min-modifier <min. vassal_levy_law modifier value>
			Minimum levy law applied by curve. [$opt_modifier_min]
			
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
	print "# Written by zijistark via dynlevy.pl v$VERSION on ".localtime." (Pacific)\n";
	print "# Code generation parameters:\n";
	print "#   N=$opt_n (total law increments)\n";
	print "#   stride=$opt_stride (holdings per law increment)\n";
	print "#   offset=$opt_offset (scaling curve starts at holdings > offset)\n";
	print "#   max_modifier=", sprintf("%0.03f", $opt_modifier_max), "\n";
	print "#   min_modifier=", sprintf("%0.03f", $opt_modifier_min), "\n";
	print "\n";
}


####
	
sub print_laws {
	print "# emf_dynlevy_laws\n";
	print "# Dynamic levy law scaling with realm_size (demesne laws)\n\n";
	print_params();

	print "laws = {\n";

	for my $i (0..$opt_n-1) {
		my $mod = ($opt_n-1-$i)*($opt_modifier_max - $opt_modifier_min)/($opt_n-1); # not the real thing, silly!
		my $mod_str = sprintf("%0.03f", $mod);

		print "\tdynlevy_$i = {\n";
		print "\t\tgroup = dynlevy\n";
		print <<EOS;

		potential = { always = no }
		revoke_allowed = { always = no }
		ai_will_do = { factor = 0 }
		ai_will_revoke = { factor = 0 }
		effect = {
			hidden_tooltip = {
EOS

		if ($i == 0) {
			print "\t\t\t\t# Turns out, due to Paradox script's severe overhead, it's faster (and simpler)\n";
			print "\t\t\t\t# to just revoke all the other ",$opt_n-1, " laws directly than use a binary search\n";
			print "\t\t\t\t# to precisely locate the correct, single law to revoke in O(lg N) time. revoke_law\n";
			print "\t\t\t\t# is apparently just as fast clr_character_flag anyhow, due to the fact that law\n";
			print "\t\t\t\t# revocation is technically an in-name-only operation (feature was never implemented).\n";
			print "\t\t\t\t# It may even be faster than clr_character_flag, because laws are tagged, IDed, and\n";
			print "\t\t\t\t# presumably just a bitset. Basically, w/ 64 laws, you'd be looking at a 64-bit\n";
			print "\t\t\t\t# integer-- clearing a single bit in it. Of course, that's not the full picture.\n\n";
		}
		
		for my $j (0..$opt_n-1) {
			next if $i == $j;
			print "\t\t\t\trevoke_law = dynlevy_$j\n"
		}

		print "\t\t\t}\n\t\t}\n";
		print <<EOS;

		castle_vassal_max_levy = $mod_str
		castle_vassal_min_levy = $mod_str
		city_vassal_max_levy = $mod_str
		city_vassal_min_levy = $mod_str
		temple_vassal_max_levy = $mod_str
		temple_vassal_min_levy = $mod_str
EOS

		print "\t}\n";
	}

	print "}\n";
}


####

sub print_events {
	print "Dynamic levy law scaling events (code-generated)\n";
	print_params();
	print <<EOS;
namespace = emf_dynlevy


# emf_dynlevy.20
# Scale all of a character's primary-tier titles' levy laws by realm_size
#
# This is event is called from a fewer different trigger sources, mostly
# title transfer on_action handlers (but always batch-optimized, deferred
# by a game day in on_action cases).
#
# Uses a perfect binary search of the covered realm_size range to reduce
# the number of evaluations necessary to reach the correct law to pass.
# Currently it takes at most log2 64 = 6 realm_size calls to reach the
# correct effect to execute.
character_event = {
	id = emf_dynlevy.20
	desc = HIDE_EVENT
	hide_window = yes
	is_triggered_only = yes
	
	immediate = {
		clr_character_flag = dynlevy_dirty # Clear batch-optimization flag

EOS

	print_search_tree(
		0, # general case
		0,
		$opt_n,
		2); # start with an indent level of 2

	print <<EOS;
	}
	
	option = { name = OK }
}


# dynlevy.21
# on_new_handler event for immediate levy law application upon title creation
#
# Like dynlevy.20, the approach is to use a binary search tree expansion upon
# realm_size to determine the correct levy law to apply to the target title.
character_event = {
	id = dynlevy.21
	desc = HIDE_EVENT
	hide_window = yes
	is_triggered_only = yes

	trigger = {
		NOT = { FROMFROM = { always = yes } }
		FROM = { higher_tier_than = count }
	}
	
	immediate = {
EOS

	print_search_tree(
		1, # title creation trigger variant
		0,
		$opt_n,
		2); # start with an indent level of 2

print <<EOS;
	}
	
	option = { name = OK }
}
EOS
}


sub print_search_tree {
	my $mode = shift;
	my $min = shift;
	my $max = shift;
	my $tab = shift;
	
	# Search [$min,$max)
	
	my $range = $max-$min;
	
	if ($range == 1) {
		# base case
		
		if ($mode == 0) {
			print "\t" x $tab, "primary_title = {\n";
			++$tab;
			print "\t" x $tab, "ROOT = {\n";
			++$tab;
			print "\t" x $tab, "any_demesne_title = {\n";
			++$tab;
			print "\t" x $tab, "limit = {\n";
			++$tab;
			print "\t" x $tab, "not = { lower_tier_than = PREVPREV }\n";
			print "\t" x $tab, "not = { has_law = dynlevy_$min }\n";
			--$tab;
			print "\t" x $tab, "}\n"; # limit
			print "\t" x $tab, "add_law = dynlevy_$min\n";
			--$tab;
			print "\t" x $tab, "}\n"; # any_demesne_title
			--$tab;
			print "\t" x $tab, "}\n"; # ROOT
			--$tab;
			print "\t" x $tab, "}\n"; # primary_title
		}
		elsif ($mode == 1) {
			print "\t" x $tab, "FROM = { add_law = dynlevy_$min }\n";
		}
		
		return;
	}
	
	my $mid = $min+($range/2);
	my $rs = $opt_offset + $opt_stride*$mid;
	
	print "\t" x $tab, "if = {\n";
	++$tab;
	print "\t" x $tab, "limit = { not = { realm_size = $rs } }\n";
	print_search_tree($mode, $min, $mid, $tab);
	--$tab;
	print "\t" x $tab, "}\n";
	print "\t" x $tab, "if = {\n";
	++$tab;
	print "\t" x $tab, "limit = { realm_size = $rs }\n";
	print_search_tree($mode, $mid, $max, $tab);
	--$tab;
	print "\t" x $tab, "}\n";
}


####

sub print_i18n {
	my $eol = ";;;;;;;;;;;;;x\n";
	print "dynlevy;Levy Efficiency$eol";
	
	for my $i (0..$opt_n-1) {
		my $mod = ($opt_n-1-$i)*($opt_modifier_max - $opt_modifier_min)/($opt_n-1); # not the real thing, silly!
		my $mod_str = sprintf("%0.01f", $mod*100);
		$mod_str =~ s/0+$//;
		$mod_str =~ s/\.$//;
		
		print "dynlevy_$i;$mod_str\%$eol";
	}
}
