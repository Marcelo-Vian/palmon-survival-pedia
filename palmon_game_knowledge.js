/*
 * Knowledge layer for the local Palmon advisor.
 * Catalog art and form relationships come from the installed XAPK assets.
 * The competitive tier is a dated reference point, never a substitute for
 * the editable account state stored by the profile advisor.
 */
(() => {
  const CATALOG = [
  {
    "id": "Zapantis",
    "base": "Zapantis",
    "evolved": "Shockmantis",
    "mega": "",
    "element": "Eletrico",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Zapantis_5033.png",
    "imageEvolved": "images/Shockmantis_5033_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Mammolith",
    "base": "Mammolith",
    "evolved": "Prismalith",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "Tank",
    "image": "images/Mammolith_5024.png",
    "imageEvolved": "images/Prismalith_5024_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Embergeist",
    "base": "Embergeist",
    "evolved": "Pyregeist",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "Tank",
    "image": "images/Embergeist_5026.png",
    "imageEvolved": "images/Pyregeist_5026_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Hexkit",
    "base": "Hexkit",
    "evolved": "Cinderpurr",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Hexkit_5035.png",
    "imageEvolved": "images/Cinderpurr_5035_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Rootwarden",
    "base": "Rootwarden",
    "evolved": "Thornkeeper",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Rootwarden_5034.png",
    "imageEvolved": "images/Thornkeeper_5034_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Glacewing",
    "base": "Glacewing",
    "evolved": "Cryovern",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Glacewing_5023.png",
    "imageEvolved": "images/Cryovern_5023_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Thundertooth",
    "base": "Thundertooth",
    "evolved": "Thundermane",
    "mega": "",
    "element": "Eletrico",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Thundertooth_5025.png",
    "imageEvolved": "images/Thundermane_5025_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Plunderjaw",
    "base": "Plunderjaw",
    "evolved": "Dreadmaw",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Plunderjaw_5032.png",
    "imageEvolved": "images/Dreadmaw_5032_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Ghillant",
    "base": "Ghillant",
    "evolved": "Chefeuillier",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "Tank",
    "image": "images/Ghillant_5005.png",
    "imageEvolved": "images/Chefeuillier_5005_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Statchew",
    "base": "Statchew",
    "evolved": "Anubeast",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "Tank",
    "image": "images/Statchew_5008.png",
    "imageEvolved": "images/Anubeast_5008_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Regalion",
    "base": "Regalion",
    "evolved": "Lionarch",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Regalion_5019.png",
    "imageEvolved": "images/Lionarch_5019_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Fulgairy",
    "base": "Fulgairy",
    "evolved": "Keraunosaur",
    "mega": "",
    "element": "Eletrico",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Fulgairy_5016.png",
    "imageEvolved": "images/Keraunosaur_5016_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Gnashley",
    "base": "Gnashley",
    "evolved": "Gnashfin",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Gnashley_5027.png",
    "imageEvolved": "images/Gnashfin_5027_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Hoofrit",
    "base": "Hoofrit",
    "evolved": "Flaries",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Hoofrit_5017.png",
    "imageEvolved": "images/Flaries_5017_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Salamantis",
    "base": "Salamantis",
    "evolved": "Silvaurus",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Salamantis_5015.png",
    "imageEvolved": "images/Silvaurus_5015_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Battereina",
    "base": "Battereina",
    "evolved": "Ampereina",
    "mega": "",
    "element": "Eletrico",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Battereina_5020.png",
    "imageEvolved": "images/Ampereina_5020_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Revontulet",
    "base": "Revontulet",
    "evolved": "Vulpyrean",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Revontulet_5021.png",
    "imageEvolved": "images/Vulpyrean_5021_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Spookaboo",
    "base": "Spookaboo",
    "evolved": "",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Spookaboo_5030.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Dolphriend",
    "base": "Dolphriend",
    "evolved": "Adolphonis",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Dolphriend_5006.png",
    "imageEvolved": "images/Adolphonis_5006_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Magmolin",
    "base": "Magmolin",
    "evolved": "Obsidrake",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Magmolin_5011.png",
    "imageEvolved": "images/Obsidrake_5011_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Kungpaw",
    "base": "Kungpaw",
    "evolved": "Kungfury",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Kungpaw_5031.png",
    "imageEvolved": "images/Kungfury_5031_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Blazeal",
    "base": "Blazeal",
    "evolved": "Wildfuror",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Blazeal_5009.png",
    "imageEvolved": "images/Wildfuror_5009_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Abuzzinian",
    "base": "Abuzzinian",
    "evolved": "Servolt",
    "mega": "",
    "element": "Eletrico",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Abuzzinian_5007.png",
    "imageEvolved": "images/Servolt_5007_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Pipistrigoi",
    "base": "Pipistrigoi",
    "evolved": "Azurostrigoi",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Pipistrigoi_5028.png",
    "imageEvolved": "images/Azurostrigoi_5028_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Baboom",
    "base": "Baboom",
    "evolved": "Rumbkey",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Baboom_5010.png",
    "imageEvolved": "images/Rumbkey_5010_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Limudroid",
    "base": "Limudroid",
    "evolved": "Bunodroid",
    "mega": "",
    "element": "Eletrico",
    "rarity": "UR",
    "role": "Suporte/controle",
    "image": "images/Limudroid_5018.png",
    "imageEvolved": "images/Bunodroid_5018_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Ninjump",
    "base": "Ninjump",
    "evolved": "Bufonobi",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Ninjump_5002.png",
    "imageEvolved": "images/Bufonobi_5002_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Fingenue",
    "base": "Fingenue",
    "evolved": "Finnabelle",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Fingenue_5013.png",
    "imageEvolved": "images/Finnabelle_5013_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Barkplug",
    "base": "Barkplug",
    "evolved": "Wattweiler",
    "mega": "",
    "element": "Eletrico",
    "rarity": "UR",
    "role": "DPS frente/bruiser",
    "image": "images/Barkplug_5001.png",
    "imageEvolved": "images/Wattweiler_5001_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Escarffier",
    "base": "Escarffier",
    "evolved": "Essaucier",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "Suporte/controle",
    "image": "images/Escarffier_5022.png",
    "imageEvolved": "images/Essaucier_5022_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Mantleray",
    "base": "Mantleray",
    "evolved": "Sorceray",
    "mega": "",
    "element": "Eletrico",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Mantleray_5004.png",
    "imageEvolved": "images/Sorceray_5004_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Surveilynx",
    "base": "Surveilynx",
    "evolved": "Camouflynx",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Surveilynx_5012.png",
    "imageEvolved": "images/Camouflynx_5012_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Oleana",
    "base": "Oleana",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Oleana_5029.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Lucidina",
    "base": "Lucidina",
    "evolved": "Oneirina",
    "mega": "",
    "element": "Agua",
    "rarity": "UR",
    "role": "DPS fundo",
    "image": "images/Lucidina_5003.png",
    "imageEvolved": "images/Oneirina_5003_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Woozard",
    "base": "Woozard",
    "evolved": "Fleurizard",
    "mega": "",
    "element": "Terra",
    "rarity": "UR",
    "role": "Suporte/controle",
    "image": "images/Woozard_5014.png",
    "imageEvolved": "images/Fleurizard_5014_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Rotorlotor",
    "base": "Rotorlotor",
    "evolved": "",
    "mega": "",
    "element": "Eletrico",
    "rarity": "Epico",
    "role": "DPS fundo",
    "image": "images/Rotorlotor_4011.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Voltbolt",
    "base": "Voltbolt",
    "evolved": "",
    "mega": "",
    "element": "Eletrico",
    "rarity": "Epico",
    "role": "DPS frente/bruiser",
    "image": "images/Voltbolt_4015.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Platyputz",
    "base": "Platyputz",
    "evolved": "",
    "mega": "",
    "element": "Agua",
    "rarity": "Epico",
    "role": "Tank",
    "image": "images/Platyputz_4003.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Axollium",
    "base": "Axollium",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Epico",
    "role": "DPS frente/bruiser",
    "image": "images/Axollium_4016.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Incineraptor",
    "base": "Incineraptor",
    "evolved": "",
    "mega": "",
    "element": "Fogo",
    "rarity": "Epico",
    "role": "DPS fundo",
    "image": "images/Incineraptor_4007.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Wyvierno",
    "base": "Wyvierno",
    "evolved": "",
    "mega": "",
    "element": "Fogo",
    "rarity": "Epico",
    "role": "DPS fundo",
    "image": "images/Wyvierno_4001.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Cerverdant",
    "base": "Cerverdant",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Epico",
    "role": "Suporte/controle",
    "image": "images/Cerverdant_4012.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Thunderclawd",
    "base": "Thunderclawd",
    "evolved": "",
    "mega": "",
    "element": "Eletrico",
    "rarity": "Epico",
    "role": "DPS fundo",
    "image": "images/Thunderclawd_4005.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Snowkami",
    "base": "Snowkami",
    "evolved": "",
    "mega": "",
    "element": "Agua",
    "rarity": "Epico",
    "role": "DPS fundo",
    "image": "images/Snowkami_4004.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Vulcanid",
    "base": "Vulcanid",
    "evolved": "",
    "mega": "",
    "element": "Fogo",
    "rarity": "Epico",
    "role": "DPS frente/bruiser",
    "image": "images/Vulcanid_4013.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Bruiseberry",
    "base": "Bruiseberry",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Epico",
    "role": "DPS frente/bruiser",
    "image": "images/Bruiseberry_4009.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Squeezel",
    "base": "Squeezel",
    "evolved": "",
    "mega": "",
    "element": "Agua",
    "rarity": "Epico",
    "role": "DPS fundo",
    "image": "images/Squeezel_3202.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Meowdame",
    "base": "Meowdame",
    "evolved": "",
    "mega": "",
    "element": "Agua",
    "rarity": "Epico",
    "role": "Suporte/controle",
    "image": "images/Meowdame_4002.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Terrastudo",
    "base": "Terrastudo",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Epico",
    "role": "DPS frente/bruiser",
    "image": "images/Terrastudo_4006.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Maximito",
    "base": "Maximito",
    "evolved": "",
    "mega": "",
    "element": "Agua",
    "rarity": "Epico",
    "role": "Tank",
    "image": "images/Maximito_4008.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Lendanear",
    "base": "Lendanear",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Epico",
    "role": "Suporte/controle",
    "image": "images/Lendanear_4010.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Spinchilla",
    "base": "Spinchilla",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Raro",
    "role": "DPS fundo",
    "image": "images/Spinchilla_3204.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Herculeaf",
    "base": "Herculeaf",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Raro",
    "role": "DPS frente/bruiser",
    "image": "images/Herculeaf_4014.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Auktyke",
    "base": "Auktyke",
    "evolved": "",
    "mega": "",
    "element": "Agua",
    "rarity": "Raro",
    "role": "DPS frente/bruiser",
    "image": "images/Auktyke_3206.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Flouffant",
    "base": "Flouffant",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Raro",
    "role": "DPS fundo",
    "image": "images/Flouffant_3203.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Kilohopp",
    "base": "Kilohopp",
    "evolved": "",
    "mega": "",
    "element": "Eletrico",
    "rarity": "Raro",
    "role": "DPS fundo",
    "image": "images/Kilohopp_3207.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Graffitty",
    "base": "Graffitty",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "Raro",
    "role": "DPS fundo",
    "image": "images/Graffitty_3201.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Emboa",
    "base": "Emboa",
    "evolved": "",
    "mega": "",
    "element": "Fogo",
    "rarity": "Raro",
    "role": "DPS fundo",
    "image": "images/Emboa_3205.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "Sylphira",
    "base": "Sylphira",
    "evolved": "Abysphira",
    "mega": "",
    "element": "Agua",
    "rarity": "Mythic",
    "role": "DPS fundo",
    "image": "assets/s3_palmons/Palmon_full_5037.png",
    "imageEvolved": "assets/s3_palmons/Palmon_full_5037_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Gryndarr",
    "base": "Gryndarr",
    "evolved": "Gryphonarch",
    "mega": "",
    "element": "Eletrico",
    "rarity": "Mythic",
    "role": "DPS frente",
    "image": "assets/s3_palmons/Palmon_full_5039.png",
    "imageEvolved": "assets/s3_palmons/Palmon_full_5039_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Scorphelia",
    "base": "Scorphelia",
    "evolved": "Scorphelas",
    "mega": "",
    "element": "Terra",
    "rarity": "Mythic",
    "role": "DPS frente",
    "image": "assets/s3_palmons/Palmon_full_5040.png",
    "imageEvolved": "assets/s3_palmons/Palmon_full_5040_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Rapheni",
    "base": "Rapheni",
    "evolved": "Pyronyx",
    "mega": "",
    "element": "Fogo",
    "rarity": "Mythic",
    "role": "DPS fundo",
    "image": "assets/s3_palmons/Palmon_full_5041.png",
    "imageEvolved": "assets/s3_palmons/Palmon_full_5041_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Dialuna",
    "base": "Dialuna",
    "evolved": "Dialunova",
    "mega": "",
    "element": "Terra",
    "rarity": "Mythic",
    "role": "Deserto / economia",
    "image": "assets/s3_palmons/Palmon_full_5038.png",
    "imageEvolved": "assets/s3_palmons/Palmon_full_5038_evolve.png",
    "imageMega": ""
  },
  {
    "id": "Sunplume",
    "base": "Sunplume",
    "evolved": "",
    "mega": "",
    "element": "Fogo",
    "rarity": "UR",
    "role": "Passiva / conta",
    "image": "assets/s3_palmons/Palmon_full_5036.png",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "TidewaveWyrm",
    "base": "Tidewave Wyrm",
    "evolved": "",
    "mega": "",
    "element": "Agua",
    "rarity": "SP Mythic",
    "role": "DPS Agua",
    "category": "SP",
    "image": "",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "ThunderzenithWyrm",
    "base": "Thunderzenith Wyrm",
    "evolved": "",
    "mega": "",
    "element": "Eletrico",
    "rarity": "SP Mythic",
    "role": "DPS Eletrico",
    "category": "SP",
    "image": "",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "PhantasmalWyrm",
    "base": "Phantasmal Wyrm",
    "evolved": "",
    "mega": "",
    "element": "Terra",
    "rarity": "SP Mythic",
    "role": "DPS Terra",
    "category": "SP",
    "image": "",
    "imageEvolved": "",
    "imageMega": ""
  },
  {
    "id": "CrimsonblazeWyrm",
    "base": "Crimsonblaze Wyrm",
    "evolved": "",
    "mega": "",
    "element": "Fogo",
    "rarity": "SP Mythic",
    "role": "DPS Fogo",
    "category": "SP",
    "image": "",
    "imageEvolved": "",
    "imageMega": ""
  }
];

  const MEGA = {
    Barkplug: 'Voltfang', Ninjump: 'Shadowkaeru', Dolphriend: 'Leviadolph',
    Gnashley: 'Gnashswirl', Ghillant: 'Leafergarde', Surveilynx: 'Predalynx',
    Abuzzinian: 'Shadowvolt', Statchew: 'Pharohound', Magmolin: 'Inferdrake',
    Hoofrit: 'Solhorn', Mantleray: 'Mystiray', Revontulet: 'Scarvulpine'
  };
  const MEGA_ART = {
    Barkplug: 'assets/s3_palmons/superevolve_5001.png', Ninjump: 'assets/s3_palmons/superevolve_5002.png',
    Mantleray: 'assets/s3_palmons/superevolve_5004.png', Ghillant: 'assets/s3_palmons/superevolve_5005.png',
    Dolphriend: 'assets/s3_palmons/superevolve_5006.png', Abuzzinian: 'assets/s3_palmons/superevolve_5007.png',
    Statchew: 'assets/s3_palmons/superevolve_5008.png', Magmolin: 'assets/s3_palmons/superevolve_5011.png',
    Surveilynx: 'assets/s3_palmons/superevolve_5012.png', Hoofrit: 'assets/s3_palmons/superevolve_5017.png',
    Revontulet: 'assets/s3_palmons/superevolve_5021.png', Gnashley: 'assets/s3_palmons/superevolve_5027.png'
  };
  CATALOG.forEach(line => {
    if (!MEGA[line.base]) return;
    line.mega = MEGA[line.base];
    line.imageMega = MEGA_ART[line.base] || '';
  });
  const TIER_SETS = {
    'S+': 'Abysphira Cryovern Prismalith Pyregeist Shockmantis Thundermane'.split(' '),
    S: 'Bufonobi Chefeuillier Cinderpurr Dreadmaw Embergeist Glacewing Gryphonarch Kungfury Leafergarde Mammolith Mystiray Oleana Pyronyx Scorphelas Shadowkaeru Sorceray Spookaboo Sunplume Sylphira Thundertooth Zapantis'.split(' '),
    A: 'Adolphonis Anubeast Azurostrigoi Essaucier Finnabelle Flaries Ghillant Gnashfin Gnashswirl Gryndarr Hexkit Inferdrake Keraunosaur Kungpaw Leviadolph Lionarch Ninjump Obsidrake Oneirina Pharohound Plunderjaw Rapheni Rumbkey Scarvulpine Scorphelia Servolt Shadowvolt Solhorn Thornkeeper Voltfang Vulpyrean Wattweiler Wildfuror'.split(' '),
    B: 'Abuzzinian Ampereina Baboom Barkplug Blazeal Bunodroid Camouflynx Dialunova Dolphriend Escarffier Fingenue Fleurizard Fulgairy Gnashley Hoofrit Incineraptor Lucidina Magmolin Mantleray Pipistrigoi Predalynx Regalion Revontulet Rootwarden Silvaurus Snowkami Squeezel Statchew Wyvierno'.split(' '),
    C: 'Axollium Battereina Cerverdant Dialuna Emboa Kilohopp Lendanear Limudroid Maximito Meowdame Salamantis Surveilynx Terrastudo Thunderclawd Voltbolt Vulcanid Woozard'.split(' '),
    D: 'Auktyke Bruiseberry Flouffant Graffitty Herculeaf Platyputz Rotorlotor Spinchilla'.split(' ')
  };
  const TIER_BY_FORM = Object.fromEntries(Object.entries(TIER_SETS).flatMap(([tier, names]) => names.map(name => [name, tier])));
  const TIER_SCORE = { 'S+': 100, S: 86, A: 70, B: 52, C: 32, D: 14, SP: 90, '?': 24 };
  const FORM_STAGE = { Base: 'base', Evoluida: 'evolved', 'Super evoluida': 'mega', base: 'base', evolved: 'evolved', mega: 'mega' };

  function normalize(value) { return String(value || '').trim().toLowerCase().replace(/[^a-z0-9]/g, ''); }
  function lineFor(value) {
    if (!value) return null;
    const needle = typeof value === 'string' ? normalize(value) : normalize(value.lineId || value.baseName || value.name || value.id);
    return CATALOG.find(line => [line.id, line.base, line.evolved, line.mega].filter(Boolean).some(name => normalize(name) === needle)) || null;
  }
  function stageFor(card, line = lineFor(card)) {
    if (!line) return 'base';
    if (card?.stage && ['base', 'evolved', 'mega'].includes(card.stage)) return card.stage;
    if (card?.form && FORM_STAGE[card.form]) return FORM_STAGE[card.form];
    const source = `${card?.tierForm || ''} ${card?.image || ''} ${card?.name || ''}`.toLowerCase();
    if (line.mega && (source.includes('mega') || source.includes('superevolve') || normalize(card?.name) === normalize(line.mega))) return 'mega';
    if (line.evolved && (source.includes('evolve') || normalize(card?.name) === normalize(line.evolved))) return 'evolved';
    return 'base';
  }
  function stageLabel(stage) { return ({ base: 'Base', evolved: 'Evoluida', mega: 'Mega' })[stage] || 'Base'; }
  function formName(card, line = lineFor(card), stage = stageFor(card, line)) {
    if (!line) return card?.name || 'Palmon';
    return stage === 'mega' && line.mega ? line.mega : stage === 'evolved' && line.evolved ? line.evolved : line.base;
  }
  function formArt(card, line = lineFor(card), stage = stageFor(card, line)) {
    if (!line) return card?.image || '';
    return stage === 'mega' && line.imageMega ? line.imageMega : stage === 'evolved' && line.imageEvolved ? line.imageEvolved : line.image;
  }
  function availableStages(line) {
    if (!line) return ['base'];
    return ['base', ...(line.evolved ? ['evolved'] : []), ...(line.mega ? ['mega'] : [])];
  }
  function formTier(card, line = lineFor(card), stage = stageFor(card, line)) {
    if (line?.category === 'SP') return { tier: 'SP', source: 'Classe SP Mythic oficial', confidence: '10 estrelas; Ultimate em 6 e 10 estrelas; bonus do 4o skill de 30% (UR: 20%). Sem ordem publica entre os quatro.' };
    const name = formName(card, line, stage);
    return { tier: TIER_BY_FORM[name] || '?', source: TIER_BY_FORM[name] ? 'LoadoutGG Conquest 23/09/2026' : 'Sem rank externo', confidence: TIER_BY_FORM[name] ? 'Referencia por forma' : 'Nao publicado' };
  }
  function descriptor(card) {
    const line = lineFor(card);
    const stage = stageFor(card, line);
    const name = formName(card, line, stage);
    const tier = formTier(card, line, stage);
    return { line, stage, stageLabel: stageLabel(stage), name, image: formArt(card, line, stage), tier: tier.tier, tierSource: tier.source, tierConfidence: tier.confidence,
      evolutionPath: line ? [line.base, line.evolved, line.mega].filter(Boolean) : [card?.name].filter(Boolean) };
  }
  function withKnowledge(card) {
    const detail = descriptor(card);
    const line = detail.line;
    if (!line) return { ...card, stage: detail.stage };
    return { ...card, lineId: line.id, baseName: line.base, stage: detail.stage, form: stageLabel(detail.stage), name: detail.name, image: detail.image || card.image, element: line.element || card.element, rarity: line.rarity || card.rarity, role: line.role || card.role, tier: detail.tier, tierForm: `${detail.name} · ${detail.stageLabel}` };
  }
  function strategicScore(card) {
    const detail = descriptor(card);
    const tierScore = TIER_SCORE[detail.tier] ?? TIER_SCORE['?'];
    const stageScore = detail.stage === 'mega' ? 12 : detail.stage === 'evolved' ? 7 : 0;
    const stars = Math.min(25, Number(card?.stars) || 0);
    const level = Math.min(310, Number(card?.level) || 0);
    return tierScore + stageScore + stars / 25 * 8 + level / 310 * 8;
  }

  window.PALMON_KNOWLEDGE = {
    version: '2026-10-21',
    catalogVersion: 'XAPK 0.5.451',
    sources: [
      { name: 'LoadoutGG tier list', url: 'https://loadoutgg.com/palmon-survival/tier-list/', checked: '2026-10-21', use: 'Referencia competitiva por forma e estagio' },
      { name: 'LoadoutGG stat rankings', url: 'https://loadoutgg.com/palmon-survival/stat-rankings/', checked: '2026-10-21', use: 'Relacao Base, Evoluida e Mega' },
      { name: 'XAPK 0.5.451', use: 'Nomes, artes, linhas de evolucao e dados do cliente' }
    ],
    mechanics: {
      elements: 'Eletrico vence Agua; Agua vence Fogo; Fogo vence Terra; Terra vence Eletrico. Agua e Terra sao neutros entre si.',
      forms: 'Evolucao I abre em 5 estrelas; cada forma e avaliada separadamente. Mega so existe em linhas especificas.',
      progression: 'Concentre estrelas, evolucao e equipamento em um nucleo que voce manteria no time; nao divida recursos entre linhas substituiveis.',
      team: 'O advisor prioriza um nucleo do mesmo elemento quando ele existe no elenco, encaixando frente e fundo antes de comparar poder bruto.',
      mounts: 'Montarias e tracos entram depois do nucleo, estrelas e evolucao; Bunny Runny e uma excecao de valor geral.',
      jobs: 'Combatentes ficam no squad. Palmons de economia e especialistas ficam na base sem competir por recursos do time.'
    },
    catalog: CATALOG,
    tierSets: TIER_SETS,
    tierScore: TIER_SCORE,
    lineFor, stageFor, stageLabel, formName, formArt, availableStages, formTier, descriptor, withKnowledge, strategicScore
  };
})();
