#!/usr/bin/perl

# Copyright (C) 2014 Matthew D. Hall <zijistark@gmail.com>
#
# Free for personal modification. Any redistribution, even
# without modification, of this program or its output is
# expressly forbidden without the consent of the author.

my $VERSION = "1.0.3";

my $opt = {
	min_total_levy      => -0.1,
	max_total_levy      => 0.4,
	castle_tax_per_levy => 0.6,
	temple_tax_per_levy => 0.8,
	city_tax_per_levy   => 1.0,
	iqta_tax_per_levy   => 0.7,
	opinion_offset => 6,
	opinion_slope  => -6,
	default_laws => {
		feudal_obligations => 0,
		feudal_slider      => 0,
		temple_obligations => 0,
		temple_slider      => 2,
		city_obligations   => 0,
		city_slider        => 3,
		iqta_obligations   => 1,
		iqta_slider        => 2,
	},
};

####

use strict;
use warnings;

my $N_LAWS = 5;
my $LEVY_RANGE = $opt->{max_total_levy} - $opt->{min_total_levy};
my $LEVY_TRADEOFF_MAX = $LEVY_RANGE / $N_LAWS;

sub slider_function {
	my ($i, $tax_per_levy) = @_;
	
	my $levy_delta = 2 * $i * $LEVY_RANGE / $N_LAWS / ($N_LAWS-1);
	my $levy = $LEVY_RANGE/$N_LAWS - $levy_delta;

	return ($levy, $tax_per_levy * $levy_delta);
}

sub obligations_function {
	my ($i, $tax_per_levy) = @_;

	my $levy = $opt->{min_total_levy} + $i*($LEVY_RANGE - 2*$LEVY_TRADEOFF_MAX)/($N_LAWS-1) + $LEVY_TRADEOFF_MAX;
	my $tax = $tax_per_levy * $levy;
	
	return ($levy, $tax);
}



#####

print_laws();
exit 0;


####

