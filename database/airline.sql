-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: airline
-- ------------------------------------------------------
-- Server version	5.7.24-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aeroports`
--

DROP TABLE IF EXISTS `aeroports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aeroports` (
  `id_aeroports` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(3) DEFAULT NULL,
  `nom` varchar(100) DEFAULT NULL,
  `pays` varchar(45) DEFAULT NULL,
  `ville` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_aeroports`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aeroports`
--

LOCK TABLES `aeroports` WRITE;
/*!40000 ALTER TABLE `aeroports` DISABLE KEYS */;
INSERT INTO `aeroports` VALUES (1,'CDG','Aéroport de Paris-Charles-de-Gaulle','France','Paris'),(16,'YUL','Aéroport international Pierre-Elliott-Trudeau','Canada','Montréal'),(17,'YQB','Aéroport international Jean-Lesage','Canada','Québec'),(18,'MEX','Aéroport international Benito-Juárez','Mexique','Mexico'),(19,'ATL','Aéroport international Hartsfield-Jackson','États-Unis','Atlanta'),(20,'JFK','Aéroport international John-F.-Kennedy','États-Unis','New-York'),(21,'HND','Aéroport international Haneda','Japon','Tokyo'),(22,'PEK','Aéroport international de Pékin-Capitale','Chine','Pékin'),(23,'BER','Aéroport Brandenburg-Willy-Brandt','Allemagne','Berlin'),(24,'BRU','Aéroport de Bruxelles-National','Belgique','Bruxelles'),(25,'MAD','Aéroport Adolfo Suárez Madrid-Barajas','Espagne','Madrid'),(26,'LYS','Aéroport de Lyon-Saint-Exupéry','France','Lyon'),(27,'LHR','Aéroport de Londres-Heathrow','Royaume-Uni','Londres'),(28,'SVO','Aéroport de Moscou-Cheremetievo','Russie','Moscou'),(42,'DTW','Aéroport métropolitain de Détroit','États-Unis','Detroit'),(43,'SYD','Aéroport Kingsford-Smith de Sydney','Australie','Sydney'),(44,'NOU','Aéroport international de Nouméa-La Tontouta','Nouvelle-Calédonie','Nouméa'),(45,'GIG','Aéroport international de Rio de Janeiro-Galeão','Brésil','Rio de Janeiro'),(46,'GRU','Aéroport international de São Paulo-Guarulhos','Brésil','São Paulo'),(47,'EZE','Aéroport international d\'Ezeiza','Argentine','Buenos Aires'),(48,'EDI','Aéroport d\'Édimbourg','Écosse','Édimbourg'),(49,'MXP','Aéroport de Milan Malpensa','Italie','Milan'),(50,'LIS','Aéroport Humberto Delgado de Lisbonne','Portugal','Lisbonne'),(51,'LAX','Aéroport international de Los Angeles','États-Unis','Los Angeles'),(52,'ZRH','Aéroport international de Zurich','Suisse','Zurich'),(53,'FCO','Aéroport Léonard-de-Vinci de Rome Fiumicino','Italie','Rome'),(54,'AKL','Aéroport d\'Auckland','Nouvelle-Zélande','Auckland'),(55,'CAI','Aéroport international du Caire','Égypte','Le Caire');
/*!40000 ALTER TABLE `aeroports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appareils`
--

DROP TABLE IF EXISTS `appareils`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `appareils` (
  `immatriculation` varchar(45) NOT NULL,
  `type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`immatriculation`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appareils`
--

LOCK TABLES `appareils` WRITE;
/*!40000 ALTER TABLE `appareils` DISABLE KEYS */;
INSERT INTO `appareils` VALUES ('A5ZZ','B772'),('A89B','A321'),('F-89H','A410'),('F-GKXO','A320-214'),('F-GSPE','777-228'),('F-GTAH','A321-211'),('F-HCBN','A320'),('F-HEPB','A320-214'),('F-HPJA','A380-861'),('F-HPJB','A380-861'),('F-L568','A325'),('H578E','A320'),('N1BC','A333'),('N1YC','B520'),('N2YT','B763'),('NX56','B301'),('NY3U','B555'),('R87JU','A320'),('T752','B733'),('Y846','B711'),('YTOP','A317');
/*!40000 ALTER TABLE `appareils` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billets`
--

