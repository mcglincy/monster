#!/bin/bash

# digraph monster {
# room_id_1 [label="Great Hall"];
# room_id_2 [label="Void"];
# ...
# room_id_434 -> room_id_433 [label="w"];
# room_id_435 -> room_id_713 [label="n"];
# room_id_435 -> room_id_436 [label="s"];
# room_id_435 -> room_id_399 [label="u"];
# }

echo "digraph monster {" > room.dot
grep dig ../world/build_rooms.ev |sed 's/^\@dig //' |awk -F\; '{printf "%s [label=\"%s\"];\n",$2,$1}' >> room.dot
egrep '\@tel|\@open' ../world/build_exits.ev |./exits.pl  >> room.dot
echo "}" >> room.dot