unit class Action;

my regex CoOrdFormat { <[a..h]> <[1..8]> };
subset CoOrd is export where * ~~ / ^ <CoOrdFormat> $ /;
enum ActionType is export < Capture Move MoveCapture >;

has CoOrd $.from is required;
has CoOrd ($.to, $.attacking);
has ActionType $.type is required;
has Bool $.was-successful;

method Str(Action:D:) {
	given $!type {
		when Move {
			return "$!from>$!to";
		}

		my $result =
			   !defined $!was-successful ?? '?'
			!! $!was-successful          ?? 's'
			!!                              'f'
			;

		when Capture {
			return "{ $!from }x{ $!attacking }=$result";
		}

		when MoveCapture {
			return "{ $!from }>{ $!to }x{ $!attacking }=$result";
		}
	}
}

# TODO: error messages
method from-str(Action:U: Str $s) returns Action {
	unless $s ~~ /
			^
			$<from>=<CoOrdFormat>
			['>' $<to>=<CoOrdFormat>]?
			['x' $<attacking>=<CoOrdFormat>
				'=' $<was-successful>=<[? s f]> ]?
			$
			/
	{
		say 'Error parsing action string: String does not match regex.';
		return Nil;
	}

	my ActionType $type;
	if defined $<to> {
		if defined $<attacking> {
			$type = MoveCapture; # Knights only
		}
		else {
			$type = Move;
		}
	}
	elsif defined $<attacking> {
		$type = Capture;
	}
	else {
		say 'Error parsing action string: Neither <to> nor <attacking> defined.';
		return Nil;
	}

	my Bool $was-successful;
	if $type == (Capture | MoveCapture) {
		$was-successful = $<was-successful>.Str eq 's';
	}

	return self.bless:
		to        => $<to>,
		from      => $<from>,
		attacking => $<attacking>,
		:$type,
		:$was-successful
		;
}

# TODO: maybe identity needs to include the turn number depending on our future needs. For now, not the case
multi submethod WHICH(Action:D:) {
	"Action|{self.Str}"
}

multi submethod WHICH(Action:U:) {
	'Action|UNDEF'
}