DROP TABLE IF EXISTS `billets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `billets` (
  `num_billet` bigint(16) NOT NULL,
  `prix` decimal(4,0) DEFAULT NULL,
  `ts_emission` datetime DEFAULT NULL,
  `num_depart` int(11) DEFAULT NULL,
  `num_passager` int(11) DEFAULT NULL,
  KEY `num_depart_idx` (`num_depart`),
  KEY `num_client_idx` (`num_passager`),
  CONSTRAINT `num_client` FOREIGN KEY (`num_passager`) REFERENCES `passagers` (`id_passager`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `num_depart` FOREIGN KEY (`num_depart`) REFERENCES `departs` (`id_departs`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billets`
--

LOCK TABLES `billets` WRITE;
/*!40000 ALTER TABLE `billets` DISABLE KEYS */;
INSERT INTO `billets` VALUES (165746583,61,'2018-08-26 08:40:00',2,1),(1085015469,45,'2018-07-04 11:23:00',2,2),(1875414696,420,'2018-05-06 15:05:00',1,3),(5164348346,45,'2018-07-07 17:54:00',2,4),(5302972100,570,'2018-09-06 15:05:00',2,5);
/*!40000 ALTER TABLE `billets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departs`
--

DROP TABLE IF EXISTS `departs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `departs` (
  `num_vol` varchar(45) DEFAULT NULL,
  `pilote_1` bigint(16) DEFAULT NULL,
  `pilote_2` bigint(16) DEFAULT NULL,
  `equipage_1` bigint(16) DEFAULT NULL,
  `equipage_2` bigint(16) DEFAULT NULL,
  `nbr_places_libres` int(11) DEFAULT NULL,
  `immatriculation` varchar(45) DEFAULT NULL,
  `id_departs` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_departs`),
  KEY `pilote_1_idx` (`pilote_1`),
  KEY `pilote_2_idx` (`pilote_2`),
  KEY `equipage_1_idx` (`equipage_1`),
  KEY `equipage_2_idx` (`equipage_2`),
  KEY `immaculation_appareil_idx` (`immatriculation`),
  KEY `num_vol_idx` (`num_vol`),
  CONSTRAINT `equipage_1` FOREIGN KEY (`equipage_1`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `equipage_2` FOREIGN KEY (`equipage_2`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `immaculation_appareil` FOREIGN KEY (`immatriculation`) REFERENCES `appareils` (`immatriculation`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `num_vol` FOREIGN KEY (`num_vol`) REFERENCES `vols` (`num_vol`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pilote_1` FOREIGN KEY (`pilote_1`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `pilote_2` FOREIGN KEY (`pilote_2`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departs`
--

LOCK TABLES `departs` WRITE;
/*!40000 ALTER TABLE `departs` DISABLE KEYS */;
INSERT INTO `departs` VALUES ('AFR348',191851249560845,163577693139738,174718143121594,292635691720225,23,'A5ZZ',1),('AFR7644',275964135451744,182942912944414,293109716948355,292108643334472,6,'F-GKXO',2),('DAL405',191851249560845,189145542576748,293109716948355,174718143121594,1,'N1BC',3),('CH425',231789586954852,191851249560845,258970132546890,292108643334472,56,'A5ZZ',4),('US872',296301254103578,189145542576748,187235698042356,256898512354692,21,'A89B',5),('FR875',247512369852012,275964135451744,187904680723891,165023458715204,68,'F-89H',6),('ME547',141032001558965,152465893204588,236987104532015,268790136987546,87,'F-GKXO',7),('FR841',231789586954852,191851249560845,258970132546890,292108643334472,45,'F-GSPE',8),('BE213',178452963236520,178958632105745,136970312546087,278934580438812,24,'F-GTAH',9),('UK38',189145542576748,296301254103578,187235698042356,256898512354692,23,'F-HCBN',10),('MA25K',275964135451744,285123652458742,293109716948355,165023458715204,12,'F-HEPB',11),('FR654',287154124123620,152465893204588,136971979281230,257890356843120,56,'F-HPJB',12),('FR842',178958632105745,182942912944414,120357890497680,278934580438812,23,'F-HPJA',13),('EG89H',152632542152789,163577693139738,174718143121594,292635691720225,12,'F-L568',14),('AUS87',247512369852012,103896452135789,167928434492920,237921389138920,2,'H578E',15),('FR652',178452963236520,163577693139738,135789204687350,136970312546087,65,'N1BC',16),('AUS714',123089562458325,154201336987554,103689702546828,234897298159460,24,'N1YC',17),('SP265',178958632105745,105632789452136,174718143121594,187904680723891,54,'N2YT',18),('SP124',205632789416507,158741254693025,207894984387387,236987104532015,21,'NX56',19),('FR812',285123652458742,152632542152789,178742013520154,293109716948355,54,'NY3U',20),('UK832',103896452135789,247512369852012,237921389138920,167928434492920,8,'R87JU',21),('IT542',152465893204588,287154124123620,268790136987546,257890356843120,25,'T752',22),('NZ845',165302154236985,154201336987554,138919719781828,103689702546828,14,'Y846',23),('ZR432',158741254693025,182942912944414,168790994894086,135970591671679,1,'YTOP',24),('CH426',231789586954852,191851249560845,258970132546890,292108643334472,56,'A5ZZ',46),('US873',296301254103578,189145542576748,187235698042356,256898512354692,21,'A89B',47),('FR876',247512369852012,275964135451744,187904680723891,165023458715204,68,'F-89H',48),('ME548',141032001558965,152465893204588,236987104532015,268790136987546,87,'F-GKXO',49),('FR840',231789586954852,191851249560845,258970132546890,292108643334472,45,'F-GSPE',50),('UK39',189145542576748,296301254103578,187235698042356,256898512354692,23,'F-HCBN',51),('MA26K',275964135451744,285123652458742,293109716948355,165023458715204,12,'F-HEPB',52),('FR655',287154124123620,152465893204588,136971979281230,257890356843120,56,'F-HPJB',53),('FR843',178958632105745,182942912944414,120357890497680,278934580438812,23,'F-HPJA',54),('EG90H',152632542152789,163577693139738,174718143121594,292635691720225,12,'F-L568',55),('AUS88',247512369852012,103896452135789,167928434492920,237921389138920,2,'H578E',56),('FR653',178452963236520,163577693139738,135789204687350,136970312546087,65,'N1BC',57),('AUS715',123089562458325,154201336987554,103689702546828,234897298159460,24,'N1YC',58),('SP266',178958632105745,105632789452136,174718143121594,187904680723891,54,'N2YT',59),('SP125',205632789416507,158741254693025,207894984387387,236987104532015,21,'NX56',60),('FR813',285123652458742,152632542152789,178742013520154,293109716948355,54,'NY3U',61),('UK833',103896452135789,247512369852012,237921389138920,167928434492920,8,'R87JU',62),('IT543',152465893204588,287154124123620,268790136987546,257890356843120,25,'T752',63),('NZ846',165302154236985,154201336987554,138919719781828,103689702546828,14,'Y846',64),('ZR433',158741254693025,182942912944414,168790994894086,135970591671679,1,'YTOP',65);
/*!40000 ALTER TABLE `departs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employes`
--

DROP TABLE IF EXISTS `employes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employes` (
  `numero_securite_sociale` bigint(16) NOT NULL,
  `prenom` varchar(45) DEFAULT NULL,
  `nom` varchar(45) DEFAULT NULL,
  `adresse` varchar(45) DEFAULT NULL,
  `ville` varchar(45) DEFAULT NULL,
  `pays` varchar(45) DEFAULT NULL,
  `salaire` decimal(15,0) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`numero_securite_sociale`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employes`
--

LOCK TABLES `employes` WRITE;
/*!40000 ALTER TABLE `employes` DISABLE KEYS */;
INSERT INTO `employes` VALUES (103689702546828,'Kato','Hiroyuki','78 Toshika street','Tokyo','Japon',3201,'naviguant'),(103896452135789,'Oliver','Ebdy','Castle avenue','Glasgow','Écosse',5302,'naviguant'),(105632789452136,'Arturo','Monhez','98 av. del Christo','Rio de Janeiro','Brésil',6302,'naviguant'),(120357890497680,'Ulrich','Friedman','875 Stutgartt strasse','Berlin','Allemagne',2310,'naviguant'),(123089562458325,'Loé','Etini','23 Main street','Nouméa','Nouvelle-Calédonie',5240,'naviguant'),(135789204687350,'Sam','Searle','235B Oxford Street','Londres','Royaume-Uni',2780,'naviguant'),(135970591671679,'Martin','Robadey','630 Alps av.','Zurich','Suisse',3012,'naviguant'),(136970312546087,'Vladimir','Poutane','874 cold war street','Moscou','Russie',23000,'naviguant'),(136971979281230,'Robin','Wilms','650 Anchor street','Amsterdam','Pays-Bas',1032,'naviguant'),(138919719781828,'James','Merchant','852 Main street','Auckland','Nouvelle-Zélande',3012,'naviguant'),(141032001558965,'Carlos','Sanchez','852 calle Grande','Mexico','Mexique',3205,'naviguant'),(152465893204588,'Fernando','Savio','852 av. Domingos','Lisbonne','Portugal',3205,'naviguant'),(152632542152789,'Mathieu','Legrand','41 rue Garibaldi','Bordeaux','France',6100,'naviguant'),(154201336987554,'Ryu','Takeshi','89 Main street','Tokyo','Japon',4560,'naviguant'),(158741254693025,'Alexandre','Cornut','875 Moutains street','Zurich','Suisse',5420,'naviguant'),(163577693139738,'Quentin','Petit','6 avenue du Bois','Lille','France',4200,'naviguant'),(165023458715204,'Guillaume','Leclercq','78 rue des 3 cailloux','Lille','France',1452,'naviguant'),(165302154236985,'Marek','Church','879 Golf avenue','Auckland','Nouvelle-Zélande',5204,'naviguant'),(167928434492920,'John','Brown','960 Kingston av.','Édimbourg','Écosse',2305,'naviguant'),(168790994894086,'Andrés','Sanchez','203B Calle Milano','Turin','Italie',1302,'naviguant'),(174718143121594,'David','Bertrand','11 rue du Bout du Chemin','Amiens','France',2900,'naviguant'),(178019734623941,'Grégoire','Pierre','12 rue de Paris','Orléans','France',3000,'au_sol'),(178452963236520,'Franck','Dubronvnic','85th NW Street','Moscou','Russie',4125,'naviguant'),(178742013520154,'Trevor','Edwards','45 Umbrellas street','Québec','Canada',2031,'naviguant'),(178958632105745,'Jules','Marchand','548 av. Hotel de ville','Bruxelles','Belgique',2450,'naviguant'),(182942912944414,'Aymerick','Jean','23 North Av.','Berlin','Allemagne',5100,'naviguant'),(187235698042356,'Braden','Ketch','840B SW street','Atlanta','États-Unis',2305,'naviguant'),(187904680723891,'Martin','Salamba','630 Calle Arribas','Buenos Aires','Brésil',3490,'naviguant'),(189145542576748,'Mark','Porter','63-8059 Donec St','New-York','États-Unis',5000,'naviguant'),(191851249560845,'Alexandre','Martin','8 rue Cul de Sac','Rennes','France',6000,'naviguant'),(205632789416507,'Maria','Arribas','5423 av. Sabajados','Buenos Aires','Argentine',4230,'naviguant'),(207894984387387,'Licia','Figueiredo','980 Calle Baja','São Paulo','Brésil',3201,'naviguant'),(231789586954852,'Cheng','Sun','63 Little Italy street','Shanghai','Chine',3980,'naviguant'),(234897298159460,'Tama','Tahiri','846 Coconut str.','Nouméa','Nouvelle-Calédonie',1630,'naviguant'),(236987104532015,'Africa','Marcolis','936 pueblo av.','Mexico','Mexique',1345,'naviguant'),(237921389138920,'Danielle','Roel','213 Super cool av.','Sydney','Australie',2360,'naviguant'),(247512369852012,'Courtney','Lawson','45 Beach avenue','Sydney','Australie',4520,'naviguant'),(256898512354692,'Mireille','Mathieu','4 avenue du Général de Gaulle','Roubaix','France',2350,'naviguant'),(257890356843120,'Marta','Calvatores','865 middle str.','Séville','Espagne',2540,'naviguant'),(258970132546890,'Vi','Le','850 Main av.','Pékin','Chine',1302,'naviguant'),(268790136987546,'Maria','Agrada','562 Calle del puerto','Porto','Portugal',2840,'naviguant'),(275964135451744,'Jeanne','Fournier','12 rue Victorien Sardou','Lyon','France',6500,'naviguant'),(278934580438812,'Sophie','Chenaux','980 Station av.','Bruxelles','Belgique',3204,'naviguant'),(282123825733664,'Marie','Dubois','45 cours Lafayette','Lyon','France',2500,'au_sol'),(285123652458742,'Charlotte','André','8 rue du Lac','Lyon','France',4520,'naviguant'),(287154124123620,'Lucia','Batisti','87 pasta avenue','Milan','Italie',6502,'naviguant'),(292108643334472,'Helena','Martinez','4302 Montes, Av.','Madrid','Espagne',3200,'naviguant'),(292635691720225,'Helen','Parker','7895 Sagittis Avenue','Londres','Royaume-Uni',3600,'naviguant'),(293109716948355,'Angele','Perrin','3666 Non, St.','Amsterdam','Pays-Bas',3800,'naviguant'),(296301254103578,'Margaux','Dulieu','984 Victoria street','Montréal','Canada',5620,'naviguant');
/*!40000 ALTER TABLE `employes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `liaisons`
--

DROP TABLE IF EXISTS `liaisons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `liaisons` (
  `id_liaison` int(11) NOT NULL AUTO_INCREMENT,
  `aeroport_origine` int(11) DEFAULT NULL,
  `aeroport_destination` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_liaison`),
  KEY `aeroport_origine_idx` (`aeroport_origine`),
  KEY `aeroport_destination_idx` (`aeroport_destination`),
  CONSTRAINT `aeroport_destination` FOREIGN KEY (`aeroport_destination`) REFERENCES `aeroports` (`id_aeroports`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `aeroport_origine` FOREIGN KEY (`aeroport_origine`) REFERENCES `aeroports` (`id_aeroports`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `liaisons`
--

LOCK TABLES `liaisons` WRITE;
/*!40000 ALTER TABLE `liaisons` DISABLE KEYS */;
INSERT INTO `liaisons` VALUES (1,1,20),(2,20,1),(3,1,16),(4,16,1),(5,16,18),(6,18,16),(7,16,20),(8,20,16),(9,26,25),(10,25,26),(11,26,27),(12,27,26),(13,24,1),(14,1,24),(15,23,1),(16,1,23),(17,1,25),(18,25,1),(19,27,42),(20,42,27),(21,1,22),(22,22,1),(23,25,23),(24,23,25),(25,26,1),(26,1,26),(27,43,27),(28,27,43),(29,55,1),(30,1,55),(31,43,44),(32,44,43),(33,1,45),(34,45,1),(35,46,47),(36,47,46),(37,46,18),(38,18,46),(39,1,51),(40,51,1),(41,27,48),(42,48,27),(43,49,50),(44,50,49),(45,52,53),(46,53,52),(47,54,21),(48,21,54),(49,1,46),(50,46,1);
/*!40000 ALTER TABLE `liaisons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `naviguants`
--

DROP TABLE IF EXISTS `naviguants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `naviguants` (
  `numero_securite_sociale` bigint(16) NOT NULL,
  `nbr_heures_vol` int(11) DEFAULT NULL,
  `fonction` varchar(45) DEFAULT NULL,
  `num_licence_pilote` bigint(16) DEFAULT NULL,
  PRIMARY KEY (`numero_securite_sociale`),
  CONSTRAINT `num_secu_sociale` FOREIGN KEY (`numero_securite_sociale`) REFERENCES `employes` (`numero_securite_sociale`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `naviguants`
--

LOCK TABLES `naviguants` WRITE;
/*!40000 ALTER TABLE `naviguants` DISABLE KEYS */;
INSERT INTO `naviguants` VALUES (103689702546828,42,'steward',NULL),(103896452135789,74,'pilote',3641025),(105632789452136,36,'pilote',5462038),(120357890497680,24,'steward',NULL),(123089562458325,45,'pilote',7850135),(135789204687350,24,'steward',NULL),(135970591671679,15,'steward',NULL),(136970312546087,11,'steward',NULL),(136971979281230,80,'steward',NULL),(138919719781828,28,'steward',NULL),(141032001558965,84,'pilote',5420369),(152465893204588,11,'pilote',7410258),(152632542152789,24,'pilote',8753625),(154201336987554,13,'pilote',4563258),(158741254693025,52,'pilote',8450563),(163577693139738,12,'pilote',7045185),(165023458715204,12,'steward',NULL),(165302154236985,15,'pilote',4102538),(167928434492920,18,'steward',NULL),(168790994894086,67,'steward',NULL),(174718143121594,8,'steward',NULL),(178452963236520,7,'pilote',8523694),(178742013520154,13,'steward',NULL),(178958632105745,12,'pilote',4520369),(182942912944414,24,'pilote',1128094),(187235698042356,51,'steward',NULL),(187904680723891,16,'steward',NULL),(189145542576748,15,'pilote',5884764),(191851249560845,11,'pilote',1316780),(205632789416507,41,'pilote',3021587),(207894984387387,9,'hôtesse',NULL),(231789586954852,42,'pilote',8932056),(234897298159460,3,'hôtesse',NULL),(236987104532015,62,'hôtesse',NULL),(237921389138920,35,'hôtesse',NULL),(247512369852012,15,'pilote',8750215),(256898512354692,0,'hôtesse',NULL),(257890356843120,53,'hôtesse',NULL),(258970132546890,23,'hôtesse',NULL),(268790136987546,36,'hôtesse',NULL),(275964135451744,5,'pilote',4926286),(278934580438812,32,'hôtesse',NULL),(285123652458742,0,'pilote',6842056),(287154124123620,4,'pilote',9620345),(292108643334472,18,'hôtesse',NULL),(292635691720225,7,'hôtesse',NULL),(293109716948355,17,'hôtesse',NULL),(296301254103578,65,'pilote',2140536);
/*!40000 ALTER TABLE `naviguants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passagers`
--

DROP TABLE IF EXISTS `passagers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `passagers` (
  `id_passager` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(45) DEFAULT NULL,
  `prenom` varchar(45) DEFAULT NULL,
  `adresse` varchar(45) DEFAULT NULL,
  `ville` varchar(45) DEFAULT NULL,
  `pays` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_passager`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passagers`
--

LOCK TABLES `passagers` WRITE;
/*!40000 ALTER TABLE `passagers` DISABLE KEYS */;
INSERT INTO `passagers` VALUES (1,'Debouck','Franck','36 avenue Guy de Collongue','Écully','France'),(2,'Raymond','Deubaze','1 allée du Lac','Lyon','France'),(3,'John','Doe','504-4886 Accumsan Ave','New-York','États-Unis'),(4,'Camille','Dupont','14 boulevard Ménilmontant','Paris','France'),(5,'Juan','Rafael','9408 Maecenas Av.','Madrid','Espagne'),(6,'Latifah','Oub','Ap #209-1213 Cursus. Road','Londres','Royaume-Uni');
/*!40000 ALTER TABLE `passagers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vols`
--

DROP TABLE IF EXISTS `vols`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vols` (
  `num_vol` varchar(45) NOT NULL,
  `ts_depart` timestamp NULL DEFAULT NULL,
  `ts_arrivee` timestamp NULL DEFAULT NULL,
  `liaison` int(11) DEFAULT NULL,
  PRIMARY KEY (`num_vol`),
  KEY `liaison_idx` (`liaison`),
  CONSTRAINT `liaison` FOREIGN KEY (`liaison`) REFERENCES `liaisons` (`id_liaison`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vols`
--

LOCK TABLES `vols` WRITE;
/*!40000 ALTER TABLE `vols` DISABLE KEYS */;
INSERT INTO `vols` VALUES ('AFR348','2018-10-18 17:05:00','2018-10-19 00:40:00',1),('AFR7644','2018-10-19 12:15:00','2018-10-19 13:30:00',10),('AUS714','2018-12-07 07:33:00','2018-12-07 10:15:00',31),('AUS715','2018-12-14 07:33:00','2018-12-14 10:15:00',31),('AUS87','2018-12-06 17:00:00','2018-12-07 02:20:00',27),('AUS88','2018-12-13 17:00:00','2018-12-14 02:20:00',27),('BE213','2018-12-05 14:10:00','2018-12-05 17:05:00',13),('CH425','2018-12-03 03:45:00','2018-12-03 13:20:00',22),('CH426','2018-12-10 03:45:00','2018-12-10 13:20:00',22),('DAL405','2018-10-18 08:40:00','2018-10-18 13:05:00',18),('EG89H','2018-12-06 12:15:00','2018-12-06 17:15:00',30),('EG90H','2018-12-13 12:15:00','2018-12-13 17:15:00',30),('FR652','2018-12-07 06:12:00','2018-12-07 22:21:00',33),('FR653','2018-12-14 06:12:00','2018-12-14 22:21:00',33),('FR654','2018-12-06 08:15:00','2018-12-06 09:45:00',25),('FR655','2018-12-13 08:15:00','2018-12-13 09:45:00',25),('FR812','2018-12-08 03:15:00','2018-12-08 09:24:00',39),('FR813','2018-12-15 03:15:00','2018-12-15 09:24:00',39),('FR840','2018-12-12 09:15:00','2018-12-12 19:30:00',21),('FR841','2018-12-05 09:15:00','2018-12-05 19:30:00',21),('FR842','2018-12-06 11:00:00','2018-12-06 13:45:00',16),('FR843','2018-12-13 11:00:00','2018-12-13 13:45:00',16),('FR875','2018-12-04 05:15:00','2018-12-04 17:23:00',49),('FR876','2018-12-11 05:15:00','2018-12-11 17:23:00',49),('IT542','2018-12-08 10:35:00','2018-12-08 14:15:00',43),('IT543','2018-12-15 10:35:00','2018-12-15 14:15:00',43),('MA25K','2018-12-06 04:45:00','2018-12-06 09:35:00',23),('MA26K','2018-12-13 04:45:00','2018-12-13 09:35:00',23),('ME547','2018-12-05 05:00:00','2018-12-05 10:05:00',6),('ME548','2018-12-12 05:00:00','2018-12-12 10:05:00',6),('NZ845','2018-12-08 12:15:00','2018-12-08 22:54:00',47),('NZ846','2018-12-15 12:15:00','2018-12-15 22:54:00',47),('SP124','2018-12-07 18:00:00','2018-12-07 22:35:00',35),('SP125','2018-12-14 18:00:00','2018-12-14 22:35:00',35),('SP265','2018-12-07 11:45:00','2018-12-07 21:35:00',37),('SP266','2018-12-14 11:45:00','2018-12-14 21:35:00',37),('UK38','2018-12-05 16:50:00','2018-12-06 00:25:00',19),('UK39','2018-12-12 16:50:00','2018-12-13 00:25:00',19),('UK832','2018-12-08 04:35:00','2018-12-08 06:50:00',41),('UK833','2018-12-15 04:35:00','2018-12-15 06:50:00',41),('US872','2018-12-03 09:35:00','2018-12-03 19:05:00',20),('US873','2018-12-10 09:35:00','2018-12-10 19:05:00',20),('ZR432','2018-12-08 13:45:00','2018-12-08 16:45:00',45),('ZR433','2018-12-15 13:45:00','2018-12-15 16:45:00',45);
/*!40000 ALTER TABLE `vols` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-11-30  0:49:56
