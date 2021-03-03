use Terminal::ANSIColor;

use Piece;
use Action;

unit class Board;

enum BoardType < Default >;

has BoardType $.type = Default;
has Bool $!is-clone = False;
# rank-major (i.e. row-major), later rows closer to black side to align with how coordinates work
has Piece @!board[8;8];
has Bool $.is-game-ended = False;
has Piece::Team $.whose-turn;

role Capturer {
	method to-capture(Capturer:D: \key) { self.AT-KEY(key) }
}
constant %roll-needed-for =
	King     => %{ King => 4, Queen => 4, Knight => 4, Pikeman => 4, Archer => 5, Infantry => 1 } but Capturer,
	Queen    => %{ King => 4, Queen => 4, Knight => 4, Pikeman => 4, Archer => 5, Infantry => 2 } but Capturer,
	Knight   => %{ King => 6, Queen => 6, Knight => 4, Pikeman => 4, Archer => 5, Infantry => 2 } but Capturer,
	Pikeman  => %{ King => 5, Queen => 5, Knight => 5, Pikeman => 4, Archer => 5, Infantry => 3 } but Capturer,
	Archer   => %{ King => 4, Queen => 4, Knight => 5, Pikeman => 5, Archer => 6, Infantry => 5 } but Capturer,
	Infantry => %{ King => 6, Queen => 6, Knight => 6, Pikeman => 5, Archer => 6, Infantry => 4 } but Capturer,
	;

submethod TWEAK {
	if $!type == Default && ! $!is-clone {
		for Archer, Knight, Pikeman, Queen, King, Pikeman, Knight, Archer {
			state $file = 0;
			@!board[0;$file] = Piece.new: type => $_, team => White;
			@!board[7;$file] = Piece.new: type => $_, team => Black;
			$file++;
		}

		for ^8 -> $file {
			@!board[1;$file] = Piece.new: type => Infantry, team => White;
			@!board[6;$file] = Piece.new: type => Infantry, team => Black;
		}

		$!whose-turn = White;
	}
}

method clone {
	
}

multi sub indices-to-coord(UInt $rank, UInt $file) returns CoOrd {
	my %translation-of = ^8 Z=> 'a'..'h';

	return %translation-of{$file} ~ $rank + 1;
}
multi sub indices-to-coord($list where *.elems == 2) returns CoOrd {
	indices-to-coord($list[0], $list[1])
}

sub coord-to-indices(CoOrd $pos) returns List {
	my %translation-of = 'a'..'h' Z=> ^8;

	my ($file, $rank) = $pos.comb;
	return $rank - 1, %translation-of{$file};
}

multi method piece-at(Board:D: CoOrd $pos) returns Piece {
	my ($rank, $file) = coord-to-indices $pos;
	return @!board[$rank;$file];
}
multi method piece-at(Board:D: [$rank, $file]) returns Piece {
	return @!board[$rank;$file];
}

