SELECT vols.num_vol, ts_depart, ts_arrivee, code_origine, code_destination FROM departs 
JOIN vols ON vols.num_vol = departs.num_vol
JOIN liaisons ON vols.liaison = liaisons.id_liaison
JOIN (SELECT id_aeroports AS id_aeroport_destination, code AS code_destination, nom AS nom_destination FROM airline.aeroports) AS aeroports_destination
 ON liaisons.aeroport_destination = aeroports_destination.id_aeroport_destination
JOIN (SELECT id_aeroports AS id_aeroport_origine, code AS code_origine, nom AS nom_origine FROM airline.aeroports) AS aeroports_origine
 ON liaisons.aeroport_origine = aeroports_origine.id_aeroport_origine
WHERE departs.pilote_1 = '191851249560845' 
	OR departs.pilote_2 = '191851249560845' 
    OR departs.equipage_1 = '191851249560845'
    OR departs.equipage_2 = '191851249560845' 
    AND ts_depart > NOW();