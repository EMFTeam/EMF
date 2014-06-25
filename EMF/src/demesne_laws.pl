#!/usr/bin/perl

# Copyright (C) 2014 Matthew D. Hall <zijistark@gmail.com>
#
# Free for personal modification. Any redistribution, even
# without modification, of this program or its output is
# expressly forbidden without the consent of the author.

my $VERSION = "0.1.1";

my $opt = {
	max_total_levy      => 0.5, # Maximum levy, of all possible settings, for any vassal class is always this
	castle_tax_per_levy => 0.6, # If you trade-off -100% feudal levies, you'll get 60% ROI on max. potential tax
	temple_tax_per_levy => 0.8, # If you trade-off -100% levies, you'll get 80% ROI on max. potential tax
	city_tax_per_levy   => 1.0, # If you trade-off -100% levies, you'll get 100% ROI on max. potential tax
	opinion_offset => 4,
	opinion_slope  => -8,
	default_laws => {
		feudal_obligations => 0,
		feudal_slider      => 0,
		temple_obligations => 0,
		temple_slider      => 2,
		city_obligations   => 0,
		city_slider        => 4,
		iqta_obligations   => 0,
		iqta_slider        => 4,
	},
};


#####


use strict;
use warnings;

print_laws();
exit 0;


####

sub print_params {
	print "# Written by zijistark via demesne_laws.pl v$VERSION on ".localtime." (Pacific)\n";
	print "# Code generation parameters:\n";
	print "#   max_total_levy=$opt->{max_total_levy}\n";
	for my $t ( qw( castle temple city ) ) {
		print "#   ${t}_tax_per_levy=".$opt->{"${t}_tax_per_levy"}."\n";
	}
	print "#   opinion_offset=$opt->{opinion_offset}\n";
	print "#   opinion_slope=$opt->{opinion_slope}\n";
	print "\n";
}

####

sub print_laws {
	print <<EOS;
# demesne_laws (set upon primary title, apply to whole demesne)
# Vassal levy/tax focus/obligations sliders
#
EOS

	print_params();
	
	print "laws = {";

	for my $type ( qw( castle temple city iqta ) ) {

		my $tax_per_levy = $opt->{ get_real_type($type).'_tax_per_levy' };
		
		print "\n\n\t# \U$type FOCUS\n";
		
		# focus
		for my $i (0..4) {
			my $levy_delta = $i * $opt->{max_total_levy}/20;
			my $levy = $opt->{max_total_levy}/5 - $levy_delta;
			my $tax = $tax_per_levy * $levy_delta;
			print_law(1, $type, $i, $levy, $tax);
		}

		print "\n\t# \U$type OBLIGATIONS\n";
		
		# obligations
		for my $i (0..4) {
			my $levy = $i * $opt->{max_total_levy}/5;
			my $tax = $tax_per_levy * $levy;
			print_law(0, $type, $i, $levy, $tax);
		}
	}
	
	print "}\n";
}



####


sub print_law {
	my $focus   = shift;
	my $type    = shift;
	my $level   = shift;
	my $levy    = shift;
	my $tax     = shift;
	
	my ($vtype, $class, $law_group, $law, $default, $muslim) = get_law_info($type, $level, $focus);
	
	$levy = sprintf("%5.3f", $levy);
	$tax  = sprintf("%5.3f", $tax);
	
	my $opinion_effect = '';
	
	unless ($focus) {
		$opinion_effect .= "\t\t${class}_opinion = ".get_opinion($level);
	}
	
	$default = ($default) ? "\t\tdefault = yes" : '';
	$default .= "\n" if $opinion_effect;
	
	my $muslim_holder = "holder_scope = { religion_group = muslim }";
	$muslim_holder = "not = { $muslim_holder }" unless $muslim;
	
	my $law_down = '';
	my $law_up = '';
	my $law_reqs = '';
	
	my $tabs = 3;
	
	if ($level > 0 && $level < 4) {
		$law_reqs .= ("\t" x $tabs)."or = {\n";
		++$tabs;
	}
	
	if ($level > 0) {
		$law_down = $law_group.'_'.($level-1);
		$law_reqs .= ("\t" x $tabs)."has_law = $law_down\n";
	}
	
	if ($level < 4) {
		$law_up = $law_group.'_'.($level+1);
		$law_reqs .= ("\t" x $tabs)."has_law = $law_up\n";
	}

	if ($level > 0 && $level < 4) {
		--$tabs;
		$law_reqs .= ("\t" x $tabs)."}\n";
	}
	
	chop $law_reqs;
	
	my $revoke_laws = '';
	
	for my $i (0..4) {
		next if $i == $level;
		$revoke_laws .= ("\t" x 4)."revoke_law = ".$law_group.'_'.$i."\n";
	}
	
	chop $revoke_laws;
	
	my $ai_will_do = (!$focus && $level < 3) ? 1 : 0;
	
	print <<EOS;
	$law = {
		group = $law_group
$default$opinion_effect

		potential = {
			not = { tier = baron }
			$muslim_holder
		}
		allow = {
			hidden_tooltip = { temporary = no }
$law_reqs
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = $ai_will_do
EOS

		if ($ai_will_do && $level == 0) {
			print <<EOS;
			modifier = {
				factor = 0
				not = { holder_scope = { trait = charitable } }
			}
EOS
		}
		elsif ($ai_will_do && $level == 1) {
		print <<EOS;
			modifier = {
				factor = 0
				not = { holder_scope = { trait = charitable } }
				has_law = $law_up
			}
			modifier = {
				factor = 0
				holder_scope = { trait = charitable }
				has_law = $law_down
			}
EOS
		}
		elsif ($ai_will_do && $level == 2) {
		print <<EOS;
			modifier = {
				factor = 0
				not = { holder_scope = { trait = greedy } }
				has_law = $law_down
			}
			modifier = {
				factor = 0
				holder_scope = { trait = greedy }
				has_law = $law_up
			}
EOS
		}

		print <<EOS;
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
$revoke_laws
			}
		}
		
		${vtype}_vassal_max_levy = $levy
		${vtype}_vassal_tax_modifier = $tax
	}
EOS
}


sub print_obligations_law {
	my $type    = shift;
	my $level   = shift;
	my $levy    = shift;
	my $tax     = shift;
	
	my ($vtype, $class, $law_group, $law, $default, $muslim) = get_law_info($type, 0);
	
print <<EOS;

EOS
}


sub get_class_name {
	my $type = shift;
	return ($type eq 'castle' || $type eq 'iqta') ? 'feudal' : $type;
}


sub get_real_type {
	my $type = shift;
	return ($type eq 'iqta') ? 'castle' : $type;
}


sub get_law_info {
	my $type = shift;
	my $level = shift;
	my $focus = shift || 0;
	my $class = get_class_name($type);
	my $law_group = ( ($type ne 'iqta') ? get_class_name($type) : 'iqta' ).'_'.( ($focus) ? 'slider' : 'obligations' );
	my $law = $law_group.'_'.$level;
	my $default = ($opt->{default_laws}{$law_group} == $level);
	my $muslim = ($type eq 'iqta');
	return (get_real_type($type), $class, $law_group, $law, $default, $muslim);
}


sub get_opinion {
	my $level = shift;
	return $level*$opt->{opinion_slope} + $opt->{opinion_offset};
}
