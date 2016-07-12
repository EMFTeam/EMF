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

my $VERSION = "1.3.2";

my $DEFAULT_N      = 64;
my $DEFAULT_STRIDE = 5;
my $DEFAULT_OFFSET = 15;

# NOTE: returns law modifier as function of law index (starting at 0)
sub scale_function {
	my $i = shift;
	return 1 / ( 1 + log(1 + $i/36.75) ) - 1;
}

my %targets = (
	laws => \&print_laws,
	i18n => \&print_i18n,
	events => \&print_events,
	effects => \&print_effects,
);

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


sub print_effects {
	print <<EOS;
# -*- ck2.scripted_effects -*-

################################
##  DYNLEVY SCRIPTED EFFECTS  ##
################################

# Dynamic levy law scaling with realm_size (event-driven demesne laws): internal support effects
# Also, see emf_cb_effects.txt for some CB helpers related to major revolts.

emf_dynlevy_update_effect = {
	hidden_tooltip = { character_event = { id = emf_dynlevy.20 } }
}

# Used in [primary] title scope
emf_dynlevy_remove_effect = {
	hidden_tooltip = {
EOS

	for my $i (0..$opt_n-1) {
		print "\t\trevoke_law = dynlevy${i}_0\n"
	}

	print <<EOS;
	}
}
EOS
}


####
	
sub print_laws {
	print <<EOS;
# -*- ck2.laws -*-

################################
##        DYNLEVY LAWS        ##
################################

# Dynamic levy law scaling with realm_size (event-driven demesne laws)

EOS

	print_params();

	print "law_groups = {\n";
	
	for my $i (0..$opt_n-1) {
		print "\tdynlevy$i = { law_type = realm }\n";
	}
		
	print "}\n\n";

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
EOS

		if ($i == 0) {
			print <<EOS;
			NOT = { tier = BARON }
			temporary = no
			OR = {
				tier = COUNT # Counts always use the default law
				has_law = $law
				holder_scope = { has_law = $law } # Even if title doesn't have the law, allow it to be copied
			}
EOS
		}
		else {
			print <<EOS;
			higher_tier_than = COUNT
			temporary = no
			OR = {
				has_law = $law
				holder_scope = { has_law = $law } # Even if title doesn't have the law, allow it to be copied
			}
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
			emf_dynlevy_remove_effect = yes
		}

		castle_vassal_max_levy = $mod_str
		castle_vassal_min_levy = $mod_str
		city_vassal_max_levy = $mod_str
		city_vassal_min_levy = $mod_str
		temple_vassal_max_levy = $mod_str
		temple_vassal_min_levy = $mod_str
		tribal_vassal_max_levy = $mod_str
		tribal_vassal_min_levy = $mod_str
EOS

		print "\t}\n";
	}

	print "}\n";
}


####

sub print_events {
	print <<EOS;
# -*- ck2.events -*-

########################################
##      DYNLEVY EVENTS (CODEGEN)      ##
########################################

# Dynamic levy law scaling with realm_size (event-driven demesne laws)

EOS

	print_params();
	print <<EOS;
namespace = emf_dynlevy


# emf_dynlevy.20
# Scale a character's primary titles' levy laws by their realm_size
#
# This is event is called from many different trigger sources, mostly
# title transfer on_action handlers. It is also called by a variety of CB
# code.
#
# Uses a perfect binary search of the covered realm_size range to reduce
# the number of evaluations necessary to reach the correct law to pass.
# Currently it takes at most log2 64 = 6 realm_size calls to reach the
# correct effect to execute. Uses the new break syntax in CKII 2.3 to
# optimistically exit the search once the correct realm_size range is found.
#
# TODO: In CKII 2.6, we should be able to use a simple export_to_variable of
# realm_size here, although we will still have to do a binary search of the
# variable's value to find the right law to apply for a given realm_size.
character_event = {
	id = emf_dynlevy.20
	
	is_triggered_only = yes
	hide_window = yes
	
	only_rulers = yes
	
	immediate = {
		primary_title = {
			if = {
				limit = {
					OR = {
						tier = BARON
						temporary = yes # E.g., rebel leader
					}
				}
				emf_dynlevy_remove_effect = yes
				break = yes
			}
			if = {
				limit = {
					tier = COUNT
					NOT = { has_law = dynlevy0_0 }
				}
				add_law = dynlevy0_0
				break = yes
			}
		}
EOS

	print_search_tree(
		0, # general case
		0,
		$opt_n,
		2); # start with an indent level of 2

	print <<EOS;
	}
}


# emf_dynlevy.23
# Maintenance version of emf_dynlevy.20, called on annual pulse
character_event = {
	id = emf_dynlevy.23
	
	is_triggered_only = yes
	hide_window = yes
	
	only_playable = yes
	
	trigger = {
		higher_tier_than = COUNT # For maintenance, we only care about tier >= DUKE.
		primary_title = { temporary = no }
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

			print "\t" x $tab, "primary_title = {\n";
			++$tab;
			print "\t" x $tab, "if = {\n";
			++$tab;
			print "\t" x $tab, "limit = { NOT = { has_law = $law } }\n";
			print "\t" x $tab, "add_law = $law\n";
			print "\t" x $tab, "break = yes\n";
			--$tab;
			print "\t" x $tab, "}\n"; # /if
			--$tab;
			print "\t" x $tab, "}\n"; # /primary_title
		
			# Set all titles greater than or equal to primary-tier to correct law
			# print "\t" x $tab, "primary_title = {\n";
			# ++$tab;
			# print "\t" x $tab, "ROOT = {\n";
			# ++$tab;
			# print "\t" x $tab, "any_demesne_title = {\n";
			# ++$tab;
			# print "\t" x $tab, "limit = {\n";
			# ++$tab;
			# print "\t" x $tab, "higher_tier_than = COUNT\n";
			# print "\t" x $tab, "NOT = { lower_tier_than = PREVPREV }\n";
			# print "\t" x $tab, "NOT = { has_law = $law }\n";
			# --$tab;
			# print "\t" x $tab, "}\n"; # /limit
			# print "\t" x $tab, "add_law = $law\n";
			# --$tab;
			# print "\t" x $tab, "}\n"; # /any_demesne_title
			# --$tab;
			# print "\t" x $tab, "}\n"; # /ROOT
			# --$tab;
			# print "\t" x $tab, "}\n"; # /primary_title
			
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
	print "\t" x $tab, "limit = { NOT = { realm_size = $rs } }\n";
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
		
		print "${law_group};Levy Efficiency$eol";
		print "${law_group}_desc;As your realm grows, your liege levy will grow with it. But by how much?$eol";
		print "${law};$mod_str Realm Levy-Raising Efficiency$eol";
		print "${law}_option;$mod_str$eol";
		print "${law}_desc;In a decentralized feudal system, rulers of large realms are less efficient at raising liege levies than rulers of smaller realms. Demesne levies are unaffected.\\n\\nSmaller realms pack a harder punch per capita, all else being equal. For larger realms to compete per capita, they inevitably must centralize. See the EMF manual for details on levy efficiency.$eol";
	}
}
