use Cro::HTTP::Server;
use Cro::HTTP::Router;

use lib '.';
use Board;
use Action;
use Piece;

unit module RulesEngine;

my Board $board;
my Board @saved-states;

my $application = route {
	get -> 'new-game', :$color = 'White', :$type='Default' {
		$board .= new;
		content 'text/plain', $board.Str;
	}

	# -----  Queries  -----

	get -> 'game-state' {
		content 'text/plain', $board.Str;
	}

	get -> 'curr-action-idx' {
		content 'text/plain', ($board.actions.elems - 1).Str;
	}

	get -> 'actions-since', UInt :$action-idx! {
		if $action-idx ≥ $board.actions.elems {
			conflict 'text/plain', 'Index out of bounds';
		}
		else {
			content 'text/plain', $board.actions[$action-idx..*].join(',');
		}
	}

	get -> 'actions-since', Int :$action-idx! {
		if $action-idx.abs > $board.actions.elems {
			conflict 'text/plain', 'Index out of bounds';
		}
		else {
			content 'text/plain', $board.actions[*+$action-idx..*].join(',');
		}
	}

	get -> 'piece-at', CoOrd :$coord! {
		content 'text/plain', $board.piece-at($coord).Str;
	}

	get -> 'actions-for', CoOrd :$coord! {
		content 'text/plain', $board.actions-for($coord).join("\n");
	}

	get -> 'is-done' {
		content 'text/plain', $board.is-game-ended.Str;
	}

	get -> 'whose-turn' {
		content 'text/plain', $board.whose-turn.Str;
	}

	get -> 'pieces', :$team!, :$corp = Nil {
		content 'text/plain', $board.pieces($team, $corp).join(',');

		CATCH {
			default {
				conflict 'text/plain', .message;
				say 'Exception caught in `pieces` endpoint:';
				.say;
			}
		}
	}

	get -> 'most-recent-roll' {
		content 'text/plain', ($board.most-recent-roll or -1).Str;
	}


	# -----  Actions  -----

	post -> 'act', :$action-str! {
		my Action $action .= from-str: $action-str;
		with $action {
			# TODO check that the action is valid for whose turn it is (probably implemented in Board)
			content 'text/plain', $board.apply-action($action).Str;
		}
		else {
			bad-request;
		}
	}

	post -> 'delegate', CoOrd :$coord!, :$corp! {
		$board.delegate($coord, $corp);

		CATCH {
			default {
				conflict 'text/plain', .message;
			}
		}
	}

	post -> 'end-turn' {
		$board.end-turn;
	}

	post -> 'save-state' {
		@saved-states.push: $board.clone;
	}

	post -> 'restore-state' {
		if @saved-states.elems == 0 {
			response.status = 409;
		}
		else {
			$board = @saved-states.pop;
		}
	}
};

my Cro::Service $service = Cro::HTTP::Server.new:
	:host<localhost>,
	:port<4850>,
	:$application
	;

$service.start;

for $*IN.lines {
	when 'v' {
		say $board;
	}

	when 'e' {
		$service.stop;
		exit;
	}
}
