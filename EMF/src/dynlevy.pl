#!/usr/bin/perl

# Copyright (C) 2014 Matthew D. Hall <zijistark@gmail.com>
#
# Free for personal modification. Any redistribution, even
# without modification, of this program or its output is
# expressly forbidden without the consent of the author.


use strict;
use warnings;
use Carp;
use Getopt::Long qw(:config gnu_getopt);

my $VERSION = "1.0.0";

my $DEFAULT_N      = 64;
my $DEFAULT_STRIDE = 5;
my $DEFAULT_OFFSET = 15;

# NOTE: returns law modifier as function of law index (starting at 0)
sub scale_function {
	my $i = shift;
	return 1 / ( 1 + log(1 + $i/36.75) ) - 1;
}

####

my $opt_n = $DEFAULT_N;
my $opt_stride = $DEFAULT_STRIDE;
my $opt_offset = $DEFAULT_OFFSET;
my $opt_target;

GetOptions(
	'n|N=i' => \$opt_n,
	'stride=i' => \$opt_stride,
	'offset=i' => \$opt_offset,
	'h|help|usage' => \&usage,
	't|target=s' => \$opt_target) or usage();

unless ($opt_target) {
	print STDERR "You must specify a codegen target with --target.  See usage info below:\n\n";
	usage();
}

$opt_target = "\L$opt_target"; # Case-insensitive

my %targets = (
	laws => \&print_laws,
	i18n => \&print_i18n,
	events => \&print_events,
);

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
			Number of distinct classes of dynamic levy laws [$DEFAULT_N]
			Currently is assumed to be a power of 2.
			
		--stride <holdings/law>
			Number of holdings covered by a single class on the curve [$DEFAULT_STRIDE]
			
		--offset <max. holdings for exemption>
			The realm_size-scaled curve starts here. [$DEFAULT_OFFSET]
			
		--help, --usage  Show this help/usage information.
		
		NOTE: The law modifier scaling function is hard-coded near the top of the
		      script and does assume the default of N=$DEFAULT_N.
	
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
	print "#   range=[".sprintf("%0.03f",scale_function($opt_n-1)).", ".sprintf("%0.03f",scale_function(0))."]\n";
	print "#   curve: m = 1 / (1 + ln(1 + i/36.75)) - 1 for levy law modifier m and dynlevy law index i\n";
	print "\n";
}


####
	
