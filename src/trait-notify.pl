#!/usr/bin/perl

my $VERSION = '1.0';

use strict;
use warnings;
use Carp;
use Getopt::Long qw(:config gnu_getopt);
use File::Spec;

my $VAN_PATH = File::Spec->catdir(qw( /cygdrive c ), 'Program Files (x86)', qw( Steam steamapps common ), 'Crusader Kings II');
my $ROOT_PATH = File::Spec->catdir(qw( /cygdrive c cygwin64 home ), $ENV{USER}, 'g');
my $MOD_PATH = File::Spec->catdir($ROOT_PATH, qw( EMF EMF ));

my $MOD_TRAITS_PATH = File::Spec->catdir($MOD_PATH, qw( common traits ));
my $MOD_LOC_PATH = File::Spec->catdir($MOD_PATH, 'localisation');
my $VAN_LOC_PATH = File::Spec->catdir($VAN_PATH, 'localisation');

my $VAN_TRAIT_FILE_RE = qr/^0\d_traits.txt$/;
my $TRAIT_FILE_IGNORE_RE = qr/age_customizer/;

my $EVT_ID_OFFSET_GAIN = 0;
my $EVT_ID_OFFSET_LOSS = 1000;
my $EVT_ID_OFFSET_GAIN_BOUNCED = 2000;
my $EVT_ID_OFFSET_LOSS_BOUNCED = 3000;

my $STATE_WAIT_OPEN = 0;
my $STATE_WAIT_CLOSE = 1;

for my $f ( ($VAN_PATH, $ROOT_PATH, $MOD_PATH, $MOD_TRAITS_PATH, $MOD_LOC_PATH, $VAN_LOC_PATH) ) {
	croak "invalid path: $f" unless -e $f;
}

my %targets = (
	localisation => \&print_localisation,
	events => \&print_events,
	effects => \&print_effects,
);

my $opt_target;

GetOptions(
	't|target=s' => \$opt_target,
) or croak;


unless ($opt_target) {
	print STDERR "You must specify a codegen target with --target localisation|effects|events.\n";
	exit 1;
}

$opt_target = "\L$opt_target"; # Case-insensitive

unless (exists $targets{$opt_target}) {
	print STDERR "Undefined codegen target '$opt_target'.  Aborting.\n";
	exit 2;
}

my $traits = read_trait_dir($MOD_TRAITS_PATH) or croak "no traits defined!";
localise_traits($VAN_LOC_PATH, $MOD_LOC_PATH, $traits);

my $handler = $targets{$opt_target};
&$handler($traits);

exit 0;


sub read_trait_dir {
	my $dpath = shift;

	opendir(my $dh, $dpath) or croak "opendir: $!: $dpath";
	my @trait_files = sort grep { /^.+?\.txt$/ } readdir $dh;
	closedir $dh;

	my %traits = ();
	my $n = 0;

	for my $f (@trait_files) {
		next if $f =~ $TRAIT_FILE_IGNORE_RE;

		my $p = File::Spec->catfile($dpath, $f);

		my $is_vanilla = 0;
		$is_vanilla = 1 if $f =~ $VAN_TRAIT_FILE_RE;

		#print "trait file".( ($is_vanilla) ? " (vanilla)" : "" ).": $p\n";

		my $state = $STATE_WAIT_OPEN;

		open(my $fh, '<', $p) or croak "open: $!: $p";

		while (<$fh>) {
			if ($state == $STATE_WAIT_OPEN) {
				if (/^(\w+)\s*=\s*[{]\s*$/) {
					croak "multiply-defined trait tag: $1!" if exists $traits{$1};

					++$n;
					my $t = { id => $n, tag => $1, vanilla => $is_vanilla };
					$traits{$1} = $t;
					$state = $STATE_WAIT_CLOSE;
				}
				next;
			}
			$state = $STATE_WAIT_OPEN if /^[}]\s*$/;
		}

		close $fh;
	}

	#print "> $n total traits.\n";

	return undef unless $n;
	return \%traits;
}


sub localise_traits {
	my $vdir = shift;
	my $mdir = shift;
	my $traits = shift;

	my $trait_key_pattern = '^(' . join('|', keys %$traits) . ');([^;]+);';
	my $trait_key_re = qr/$trait_key_pattern/;

	read_localisation_dir($vdir, $trait_key_re, $traits);
	read_localisation_dir($mdir, $trait_key_re, $traits);

	my @tags_missing_loc = map { $_->{tag} } grep { (!exists $_->{name}) || !$_->{name} } values %$traits;

	if (@tags_missing_loc) {
		print STDERR "fatal: the following traits are missing localisation:\n";
		for my $tag (@tags_missing_loc) {
			print STDERR "  $tag\n";
		}
		exit 3;
	}
}

