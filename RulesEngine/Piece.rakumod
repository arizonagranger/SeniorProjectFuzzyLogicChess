use Terminal::ANSIColor;

unit class Piece;

enum PieceType is export < King Queen Archer Pikeman Knight Infantry >;
enum Team is export < White Black >;

has PieceType $.type is required;
has Team $.team is required;

# For pawns
has Bool $.has-moved = False;

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
	($!team == White ?? 'W' !! 'B') ~ self.shorthand
}
multi method Str(Piece:U:) {
	q{}
}