method actions-for(Board:D: CoOrd $pos) {
	my @deltas = (-1, 0, 1 X -1, 0, 1).grep: * !eqv (0, 0);

	my Piece $piece = self.piece-at: $pos;

	return () without $piece;
	return () unless $piece.team == $!whose-turn;

	my Action @actions;

	given $piece.type {
		when King | Queen | Knight {
			# my SetHash[Action] ($final, $working) = SetHash.new xx 2;
			my SetHash ($final, $working) = SetHash.new xx 2;
			
			# Keep this around to remove it later
			my Action $trivial-action .= new: :to($pos), :from($pos), :type(Move);
			$working.set: $trivial-action;

			my $dist = $_ ~~ Knight ?? 6 !! 3; # Knights can only move 5--the 6th round is for captures only
			for 1..$dist -> $current-dist {
				my $old-working = $working.SetHash; # copy
				for $working.keys.map(*.to) -> $working-coord {
					my @adjacents = @deltas
						.map({ @$_ Z+ coord-to-indices $working-coord }) # add deltas to starting pos
						.grep({ 0 <= all($_) <= 7 })                     # keep only coords within bounds
						;
					for @adjacents -> $possible {
						my Piece $adjacent-piece = self.piece-at: $possible;
						my CoOrd $adjacent-coord = indices-to-coord $possible;

						if defined $adjacent-piece { # capture or collision
							if $adjacent-piece.team != $piece.team { # not collision
								# only knights can move then capture
								if $current-dist == 1 {
									$final.set: Action.new: :from($pos), :to($adjacent-coord), :type(Capture);
								}
								elsif $piece.type == Knight {
									$final.set: Action.new: :from($pos), :to($working-coord),
											:attacking($adjacent-coord), :type(MoveCapture);
								}
							}
						}
						elsif $current-dist != 6 { # 6th round is for knights capturing only
							my Action $move .= new: :from($pos), :to($adjacent-coord), :type(Move);
							$working.set: $move unless $move ∈ $final;
						}
					}
				}
				$final.set($working.keys);
				$working.unset($old-working.keys);
			}

			$final.unset($trivial-action);
			@actions = $final.keys.Array;
		}

		my @pos-indices = coord-to-indices $pos;
		my @adjacents = @deltas.map({ @$_ Z+ @pos-indices }).grep({ 0 <= all($_) <= 7 });

		when Pikeman | Infantry {
			my $attacking-direction = $piece.team == White ?? 1 !! -1;
			for @adjacents -> $possible {
				my $possible-coord = indices-to-coord $possible;
				with self.piece-at: $possible {
					if .team != $piece.team && $possible[0] - @pos-indices[0] == $attacking-direction {
						@actions.push: Action.new: :from($pos), :attacking($possible-coord), :type(Capture);
					}
				}
				else {
					@actions.push: Action.new: :from($pos), :to($possible-coord), :type(Move);
				}
			}
		}

		when Archer {
			for @adjacents -> $possible {
				without self.piece-at: $possible {
					@actions.push: Action.new: :from($pos), :to(indices-to-coord $possible), :type(Move);
				}
			}

			# Easier (and probably more efficient) to just iterate over the board in this case
			for ^8 X ^8 -> ($rank, $file) {
				$_ = @!board[$rank;$file];
				if .defined && .team != $piece.team {
					if (($rank, $file) Z- @pos-indices).map(&abs).sum ≤ 3 {
						@actions.push: Action.new: :from($pos),
								:attacking(indices-to-coord $rank, $file), :type(Capture);
					}
				}
			}
		}
	}

	return @actions;
}

method apply-action(Action $action) returns Action {
	sub move($from, $to) {
		my ($from_rank, $from_file) = coord-to-indices $from;
		my ($to_rank, $to_file) = coord-to-indices $to;
		@!board[$to_rank;$to_file] = @!board[$from_rank;$from_file];
		@!board[$from_rank;$from_file] = Nil;
	}

	given $action.type {
		when Move {
			move $action.from, $action.to;
			return Action.new:
					from => $action.from,
					to   => $action.to,
					type => Move;
		}
		
		my $roll = (1..6).roll;
		my PieceType ($attacker, $defender) =
				self.piece-at($action.from).type,
				self.piece-at($action.attacking).type;

		my $was-successful = $roll ≥ %roll-needed-for{$attacker}.to-capture($defender);

		when Capture {
			move $action.from, $action.attacking if $was-successful;

			return Action.new:
					from      => $action.from,
					attacking => $action.attacking,
					type      => Capture,
					:$was-successful
					;
			
		}

		when MoveCapture {
			if $was-successful {
				move $action.from, $action.attacking;
			}
			else {
				move $action.from, $action.to;
			}

			return Action.new:
					from      => $action.from,
					attacking => $action.attacking,
					to        => $action.to,
					type      => MoveCapture,
					:$was-successful
					;
		}
	}
}

method end-turn {
	$!whose-turn = $!whose-turn == White ?? Black !! White;
}

method Str {
	my $str = '';
	my $empties = 0;
	for @!board.flat {
		if .defined {
			if $empties {
				$str ~= $empties;
				$empties = 0;
			}
			$str ~= .Str;
		}
		else {
			$empties++;
		}
	}

	if $empties {
		$str ~= $empties;
		$empties = 0;
	}

	return $str;
}

multi method gist(Board:D:) {
	my @board = @!board;
	@board.rotor(8)
		.reverse
		.map({ colored $_».gist.join(' '), 'on_255,212,128' })
		.join("\n");
}
multi method gist(Board:U:) {
	'Nil'
}