sub read_localisation_dir {
	my $d = shift;
	my $text_re = shift;
	my $traits = shift;

	opendir(my $dh, $d) or croak "opendir: $!: $d";
	my @loc_files = sort grep { /^.+?\.csv$/ } readdir $dh;
	closedir $dh;

	for my $f (@loc_files) {
		my $p = File::Spec->catfile($d, $f);

		open(my $fh, '<', $p) or croak "open: $!: $p";

		while (<$fh>) {
			next if /^\s*#/;
			if ($_ =~ $text_re) {
				$traits->{$1}{name} = $2;
				#print "$1 => $2   [$f]\n";
			}
		}

		close $fh;
	}
}


sub print_params {
	print "# Written by zijistark via trait-notify.pl v$VERSION on ".localtime." (Pacific)\n";
	print "\n";
}

sub print_effects {
	my $traits = shift;

	print "# -*- ck2.scripted_effects -*-\n";
	print_params();

	print <<EOS;

#########################################
#  TRAIT NOTIFICATION SCRIPTED EFFECTS  #
#########################################

EOS

	for my $tag (sort { $traits->{$a}{id} <=> $traits->{$b}{id} } keys %$traits) {
		my $t = $traits->{$tag};

		my $gain_effect = "emf_notify_add_${tag}_effect";
		my $loss_effect = "emf_notify_remove_${tag}_effect";

		my $gain_id = $t->{id} + $EVT_ID_OFFSET_GAIN;
		my $loss_id = $t->{id} + $EVT_ID_OFFSET_LOSS;

		print <<EOS;

#### [$t->{id}] $t->{name}: $tag ####
$gain_effect = {
	hidden_tooltip = {
		if = {
			limit = { trait = $tag }
			log = "WARNING: $gain_effect: [This.GetBestName] ([This.GetID]) already has the trait to be added ($tag)!"
		}
	}
	if = {
		limit = { NOT = { trait = $tag } }
		add_trait = $tag
		hidden_tooltip = { character_event = { id = emf_trait.$gain_id } }
	}
}
$loss_effect = {
	hidden_tooltip = {
		if = {
			limit = { NOT = { trait = $tag } }
			log = "WARNING: $loss_effect: [This.GetBestName] ([This.GetID]) doesn't have the trait to be removed ($tag)!"
		}
	}
	if = {
		limit = { trait = $tag }
		remove_trait = $tag
		hidden_tooltip = { character_event = { id = emf_trait.$loss_id } }
	}
}
EOS
	}
}

