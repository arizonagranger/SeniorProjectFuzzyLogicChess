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


	# -----  Actions  -----

	post -> 'act', :$action-str! {
		my Action $action .= from-str: $action-str;
		say '$action-str = ', $action-str, ', $action defined = ', defined $action;
		with $action {
			# TODO check that the action is valid for whose turn it is (probably implemented in Board)
			content 'text/plain', $board.apply-action($action).Str;
		}
		else {
			bad-request;
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