sub print_laws {
	print "# emf_dynlevy_laws\n";
	print "# Dynamic levy law scaling with realm_size (demesne laws)\n\n";
	print_params();

	print "laws = {\n";

	for my $i (0..$opt_n-1) {
		my $mod = scale_function($i);
		my $mod_str = sprintf("%0.03f", $mod);

		my $law_group = "dynlevy$i";
		my $law = $law_group."_0";
		
		my $is_default = '';
		
		if ($i == 0) {
			$is_default = "\n\t\tdefault = yes";
		}
		
		print <<EOS;
	$law = {
		group = $law_group$is_default

		potential = {
			not = { tier = baron }
EOS

		if ($i == 0) {
			print <<EOS;
			or = {
				tier = count
				has_law = $law
			}
EOS
		}
		else {
			print <<EOS;
			has_law = $law
EOS
		}

		print <<EOS;
		}
		allow = {
		}
		revoke_allowed = {
			always = no
		}
		ai_will_do = {
			factor = 0
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
EOS

		if ($i == 0) {
			print "\t\t\t\t# Turns out, due to Paradox script's severe overhead, it's faster (and simpler)\n";
			print "\t\t\t\t# to just revoke all the other ",$opt_n-1, " laws directly than use a binary search\n";
			print "\t\t\t\t# to precisely locate the correct, single law to revoke in O(lg N) time. revoke_law\n";
			print "\t\t\t\t# should be just as fast clr_character_flag anyhow.\n\n";
		}
		
		for my $j (0..$opt_n-1) {
			print "\t\t\t\trevoke_law = dynlevy${j}_0\n"
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
	print "# Dynamic levy law scaling events (code-generated)\n";
	print_params();
	print <<EOS;
namespace = emf_dynlevy


# emf_dynlevy.20
# Scale all of a character's primary-tier titles' levy laws by realm_size
#
# This is event is called from many different trigger sources, mostly
# title transfer on_action handlers (but always batch-optimized, deferred
# by a game day in on_action cases). It is also called by a variety of CB
# code.
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


# emf_dynlevy.21
# on_new_holder event for immediate levy law application upon title creation
#
# Like emf_dynlevy.20, the approach is to use a binary search tree expansion upon
# realm_size to determine the correct levy law to apply to the target title.
character_event = {
	id = emf_dynlevy.21
	desc = HIDE_EVENT
	hide_window = yes
	is_triggered_only = yes

	trigger = {
		not = { FROMFROM = { always = yes } }
		FROM = { higher_tier_than = count }
		
		# Only titles of primary-tier or higher
		primary_title = {
			not = { higher_tier_than = FROM }
		}
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


# emf_dynlevy.22
# Debug event for identifying the dynlevy law(s) applied to a character
character_event = {
	id = emf_dynlevy.22
	desc = emf_dynlevy.22.desc
	picture = GFX_evt_battle
	is_triggered_only = yes
	
	option = {
		name = OK

EOS

	for my $i (0..$opt_n-1) {
		my $law = "dynlevy${i}_0";
		print <<EOS;
		if = {
			limit = { has_law = $law }
			custom_tooltip = { text = emf_ctt_dbg_$law }
		}
EOS
	}

	print <<EOS;
	}
}


# emf_dynlevy.23
# Maintenance version of emf_dynlevy.20, called on annual pulse
character_event = {
	id = emf_dynlevy.23
	desc = HIDE_EVENT
	hide_window = yes
	is_triggered_only = yes
	
	only_playable = yes
	
	trigger = {
		higher_tier_than = count # For maintenance, we only care about tier >= DUKE.
	}
	
	immediate = {
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


# emf_dynlevy.24
# Debug / fix event in case somebody should run into the mysterious, once-sighted
# cosmetic bug of multiple dynlevy laws appearing to be activated at the same
# time. [Not even sure it works, as I haven't been able to repeat this mystery.]
character_event = {
	id = emf_dynlevy.24
	desc = HIDE_EVENT
	hide_window = yes
	is_triggered_only = yes
	
	immediate = {
	
		# Clear  all dynlevy laws from all tier >= DUKE titles
		any_demesne_title = {
			limit = { higher_tier_than = count }
			
EOS

	for my $i (0..$opt_n-1) {
		print "\t" x 3, "revoke_law = dynlevy${i}_0\n";
	}

	print <<EOS;
		}
		
		# Reset appropriate law
		character_event = { id = emf_dynlevy.20 }
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
		
		my $lg = "dynlevy$min";
		my $law = $lg."_0";
		
		if ($mode == 0) {
		
			# Set all titles greater than or equal to primary-tier to correct law
			print "\t" x $tab, "primary_title = {\n";
			++$tab;
			print "\t" x $tab, "ROOT = {\n";
			++$tab;
			print "\t" x $tab, "any_demesne_title = {\n";
			++$tab;
			print "\t" x $tab, "limit = {\n";
			++$tab;
			print "\t" x $tab, "higher_tier_than = count\n";
			print "\t" x $tab, "not = { lower_tier_than = PREVPREV }\n";
			print "\t" x $tab, "not = { has_law = $law }\n";
			--$tab;
			print "\t" x $tab, "}\n"; # /limit
			print "\t" x $tab, "add_law = $law\n";
			--$tab;
			print "\t" x $tab, "}\n"; # /any_demesne_title
			--$tab;
			print "\t" x $tab, "}\n"; # /ROOT
			--$tab;
			print "\t" x $tab, "}\n"; # /primary_title
			
			my $rsz_idx = $min+1;

			if ($min > 0) {
				# Set a variable indicating law tier (a way to programatically track realm size)
				# print "\t" x $tab, "set_variable = { which = rsz_idx value = $rsz_idx }\n";
			}
			else { # Minimum realm size case
			
				# If no longer even ruling a landed realm...
				# print "\t" x $tab, "if = {\n";
				# ++$tab;
				# print "\t" x $tab, "limit = { not = { realm_size = 1 } }\n";
				
				# # Reset variable indicating law tier (variable goes poof)
				# print "\t" x $tab, "set_variable = { which = rsz_idx value = 0 } # Poof!\n";
				
				# --$tab;
				# print "\t" x $tab, "}\n"; # /if

				# # Otherwise...
				# print "\t" x $tab, "if = {\n";
				# ++$tab;
				# print "\t" x $tab, "limit = { realm_size = 1 }\n";
				
				# # Set variable as normal
				# print "\t" x $tab, "set_variable = { which = rsz_idx value = $rsz_idx }\n";
				
				# --$tab;
				# print "\t" x $tab, "}\n"; # /if
			}
		}
		elsif ($mode == 1) {
			print "\t" x $tab, "FROM = { add_law = $law }\n";
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
	print "#CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x\n";
	my $eol = ";;;;;;;;;;;;;x\n";
	print "emf_dynlevy.22.desc;Hover over the event option for my levy efficiency law. If no tooltip appears, I have no dynlevy law applied.$eol";
	
	for my $i (0..$opt_n-1) {
		my $mod = scale_function($i) + 1;
		my $mod_str = sprintf("%0.01f", $mod*100);
		$mod_str =~ s/0+$//;
		$mod_str =~ s/\.$//;
		$mod_str .= '%';
		my $law_group = "dynlevy$i";
		my $law = $law_group."_0";
		
		my $min_rs = ($i == 0) ? 1 : ($opt_offset + $opt_stride*$i);
		my $max_rs = ($i == $opt_n-1) ? "INF" : ($opt_offset + $opt_stride*($i+1)-1);
		
		print "emf_ctt_dbg_$law;Dynamic Levy Law: §Y$law§!\\nLevy Efficiency: §Y$mod_str§!\\nRealm Size: §Y$min_rs§! through §Y$max_rs§!\\n$eol";
		print "${law_group};Levy Efficiency$eol";
		print "${law_group}_desc;As your realm grows, your liege levy will grow with it. But by how much?$eol";
		print "${law};$mod_str Realm Levy-Raising Efficiency$eol";
		print "${law}_option;$mod_str$eol";
		print "${law}_desc;In a decentralized feudal system, rulers of large realms are less efficient at raising liege levies than rulers of smaller realms. Demesne levies are unaffected.\\n\\nSmaller realms pack a harder punch per capita, all else being equal. For larger realms to compete per capita, they inevitably must centralize. See the EMF manual for details on levy efficiency.$eol";
	}
}