sub print_params {
	print "# Written by zijistark via demesne_laws.pl v$VERSION on ".localtime." (Pacific)\n";
	print "# Code generation parameters:\n";
	print "#   min_total_levy=$opt->{min_total_levy}\n";
	print "#   max_total_levy=$opt->{max_total_levy}\n";
	for my $t ( qw( castle temple city iqta ) ) {
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
	print_summary();
	
	print "laws = {\n";
	
	print_cm_laws();

	for my $type ( qw( castle temple city iqta ) ) {

		my $tax_per_levy = $opt->{ "${type}_tax_per_levy" };
		
		# Focus
		print "\n\n\t# \U$type FOCUS\n";
		
		for my $i (0..4) {
			print_law(1, $type, $i, slider_function($i, $tax_per_levy));
		}

		# Obligations
		print "\n\t# \U$type OBLIGATIONS\n";
		
		# Normalize/offset the actual "None" level of tax obligations to always be 0
		my (undef, $min_tax_offset) = obligations_function(0, $tax_per_levy);
		
		for my $i (0..4) {
			my ($levy, $tax) = obligations_function($i, $tax_per_levy);
			print_law(0, $type, $i, $levy, $tax - $min_tax_offset);
		}
	}
	
	print "}\n";
}

####

sub print_summary {

	print "# Law modifier summary (max_levy/tax):\n#\n";

	for my $type ( qw( castle temple city iqta ) ) {

		my $tax_per_levy = $opt->{ "${type}_tax_per_levy" };
		
		print "#\n# \U$type\n";

		printf("# %12s ", "Focus:");
		
		for my $i (0..4) {
			printf("%13s  ", sprintf("%5.3f/%5.3f", slider_function($i, $tax_per_levy)));
		}
		
		printf("\n# %12s ", "Obligations:");
		
		# Normalize/offset the actual "None" level of tax obligations to always be 0
		my (undef, $min_tax_offset) = obligations_function(0, $tax_per_levy);
		
		for my $i (0..4) {
			my ($levy, $tax) = obligations_function($i, $tax_per_levy);
			printf("%13s  ", sprintf("%5.3f/%5.3f", $levy, $tax - $min_tax_offset));
		}
		
		print "\n";
	}
	
	print "\n";
}

####

sub print_law {
	my $focus   = shift;
	my $type    = shift;
	my $level   = shift;
	my $levy    = shift;
	my $tax     = shift;
	
	my ($vtype, $class, $law_group, $law, $default, $muslim) = get_law_info($type, $level, $focus);
	
	$levy = sprintf("%-5.3f", $levy);
	$tax  = sprintf("%-5.3f", $tax);
	
	my $opinion_effect = '';
	
	unless ($focus) {
		$opinion_effect .= "\t\t${class}_opinion = ".get_opinion($level);
	}
	
	$default = ($default) ? "\t\tdefault = yes" : '';
	$default .= "\n" if $opinion_effect;

	my $muslim_holder = '';

	if ($type ne 'city') {
		$muslim_holder = "holder_scope = { religion_group = muslim }";
		$muslim_holder = "not = { $muslim_holder }" unless $muslim;
		$muslim_holder = "\n\t\t\t$muslim_holder";
	}
	
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
	
	if ($level > 0 && !$focus) {
		$law_reqs .= <<EOS;
			not = {
				has_law = hre_law_0
				has_law = themes_0
			}
EOS
	}
	
	chop $law_reqs;
	
	my $revoke_laws = '';
	
	for my $i (0..4) {
		$revoke_laws .= ("\t" x 4)."revoke_law = ".$law_group.'_'.$i."\n";
	}
	
	chop $revoke_laws;
	
	my $ai_will_do = (!$focus && $level < 3) ? 1 : 0;
	
	print <<EOS;
	$law = {
		group = $law_group
$default$opinion_effect

		potential = {
			not = { tier = baron }$muslim_holder
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


####

sub print_cm_laws {
	print <<EOS;

	# CENTRALIZATION LAWS
	##############################
	
	centralization_0 = {
		group = centralization
		default = yes
		
		allow = {
			OR = {
				has_law = centralization_1
				AND = {
					NOT = {	has_law = centralization_0 }
					NOT = {	has_law = centralization_1 }
					NOT = {	has_law = centralization_2 }
					NOT = {	has_law = centralization_3 }
					NOT = {	has_law = centralization_4 }
				}
			}
		}
		potential = {
			higher_tier_than = count
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0.8
			}
			modifier = {
				factor = 0
				NOT = {
					OR = {
						AND = {
							has_law = centralization_1
							over_vassal_limit = -1
							over_max_demesne_size = -1
						}
						AND = {
							has_law = centralization_2
							over_vassal_limit = -6
							over_max_demesne_size = -2
						}
						AND = {
							has_law = centralization_3
							over_vassal_limit = -11
							over_max_demesne_size = -3
						}
						AND = {
							has_law = centralization_4
							over_vassal_limit = -16
							over_max_demesne_size = -4
						}					
					}
				}
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = centralization_0
				revoke_law = centralization_1
				revoke_law = centralization_2
				revoke_law = centralization_3
				revoke_law = centralization_4
			}
		}
		
		vassal_limit = 10
	}
	
	centralization_1 = {
		group = centralization
		
		allow = {
			OR = { 
				has_law = centralization_0
				has_law = centralization_2
			}
			OR = {
				OR = {
					has_law = tribal_organization_1
					has_law = tribal_organization_2
					has_law = tribal_organization_3
					has_law = tribal_organization_4
				}
				holder_scope = {
					is_tribal = no
				}
			}
		}
		potential = {
			higher_tier_than = count
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0.9
			}
			modifier = {
				factor = 0
				NOT = {
					OR = {
						AND = {
							has_law = centralization_0
							over_vassal_limit = -1
							over_max_demesne_size = 1
						}
						AND = {
							has_law = centralization_2
							over_vassal_limit = 1
							over_max_demesne_size = -1
						}
						AND = {
							has_law = centralization_3
							over_vassal_limit = 6
							over_max_demesne_size = -2
						}
						AND = {
							has_law = centralization_4
							over_vassal_limit = 11
							over_max_demesne_size = -3
						}					
					}
				}
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = centralization_0
				revoke_law = centralization_1
				revoke_law = centralization_2
				revoke_law = centralization_3
				revoke_law = centralization_4
			}
		}
		
		vassal_limit = 5
		demesne_size = 1
	}
	
	centralization_2 = {
		group = centralization
		
		allow = {
			OR = { 
				has_law = centralization_1
				has_law = centralization_3
			}
			OR = {
				OR = {
					has_law = tribal_organization_2
					has_law = tribal_organization_3
					has_law = tribal_organization_4
				}
				holder_scope = {
					is_tribal = no
				}
			}
		}
		potential = {
			higher_tier_than = count
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0
				NOT = {
					OR = {
						AND = {
							has_law = centralization_0
							over_vassal_limit = -6
							over_max_demesne_size = 2
						}
						AND = {
							has_law = centralization_1
							over_vassal_limit = -1
							over_max_demesne_size = 1
						}
						AND = {
							has_law = centralization_3
							over_vassal_limit = 1
							over_max_demesne_size = -1
						}
						AND = {
							has_law = centralization_4
							over_vassal_limit = 6
							over_max_demesne_size = -2
						}					
					}
				}
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = centralization_0
				revoke_law = centralization_1
				revoke_law = centralization_2
				revoke_law = centralization_3
				revoke_law = centralization_4
			}
		}
		
		vassal_limit = 0
		demesne_size = 2
	}
	
	centralization_3 = {
		group = centralization
		
		allow = {
			OR = { 
				has_law = centralization_2
				has_law = centralization_4
			}
			OR = {
				OR = {
					has_law = tribal_organization_3
					has_law = tribal_organization_4
				}
				holder_scope = {
					is_tribal = no
				}
			}
		}
		potential = {
			higher_tier_than = count
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0.9
			}
			modifier = {
				factor = 0
				NOT = {
					OR = {
						AND = {
							has_law = centralization_0
							over_vassal_limit = -11
							over_max_demesne_size = 3
						}
						AND = {
							has_law = centralization_1
							over_vassal_limit = -6
							over_max_demesne_size = 2
						}
						AND = {
							has_law = centralization_2
							over_vassal_limit = -1
							over_max_demesne_size = 1
						}
						AND = {
							has_law = centralization_4
							over_vassal_limit = 1
							over_max_demesne_size = -1
						}					
					}
				}
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = centralization_0
				revoke_law = centralization_1
				revoke_law = centralization_2
				revoke_law = centralization_3
				revoke_law = centralization_4
			}
		}
		
		vassal_limit = -5
		demesne_size = 3
	}
	
	centralization_4 = {
		group = centralization
		
		allow = {
			has_law = centralization_3
			OR = {
				OR = {
					has_law = tribal_organization_4
				}
				holder_scope = {
					is_tribal = no
				}
			}
		}
		potential = {
			higher_tier_than = count
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0.8
			}
			modifier = {
				factor = 0
				NOT = {
					OR = {
						AND = {
							has_law = centralization_0
							over_vassal_limit = -16
							over_max_demesne_size = 4
						}
						AND = {
							has_law = centralization_1
							over_vassal_limit = -11
							over_max_demesne_size = 3
						}
						AND = {
							has_law = centralization_2
							over_vassal_limit = -6
							over_max_demesne_size = 2
						}
						AND = {
							has_law = centralization_3
							over_vassal_limit = -1
							over_max_demesne_size = 1
						}					
					}
				}
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = centralization_0
				revoke_law = centralization_1
				revoke_law = centralization_2
				revoke_law = centralization_3
				revoke_law = centralization_4
			}
		}
		
		vassal_limit = -10
		demesne_size = 4
	}
	
	
	# TRIBAL ORGANIZATION
	##############################
	
	tribal_organization_0 = {
		group = tribal_organization
		default = yes
		
		tribal_opinion = 5
		
		allow = {
			OR = {
				has_law = tribal_organization_1
				AND = {
					NOT = { has_law = tribal_organization_0 }
					NOT = { has_law = tribal_organization_1 }
					NOT = { has_law = tribal_organization_2 }
					NOT = { has_law = tribal_organization_3 }
					NOT = { has_law = tribal_organization_4 }
				}
			}
		}
		potential = {
			holder_scope = {
				is_tribal = yes
				independent = yes
			}
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0
				has_law = tribal_organization_1
				holder_scope = {
					NOT = {
						any_vassal = {
							is_tribal = yes
							dislike_tribal_organization = yes
							NOT = {
								opinion = {
									who = liege
									value = 0
								}
							}
						}
					}
				}
			}
			modifier = {
				factor = 0.5
				has_law = tribal_organization_1
				dislike_tribal_organization = no
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = tribal_organization_0
				revoke_law = tribal_organization_1
				revoke_law = tribal_organization_2
				revoke_law = tribal_organization_3
				revoke_law = tribal_organization_4
				if = {
					limit = {
						OR = {
							has_law = centralization_1
							has_law = centralization_2
							has_law = centralization_3
							has_law = centralization_4
						}
					}
					add_law = centralization_0
				}
			}
			set_allow_title_revokation = no
			set_allow_free_infidel_revokation = no
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_1
					}
				}
				custom_tooltip = {
					text = disables_centralization_1
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_2
					}
				}
				custom_tooltip = {
					text = disables_centralization_2
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_3
					}
				}
				custom_tooltip = {
					text = disables_centralization_3
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_4
					}
				}
				custom_tooltip = {
					text = disables_centralization_4
				}
			}
			set_tribal_vassal_levy_control = no
			set_tribal_vassal_tax_income = no
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_4
					}
				}
				custom_tooltip = {
					text = disallows_change_government
				}
			}
		}
	}
	
	tribal_organization_1 = {
		group = tribal_organization
		
		tribal_opinion = -5
		
		allow = {
			OR = {
				has_law = tribal_organization_0
				has_law = tribal_organization_2
			}
		}
		potential = {
			holder_scope = {
				is_tribal = yes
				independent = yes
			}
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0.5
				has_law = tribal_organization_0
				holder_scope = {
					any_vassal = {
						is_tribal = yes
						dislike_tribal_organization = yes
						NOT = {
							opinion = {
								who = liege
								value = 10
							}
						}
					}
				}
			}
			modifier = {
				factor = 0
				has_law = tribal_organization_2
				holder_scope = {
					NOT = {
						any_vassal = {
							is_tribal = yes
							dislike_tribal_organization = yes
							NOT = {
								opinion = {
									who = liege
									value = 0
								}
							}
						}
					}
				}
			}
			modifier = {
				factor = 2
				has_law = tribal_organization_0
				dislike_tribal_organization = no
			}
			modifier = {
				factor = 0.5
				has_law = tribal_organization_2
				dislike_tribal_organization = no
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		pass_effect = {
			hidden_tooltip = {
				if = { 
					limit = {
						has_law = tribal_organization_0
					}
					holder_scope = {
						any_vassal = {
							limit = {
								is_tribal = yes
								dislike_tribal_organization = yes
							}
							opinion = {
								who = ROOT
								modifier = opinion_increased_tribal_organization
								months = 60
							}
						}
					}
				}
			}
		}
		effect = {
			hidden_tooltip = {
				revoke_law = tribal_organization_0
				revoke_law = tribal_organization_1
				revoke_law = tribal_organization_2
				revoke_law = tribal_organization_3
				revoke_law = tribal_organization_4
				if = {
					limit = {
						OR = {
							has_law = centralization_2
							has_law = centralization_3
							has_law = centralization_4
						}
					}
					add_law = centralization_1
				}
			}
			set_allow_title_revokation = yes
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_0
					}
				}
				custom_tooltip = {
					text = enables_centralization_1
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_2
					}
				}
				custom_tooltip = {
					text = disables_centralization_2
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_3
					}
				}
				custom_tooltip = {
					text = disables_centralization_3
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_4
					}
				}
				custom_tooltip = {
					text = disables_centralization_4
				}
			}
			set_allow_free_infidel_revokation = no
			set_tribal_vassal_levy_control = no
			set_tribal_vassal_tax_income = no
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_4
					}
				}
				custom_tooltip = {
					text = disallows_change_government
				}
			}
		}
	}
	
	tribal_organization_2 = {
		group = tribal_organization
		
		tribal_opinion = -10
		
		allow = {
			OR = {
				has_law = tribal_organization_1
				has_law = tribal_organization_3
			}
		}
		potential = {
			holder_scope = {
				is_tribal = yes
				independent = yes
			}
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0.5
				has_law = tribal_organization_1
				holder_scope = {
					any_vassal = {
						is_tribal = yes
						dislike_tribal_organization = yes
						NOT = {
							opinion = {
								who = liege
								value = 5
							}
						}
					}
				}
			}
			modifier = {
				factor = 0
				has_law = tribal_organization_3
				holder_scope = {
					NOT = {
						any_vassal = {
							is_tribal = yes
							dislike_tribal_organization = yes
							NOT = {
								opinion = {
									who = liege
									value = 0
								}
							}
						}
					}
				}
			}
			modifier = {
				factor = 2
				has_law = tribal_organization_1
				dislike_tribal_organization = no
			}
			modifier = {
				factor = 0.5
				has_law = tribal_organization_3
				dislike_tribal_organization = no
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		pass_effect = {
			hidden_tooltip = {
				if = { 
					limit = {
						has_law = tribal_organization_1
					}
					holder_scope = {
						any_vassal = {
							limit = {
								is_tribal = yes
								dislike_tribal_organization = yes
							}
							opinion = {
								who = ROOT
								modifier = opinion_increased_tribal_organization
								months = 60
							}
						}
					}
				}
			}
		}
		effect = {
			hidden_tooltip = {
				revoke_law = tribal_organization_0
				revoke_law = tribal_organization_1
				revoke_law = tribal_organization_2
				revoke_law = tribal_organization_3
				revoke_law = tribal_organization_4
				if = {
					limit = {
						OR = {
							has_law = centralization_3
							has_law = centralization_4
						}
					}
					add_law = centralization_2
				}
			}
			set_allow_title_revokation = yes
			set_allow_free_infidel_revokation = yes
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_0
						has_law = tribal_organization_1
					}
				}
				custom_tooltip = {
					text = enables_centralization_2
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_3
					}
				}
				custom_tooltip = {
					text = disables_centralization_3
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_4
					}
				}
				custom_tooltip = {
					text = disables_centralization_4
				}
			}
			set_tribal_vassal_levy_control = no
			set_tribal_vassal_tax_income = no
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_4
					}
				}
				custom_tooltip = {
					text = disallows_change_government
				}
			}
		}
	}
	
	tribal_organization_3 = {
		group = tribal_organization
		
		tribal_opinion = -20
		
		allow = {
			OR = {
				has_law = tribal_organization_2
				has_law = tribal_organization_4
			}
		}
		potential = {
			holder_scope = {
				is_tribal = yes
				independent = yes
			}
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0.5
				has_law = tribal_organization_2
				holder_scope = {
					any_vassal = {
						is_tribal = yes
						dislike_tribal_organization = yes
						NOT = {
							opinion = {
								who = liege
								value = 10
							}
						}
					}
				}
			}
			modifier = {
				factor = 0
				has_law = tribal_organization_4
				holder_scope = {
					NOT = {
						any_vassal = {
							is_tribal = yes
							dislike_tribal_organization = yes
							NOT = {
								opinion = {
									who = liege
									value = 0
								}
							}
						}
					}
				}
			}
			modifier = {
				factor = 2
				has_law = tribal_organization_2
				dislike_tribal_organization = no
			}
			modifier = {
				factor = 0.5
				has_law = tribal_organization_4
				dislike_tribal_organization = no
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		pass_effect = {
			hidden_tooltip = {
				if = { 
					limit = {
						has_law = tribal_organization_2
					}
					holder_scope = {
						any_vassal = {
							limit = {
								is_tribal = yes
								dislike_tribal_organization = yes
							}
							opinion = {
								who = ROOT
								modifier = opinion_increased_tribal_organization
								months = 60
							}
						}
					}
					add_law = centralization_0
				}
			}
		}
		effect = {
			hidden_tooltip = {
				revoke_law = tribal_organization_0
				revoke_law = tribal_organization_1
				revoke_law = tribal_organization_2
				revoke_law = tribal_organization_3
				revoke_law = tribal_organization_4
				if = {
					limit = {
						OR = {
							has_law = centralization_4
						}
					}
					add_law = centralization_3
				}
			}
			set_allow_title_revokation = yes
			set_allow_free_infidel_revokation = yes
			set_tribal_vassal_levy_control = yes
			set_tribal_vassal_tax_income = yes
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_0
						has_law = tribal_organization_1
						has_law = tribal_organization_2
					}
				}
				custom_tooltip = {
					text = enables_centralization_3
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_4
					}
				}
				custom_tooltip = {
					text = disables_centralization_4
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_4
					}
				}
				custom_tooltip = {
					text = disallows_change_government
				}
			}
		}
	}
	
	tribal_organization_4 = {
		group = tribal_organization
		
		tribal_opinion = -30
		
		allow = {
			has_law = tribal_organization_3
		}
		potential = {
			holder_scope = {
				is_tribal = yes
				independent = yes
			}
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0.5
				has_law = tribal_organization_3
				holder_scope = {
					any_vassal = {
						is_tribal = yes
						dislike_tribal_organization = yes
						NOT = {
							opinion = {
								who = liege
								value = 10
							}
						}
					}
				}
			}
			modifier = {
				factor = 2
				has_law = tribal_organization_3
				dislike_tribal_organization = no
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		pass_effect = {
			hidden_tooltip = {
				if = { 
					limit = {
						has_law = tribal_organization_3
					}
					holder_scope = {
						any_vassal = {
							limit = {
								is_tribal = yes
								dislike_tribal_organization = yes
							}
							opinion = {
								who = ROOT
								modifier = opinion_increased_tribal_organization
								months = 60
							}
						}
					}
				}
			}
		}
		effect = {
			hidden_tooltip = {
				revoke_law = tribal_organization_0
				revoke_law = tribal_organization_1
				revoke_law = tribal_organization_2
				revoke_law = tribal_organization_3
				revoke_law = tribal_organization_4
			}
			set_allow_title_revokation = yes
			set_allow_free_infidel_revokation = yes
			set_tribal_vassal_levy_control = yes
			set_tribal_vassal_tax_income = yes
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_0
						has_law = tribal_organization_1
						has_law = tribal_organization_2
						has_law = tribal_organization_3
					}
				}
				custom_tooltip = {
					text = enables_centralization_4
				}
			}
			if {
				limit = { 
					OR = {
						has_law = tribal_organization_0
						has_law = tribal_organization_1
						has_law = tribal_organization_2
						has_law = tribal_organization_3
					}
				}
				custom_tooltip = {
					text = allows_change_government
				}
			}
		}
	}
	
	# VICE ROYALTY LAWS
	##############################
	
	vice_royalty_0 = {
		group = vice_royalty
		default = yes
		
		potential = {
			higher_tier_than = king
			holder_scope = {
				independent = yes
				is_feudal = yes
			}
			has_dlc = "Charlemagne"
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 1
			modifier = {
				factor = 0
				NOT = {
					OR = {
						AND = {
							has_law = vice_royalty_1
							over_vassal_limit = 1
						}
						AND = {
							has_law = vice_royalty_2
							over_vassal_limit = 6
						}		
					}
				}
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = vice_royalty_0
				revoke_law = vice_royalty_1
				revoke_law = vice_royalty_2
			}
			set_allow_vice_royalties = no
		}
	}

	vice_royalty_1 = {
		group = vice_royalty
		
		potential = {
			higher_tier_than = king
			holder_scope = {
				independent = yes
				is_feudal = yes
			}
			has_dlc = "Charlemagne"
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 2
			modifier = {
				factor = 0
				AND = {
					has_law = vice_royalty_2
					over_vassal_limit = 1
				}
			}
			modifier = {
				factor = 0
				AND = {
					has_law = vice_royalty_0
					over_vassal_limit = -5
				}
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = vice_royalty_0
				revoke_law = vice_royalty_1
				revoke_law = vice_royalty_2
			}
			set_allow_vice_royalties = king
		}
		
		vassal_limit = -5
	}
	
	vice_royalty_2 = {
		group = vice_royalty
		
		potential = {
			higher_tier_than = king
			holder_scope = {
				independent = yes
				is_feudal = yes
			}
			has_dlc = "Charlemagne"
		}
		revoke_allowed = {
			always = no
		}			
		ai_will_do = {
			factor = 3
			modifier = {
				factor = 0
				AND = {
					has_law = vice_royalty_0
					over_vassal_limit = -10
				}
			}
			modifier = {
				factor = 0
				AND = {
					has_law = vice_royalty_1
					over_vassal_limit = -5
				}
			}
		}
		ai_will_revoke = {
			factor = 0
		}
		effect = {
			hidden_tooltip = {
				revoke_law = vice_royalty_0
				revoke_law = vice_royalty_1
				revoke_law = vice_royalty_2
			}
			set_allow_vice_royalties = duke
		}
		
		vassal_limit = -10
	}
	
	# BYZANTINE ADMINISTRATION
	##############################
	
	feudal_administration = {
		group = administration
		
		potential = {
			higher_tier_than = king
			holder_scope = {
				independent = yes
				is_tribal = no
			}
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
				revoke_law = feudal_administration
				revoke_law = imperial_administration
			}
		}
	}
	
	imperial_administration = {
		group = administration
		
		allow = {
			has_law = crown_authority_4
		}
		
		potential = {
			higher_tier_than = king
			holder_scope = {
				independent = yes
				is_tribal = no
			}
		}
		revoke_allowed = {
			always = no
		}
		ai_will_do = {
			factor = 10
		}
		ai_will_revoke = {
			factor = 0
		}
		
		effect = {
			hidden_tooltip = {
				revoke_law = feudal_administration
				revoke_law = imperial_administration
			}
			if  = {
				limit = {
					has_dlc = "Charlemagne"
				}
				add_law = vice_royalty_2
			}
		}
		
		vassal_limit = 25
		feudal_opinion = -10
	}
	