sub print_events {
	my $traits = shift;

	print "# -*- ck2.events -*-\n";
	print_params();

	print <<EOS;
#########################################
#       TRAIT NOTIFICATION EVENTS       #
#########################################

namespace = emf_notify

# NOTE: One should never call these event IDs directly but instead should use
# the named scripted effects in emf_notify_effects.txt to deliver notifications
# for the add/remove of traits. That way, when traits are added or changed,
# their trait IDs and thus event IDs here may change, but their named effects
# will always resolve to the correct event. Additionally, the scripted effects
# actually add/remove the trait as well so as to be able to avoid redundant
# notifications and catch coding errors.


##################################################
#    Trait Gain Notification Forwarder Events    #
# emf_notify.1 through emf_notify.1000 reserved  #
##################################################
EOS

	my @sorted_tags = sort { $traits->{$a}{id} <=> $traits->{$b}{id} } keys %$traits;

	for my $tag (@sorted_tags) {
		my $t = $traits->{$tag};
		my $id = $t->{id} + $EVT_ID_OFFSET_GAIN;
		my $bounced_id = $t->{id} + $EVT_ID_OFFSET_GAIN_BOUNCED;
		my $evt_id = 'emf_notify.'.$id;
		my $bounced_evt_id = 'emf_notify.'.$bounced_id;

		print <<EOS;

# $evt_id -- added $tag ($t->{name})
character_event = {
	id = $evt_id

	is_triggered_only = yes
	hide_window = yes

	trigger = {
		OR = {
			FROM = { ai = no }
			event_target:emf_notify_receiver = { ai = no }
		}
	}

	immediate = {
		# If the target emf_notify_receiver is defined (and player), send notifications about ROOT's trait gain to them.
		if = {
			limit = { event_target:emf_notify_receiver = { ai = no } }
			event_target:emf_notify_receiver = { character_event = { id = $bounced_evt_id } }
		}
		# If FROM is a player, send notification about ROOT's trait gain to FROM.
		if = {
			limit = {
				# Don't duplicate to FROM -- we can only send 2 notification events if FROM and emf_notify_receiver are
				# two different player characters.
				FROM = {
					ai = no
					NOT = { character = event_target:emf_notify_receiver }
				}
			}
			FROM = { character_event = { id = $bounced_evt_id } }
		}
	}
}
EOS
	}

	print <<EOS;


####################################################
#     Trait Loss Notification Forwarder Events     #
# emf_notify.1001 through emf_notify.2000 reserved #
####################################################
EOS

	for my $tag (@sorted_tags) {
		my $t = $traits->{$tag};
		my $id = $t->{id} + $EVT_ID_OFFSET_LOSS;
		my $bounced_id = $t->{id} + $EVT_ID_OFFSET_LOSS_BOUNCED;
		my $evt_id = 'emf_notify.'.$id;
		my $bounced_evt_id = 'emf_notify.'.$bounced_id;

		print <<EOS;

# $evt_id -- removed $tag ($t->{name})
character_event = {
	id = $evt_id

	is_triggered_only = yes
	hide_window = yes

	trigger = {
		OR = {
			FROM = { ai = no }
			event_target:emf_notify_receiver = { ai = no }
		}
	}

	immediate = {
		# If the target emf_notify_receiver is defined (and player), send notifications about ROOT's trait loss to them.
		if = {
			limit = { event_target:emf_notify_receiver = { ai = no } }
			event_target:emf_notify_receiver = { character_event = { id = $bounced_evt_id } }
		}
		# If FROM is a player, send notification about ROOT's trait loss to FROM.
		if = {
			limit = {
				# Don't duplicate to FROM -- we can only send 2 notification events if FROM and emf_notify_receiver are
				# two different player characters.
				FROM = {
					ai = no
					NOT = { character = event_target:emf_notify_receiver }
				}
			}
			FROM = { character_event = { id = $bounced_evt_id } }
		}
	}
}
EOS
	}

	print <<EOS;


####################################################
#          Trait Gain Notification Events          #
# emf_notify.2001 through emf_notify.3000 reserved #
####################################################
EOS

	for my $tag (@sorted_tags) {
		my $t = $traits->{$tag};
		my $id = $t->{id} + $EVT_ID_OFFSET_GAIN_BOUNCED;
		my $evt_id = 'emf_notify.'.$id;

		print <<EOS;

# $evt_id -- added $tag ($t->{name}) to FROM [notification]
character_event = {
	id = $evt_id
	desc = $evt_id.desc
	picture = GFX_evt_emissary

	desc = {
		text = $evt_id.desc_w_relation
		trigger = {
			NOT = { character = FROM }
			OR = {
				is_close_relative = FROM
				is_married = FROM
				any_ward = { character = FROM }
				guardian = { character = FROM }
			}
		}
	}

	is_triggered_only = yes
	notification = yes

	option = { name = OK }
}
EOS
	}

	print <<EOS;


####################################################
#          Trait Loss Notification Events          #
# emf_notify.3001 through emf_notify.4000 reserved #
####################################################
EOS

	for my $tag (@sorted_tags) {
		my $t = $traits->{$tag};
		my $id = $t->{id} + $EVT_ID_OFFSET_LOSS_BOUNCED;
		my $evt_id = 'emf_notify.'.$id;

		print <<EOS;

# $evt_id -- removed $tag ($t->{name}) from FROM [notification]
character_event = {
	id = $evt_id
	desc = $evt_id.desc
	picture = GFX_evt_emissary

	desc = {
		text = $evt_id.desc_w_relation
		trigger = {
			NOT = { character = FROM }
			OR = {
				is_close_relative = FROM
				is_married = FROM
				any_ward = { character = FROM }
				guardian = { character = FROM }
			}
		}
	}

	is_triggered_only = yes
	notification = yes

	option = { name = OK }
}
EOS
	}
}

sub print_localisation {
	my $traits = shift;
	my @sorted_tags = sort { $traits->{$a}{id} <=> $traits->{$b}{id} } keys %$traits;

	print "#CODE;ENGLISH;FRENCH;GERMAN;;SPANISH;;;;;;;;;x\n";
	my $eol = ";;;;;;;;;;;;;x\n";

	for my $tag (@sorted_tags) {
		my $t = $traits->{$tag};
		my $id = $t->{id} + $EVT_ID_OFFSET_GAIN_BOUNCED;
		my $evt_id = 'emf_notify.'.$id;

		print "$evt_id.desc;[From.GetDynName] has gained the trait §Y$t->{name}§!.$eol";
		print "$evt_id.desc_w_relation;Your [GetFromRelation], [From.GetDynName], has gained the trait §Y$t->{name}§!.$eol";
	}

	for my $tag (@sorted_tags) {
		my $t = $traits->{$tag};
		my $id = $t->{id} + $EVT_ID_OFFSET_LOSS_BOUNCED;
		my $evt_id = 'emf_notify.'.$id;

		print "$evt_id.desc;[From.GetDynName] has lost the trait §Y$t->{name}§!.$eol";
		print "$evt_id.desc_w_relation;Your [GetFromRelation], [From.GetDynName], has lost the trait §Y$t->{name}§!.$eol";
	}
}
