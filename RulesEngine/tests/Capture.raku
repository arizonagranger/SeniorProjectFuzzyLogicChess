use lib '..';
use TestingTools;

get 'new-game';
post 'act', action-str => 'e2>e3';
post 'end-turn';
post 'act', action-str => 'd7>d6';
post 'end-turn';
post 'act', action-str => 'e3>e4';
post 'end-turn';
post 'act', action-str => 'd6>d5';
post 'end-turn';
post 'act', action-str => 'e4xd5=s';
