use Cro::HTTP::Client;

sub post($endpoint, *%args) is export {
	await (await Cro::HTTP::Client.post(
			  "http://localhost:4850/$endpoint"
			~ (%args.keys.elems ?? '?' !! '')
			~ %args.pairs.map({ .key ~ '=' ~ (S/'>'/%3E/ given .value) }).join('&'))
		).body
}

sub get($endpoint, *%args) is export {
	for %args.keys {
		%args{$_} ~~ s/'>'/%3E/;
	}
	await (await Cro::HTTP::Client.get(
			  "http://localhost:4850/$endpoint"
			~ (%args.keys.elems ?? '?' !! '')
			~ %args.pairs.map({ .key ~ '=' ~ (S/'>'/%3E/ given .value) }).join('&'))
		).body
}
