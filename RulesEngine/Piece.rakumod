use Terminal::ANSIColor;

unit class Piece;

enum PieceType is export < King Queen Archer Pikeman Knight Infantry >;
enum Team is export < White Black >;

has Type $.type is required;
has Team $.team is required;

# For pawns
has Bool $.has-moved = False;

method gist {
	colored self.shorthand, $!team == White ?? 'white' !! 'black';
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
