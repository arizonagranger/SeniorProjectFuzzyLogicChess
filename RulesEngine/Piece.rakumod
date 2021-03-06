use Terminal::ANSIColor;

unit class Piece;

enum PieceType is export < King Queen Archer Pikeman Knight Infantry >;
enum Team is export < White Black >;
enum Corp is export < K L R >; # King, left, right

has PieceType $.type is required;
has Team $.team is required;
has Corp $.corp is rw = K;

multi method clone(Piece:D:) {
	Piece.new:
		type => $!type,
		team => $!team,
		corp => $!corp,
		;
}
multi method clone(Piece:U:) {
	Piece
}

method gist {
	if defined self {
		return color($!team == White ?? 'white' !! 'black') ~ self.shorthand;
	}
	else {
		return q{ };
	}
}

multi method shorthand(Piece:D:) {
	given $!type {
		return 'K' when King;
		return 'Q' when Queen;
		return 'A' when Archer;
		return 'P' when Pikeman;
		return 'N' when Knight;
		return 'I' when Infantry;
	}
}
multi method shorthand(Piece:U:) {
	q{ }
}

multi method Str(Piece:D:) {
	  ($!team == White ?? self.shorthand !! self.shorthand.lc)
	~ $!corp
}
multi method Str(Piece:U:) {
	q{}
}
