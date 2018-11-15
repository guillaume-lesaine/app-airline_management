SELECT nom, 
       prenom,
       fonction,
       naviguants_vols.naviguant, 
	   naviguants_vols.num_vol
FROM (
	(SELECT pilote_1 AS naviguant, num_vol
		FROM airline.departs)
	UNION DISTINCT
	(SELECT pilote_2 AS naviguant, num_vol
		FROM airline.departs)
	UNION DISTINCT 
    (SELECT equipage_1 AS naviguant, num_vol
		FROM airline.departs)
	UNION DISTINCT
    (SELECT equipage_2 AS naviguant, num_vol
		FROM airline.departs)
) AS naviguants_vols
JOIN airline.vols ON vols.num_vol = naviguants_vols.num_vol
JOIN airline.employes ON employes.numero_securite_sociale = naviguants_vols.naviguant
JOIN airline.naviguants ON naviguants.numero_securite_sociale = naviguants_vols.naviguant
WHERE ts_depart < NOW() AND ts_arrivee > NOW();