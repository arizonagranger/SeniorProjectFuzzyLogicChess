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
	get 'new-game', :$color = 'White', :$type='Default' {
		content 'text/plain', $board.Str;
	}

	# -----  Queries  -----

	get 'piece-at', Board::CoOrd :$coord {
		# TODO
	}

	get 'moves-for', Board::CoOrd :$coord {
		# TODO
	}

	get 'is-done' {
		content 'text/plain', $board.is-game-ended;
	}

	get 'whose-turn {
		content 'text/plain', $board.whose-turn;
	}


	# -----  Actions  -----

	post 'act', :$action {
		# TODO
	}

	post 'end-turn' {
		# TODO
	}

	post 'save-state' {
		# TODO
	}

	post 'restore-state' {
		# TODO
	}
};

my Cro::Service $service = Cro::HTTP::Server.new:
	:host<localhost>,
	:port<4850>,
	:$application
	;

$service.start;

react whenever signal(SIGINT) {
	$service.stop;
	exit;
}
