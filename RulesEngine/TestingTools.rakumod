use Cro::HTTP::Client;

sub post($endpoint, *%args) {
	await (await Cro::HTTP::Client.post(
			  "http://localhost:4850/$endpoint"
			~ (%args.keys.elems ?? '?' !! '')
			~ %args.pairs.map({ .key ~ '=' ~ .value }).join('&'))
		).body
}

sub get($endpoint, *%args) {
	await (await Cro::HTTP::Client.get(
			  "http://localhost:4850/$endpoint"
			~ (%args.keys.elems ?? '?' !! '')
			~ %args.pairs.map({ .key ~ '=' ~ .value }).join('&'))
		).body
}