# BYZANTINE EMPIRE
	themes_0 = {
		show_as_title = yes
		group = themes
		default = yes
		
		potential = {
			title = e_byzantium
			NOT = { has_global_flag = shattered_balance }
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
				revoke_law = themes_0
				revoke_law = themes_1
				revoke_law = themes_2
			}
			add_law = vice_royalty_2
		}
		
		castle_vassal_max_levy = -0.1
		castle_vassal_min_levy = -0.1
		city_vassal_max_levy = -0.1
		city_vassal_min_levy = -0.1
		temple_vassal_max_levy = -0.1
		temple_vassal_min_levy = -0.1
		
		castle_vassal_tax_modifier = -0.05
		temple_vassal_tax_modifier = -0.1
		city_vassal_tax_modifier = -0.15
	}
	
	themes_1 = {
		show_as_title = yes
		group = themes
		
		feudal_opinion = -10
		city_opinion = -10
		temple_opinion = -10
		
		potential = {
			title = e_byzantium
			NOT = { has_global_flag = shattered_balance }
		}
		allow = {
			holder_scope = {
				prestige = 1000
				custom_tooltip = {
					text = pb_vassal_opinion_neg_25
					hidden_tooltip = {
						NOT = {
							any_vassal = {
								higher_tier_than = count
								NOT = { opinion = { who = liege value = -25 } }
								primary_title = { is_primary_type_title = no } # Mercs, the Pope, Holy Orders, etc
								prisoner = no
							}
						}
					}
				}
			}
			NOT = { has_law = themes_2 }
		}
		revoke_allowed = {
			always = no
		}
		ai_will_do = {
			factor = 1
		}
		ai_will_revoke = {
			factor = 0
		}
		pass_effect = {
			hidden_tooltip = {
				set_global_flag = theme_system_reformed
				holder_scope = {
					any_vassal = {
						opinion = {
							who = ROOT
							modifier = opinion_increased_authority
							months = 300
						}
					}
				}
			}
		}
		effect = {
			hidden_tooltip = {
				revoke_law = themes_0
				revoke_law = themes_1
				revoke_law = themes_2
			}
			add_law = vice_royalty_2
		}
		
		city_vassal_min_levy = 0.1
		castle_vassal_min_levy = 0.1
		temple_vassal_min_levy = 0.1

		castle_vassal_max_levy = -0.05
		city_vassal_max_levy = -0.05
		temple_vassal_max_levy = -0.05
		
		castle_vassal_tax_modifier = -0.025
		temple_vassal_tax_modifier = -0.05
		city_vassal_tax_modifier = -0.075
	}
	
	themes_2 = {
		show_as_title = yes
		group = themes
		
		feudal_opinion = -15
		city_opinion = -15
		temple_opinion = -15
		
		potential = {
			title = e_byzantium
			NOT = { has_global_flag = shattered_balance }
		}
		allow = {
			has_law = themes_1
			holder_scope = {
				prestige = 2000
				custom_tooltip = {
					text = pb_vassal_opinion_neg_10
					hidden_tooltip = {
						NOT = {
							any_vassal = {
								higher_tier_than = count
								NOT = { opinion = { who = liege value = -10 } }
								primary_title = { is_primary_type_title = no } # Mercs, the Pope, Holy Orders, etc
								prisoner = no
							}
						}
					}
				}
			}
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
		pass_effect = {
			hidden_tooltip = {
				set_global_flag = theme_system_reformed_2
				holder_scope = {
					any_vassal = {
						opinion = {
							who = ROOT
							modifier = opinion_increased_authority
							months = 300
						}
					}
				}
			}
		}
		effect = {
			hidden_tooltip = {
				revoke_law = themes_0
				revoke_law = themes_1
				revoke_law = themes_2
			}
			add_law = vice_royalty_2
		}
		city_vassal_min_levy = 0.2
		castle_vassal_min_levy = 0.2
		temple_vassal_min_levy = 0.2
	}
	
	# HOLY ROMAN EMPIRE
	hre_law_0 = {
		show_as_title = yes
		group = hre_law
		default = yes
		
		potential = {
			title = e_hre
			NOT = { has_global_flag = shattered_balance }
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
				revoke_law = hre_law_0
				revoke_law = hre_law_1
			}
		}

		castle_vassal_max_levy = -0.15
		castle_vassal_min_levy = -0.15
		city_vassal_max_levy = -0.15
		city_vassal_min_levy = -0.15
		temple_vassal_max_levy = -0.15
		temple_vassal_min_levy = -0.15
		
		castle_vassal_tax_modifier = -0.05
		temple_vassal_tax_modifier = -0.1
		city_vassal_tax_modifier = -0.15
	}
	
	hre_law_1 = {
		show_as_title = yes
		group = hre_law
		
		feudal_opinion = -15
		city_opinion = -10
		temple_opinion = -10
		
		potential = {
			title = e_hre
			NOT = { has_global_flag = shattered_balance }
		}
		allow = {
			holder_scope = {
				prestige = 1000
				custom_tooltip = {
					text = pb_vassal_opinion_neg_25
					hidden_tooltip = {
						NOT = {
							any_vassal = {
								higher_tier_than = count
								NOT = { opinion = { who = liege value = -25 } }
								primary_title = { is_primary_type_title = no } # Mercs, the Pope, Holy Orders, etc
								prisoner = no
							}
						}
					}
				}
			}
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
		pass_effect = {
			hidden_tooltip = {
				set_global_flag = hre_centralized
				holder_scope = {
					any_vassal = {
						opinion = {
							who = ROOT
							modifier = opinion_increased_authority
							months = 300
						}
					}
				}
			}
		}
		effect = {
			hidden_tooltip = {
				revoke_law = hre_law_0
				revoke_law = hre_law_1
			}
		}
	}

EOS
}
