; Evos+moves data structure:
; - Evolution methods:
;    * db EVOLVE_LEVEL, level, species
;    * db EVOLVE_ITEM, used item, min level (1), species
;    * db EVOLVE_TRADE, min level (1), species
; - db 0 ; no more evolutions
; - Learnset (in increasing level order):
;    * learnset_move level, move
; - db 0 ; no more level-up moves

EvosMovesPointerTable:
	table_width 2
	dw RhydonEvosMoves
	dw KangaskhanEvosMoves
	dw NidoranMEvosMoves
	dw ClefairyEvosMoves
	dw SpearowEvosMoves
	dw VoltorbEvosMoves
	dw NidokingEvosMoves
	dw SlowbroEvosMoves
	dw IvysaurEvosMoves
	dw ExeggutorEvosMoves
	dw LickitungEvosMoves
	dw ExeggcuteEvosMoves
	dw GrimerEvosMoves
	dw GengarEvosMoves
	dw NidoranFEvosMoves
	dw NidoqueenEvosMoves
	dw CuboneEvosMoves
	dw RhyhornEvosMoves
	dw LaprasEvosMoves
	dw ArcanineEvosMoves
	dw MewEvosMoves
	dw GyaradosEvosMoves
	dw ShellderEvosMoves
	dw TentacoolEvosMoves
	dw GastlyEvosMoves
	dw ScytherEvosMoves
	dw StaryuEvosMoves
	dw BlastoiseEvosMoves
	dw PinsirEvosMoves
	dw TangelaEvosMoves
	dw MissingNo1FEvosMoves
	dw MissingNo20EvosMoves
	dw GrowlitheEvosMoves
	dw OnixEvosMoves
	dw FearowEvosMoves
	dw PidgeyEvosMoves
	dw SlowpokeEvosMoves
	dw KadabraEvosMoves
	dw GravelerEvosMoves
	dw ChanseyEvosMoves
	dw MachokeEvosMoves
	dw MrMimeEvosMoves
	dw HitmonleeEvosMoves
	dw HitmonchanEvosMoves
	dw ArbokEvosMoves
	dw ParasectEvosMoves
	dw PsyduckEvosMoves
	dw DrowzeeEvosMoves
	dw GolemEvosMoves
	dw MissingNo32EvosMoves
	dw MagmarEvosMoves
	dw MissingNo34EvosMoves
	dw ElectabuzzEvosMoves
	dw MagnetonEvosMoves
	dw KoffingEvosMoves
	dw MissingNo38EvosMoves
	dw MankeyEvosMoves
	dw SeelEvosMoves
	dw DiglettEvosMoves
	dw TaurosEvosMoves
	dw MissingNo3DEvosMoves
	dw MissingNo3EEvosMoves
	dw MissingNo3FEvosMoves
	dw FarfetchdEvosMoves
	dw VenonatEvosMoves
	dw DragoniteEvosMoves
	dw MissingNo43EvosMoves
	dw MissingNo44EvosMoves
	dw MissingNo45EvosMoves
	dw DoduoEvosMoves
	dw PoliwagEvosMoves
	dw JynxEvosMoves
	dw MoltresEvosMoves
	dw ArticunoEvosMoves
	dw ZapdosEvosMoves
	dw DittoEvosMoves
	dw MeowthEvosMoves
	dw KrabbyEvosMoves
	dw MissingNo4FEvosMoves
	dw MissingNo50EvosMoves
	dw MissingNo51EvosMoves
	dw VulpixEvosMoves
	dw NinetalesEvosMoves
	dw PikachuEvosMoves
	dw RaichuEvosMoves
	dw MissingNo56EvosMoves
	dw MissingNo57EvosMoves
	dw DratiniEvosMoves
	dw DragonairEvosMoves
	dw KabutoEvosMoves
	dw KabutopsEvosMoves
	dw HorseaEvosMoves
	dw SeadraEvosMoves
	dw MissingNo5EEvosMoves
	dw MissingNo5FEvosMoves
	dw SandshrewEvosMoves
	dw SandslashEvosMoves
	dw OmanyteEvosMoves
	dw OmastarEvosMoves
	dw JigglypuffEvosMoves
	dw WigglytuffEvosMoves
	dw EeveeEvosMoves
	dw FlareonEvosMoves
	dw JolteonEvosMoves
	dw VaporeonEvosMoves
	dw MachopEvosMoves
	dw ZubatEvosMoves
	dw EkansEvosMoves
	dw ParasEvosMoves
	dw PoliwhirlEvosMoves
	dw PoliwrathEvosMoves
	dw WeedleEvosMoves
	dw KakunaEvosMoves
	dw BeedrillEvosMoves
	dw MissingNo73EvosMoves
	dw DodrioEvosMoves
	dw PrimeapeEvosMoves
	dw DugtrioEvosMoves
	dw VenomothEvosMoves
	dw DewgongEvosMoves
	dw MissingNo79EvosMoves
	dw MissingNo7AEvosMoves
	dw CaterpieEvosMoves
	dw MetapodEvosMoves
	dw ButterfreeEvosMoves
	dw MachampEvosMoves
	dw MissingNo7FEvosMoves
	dw GolduckEvosMoves
	dw HypnoEvosMoves
	dw GolbatEvosMoves
	dw MewtwoEvosMoves
	dw SnorlaxEvosMoves
	dw MagikarpEvosMoves
	dw MissingNo86EvosMoves
	dw MissingNo87EvosMoves
	dw MukEvosMoves
	dw MissingNo8AEvosMoves
	dw KinglerEvosMoves
	dw CloysterEvosMoves
	dw MissingNo8CEvosMoves
	dw ElectrodeEvosMoves
	dw ClefableEvosMoves
	dw WeezingEvosMoves
	dw PersianEvosMoves
	dw MarowakEvosMoves
	dw MissingNo92EvosMoves
	dw HaunterEvosMoves
	dw AbraEvosMoves
	dw AlakazamEvosMoves
	dw PidgeottoEvosMoves
	dw PidgeotEvosMoves
	dw StarmieEvosMoves
	dw BulbasaurEvosMoves
	dw VenusaurEvosMoves
	dw TentacruelEvosMoves
	dw MissingNo9CEvosMoves
	dw GoldeenEvosMoves
	dw SeakingEvosMoves
	dw MissingNo9FEvosMoves
	dw MissingNoA0EvosMoves
	dw MissingNoA1EvosMoves
	dw MissingNoA2EvosMoves
	dw PonytaEvosMoves
	dw RapidashEvosMoves
	dw RattataEvosMoves
	dw RaticateEvosMoves
	dw NidorinoEvosMoves
	dw NidorinaEvosMoves
	dw GeodudeEvosMoves
	dw PorygonEvosMoves
	dw AerodactylEvosMoves
	dw MissingNoACEvosMoves
	dw MagnemiteEvosMoves
	dw MissingNoAEEvosMoves
	dw MissingNoAFEvosMoves
	dw CharmanderEvosMoves
	dw SquirtleEvosMoves
	dw CharmeleonEvosMoves
	dw WartortleEvosMoves
	dw CharizardEvosMoves
	dw MissingNoB5EvosMoves
	dw FossilKabutopsEvosMoves
	dw FossilAerodactylEvosMoves
	dw MonGhostEvosMoves
	dw OddishEvosMoves
	dw GloomEvosMoves
	dw VileplumeEvosMoves
	dw BellsproutEvosMoves
	dw WeepinbellEvosMoves
	dw VictreebelEvosMoves
	assert_table_length NUM_POKEMON_INDEXES

RhydonEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 30, STOMP
	learnset_move 35, TAIL_WHIP
	learnset_move 40, FURY_ATTACK
	learnset_move 48, HORN_DRILL
	learnset_move 55, LEER
	learnset_move 64, TAKE_DOWN
	db 0

KangaskhanEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 26, BITE
	learnset_move 31, TAIL_WHIP
	learnset_move 36, MEGA_PUNCH
	learnset_move 41, LEER
	learnset_move 46, DIZZY_PUNCH
	db 0

NidoranMEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 16, NIDORINO
	db 0
; Learnset
	learnset_move 8, HORN_ATTACK
	learnset_move 14, POISON_STING
	learnset_move 21, FOCUS_ENERGY
	learnset_move 29, FURY_ATTACK
	learnset_move 36, HORN_DRILL
	learnset_move 43, DOUBLE_KICK
	db 0

ClefairyEvosMoves:
; Evolutions
	db EVOLVE_ITEM, MOON_STONE, 1, CLEFABLE
	db 0
; Learnset
	learnset_move 13, SING
	learnset_move 18, DOUBLESLAP
	learnset_move 24, MINIMIZE
	learnset_move 31, METRONOME
	learnset_move 39, DEFENSE_CURL
	learnset_move 48, LIGHT_SCREEN
	db 0

SpearowEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 20, FEAROW
	db 0
; Learnset
	learnset_move 9, LEER
	learnset_move 15, FURY_ATTACK
	learnset_move 22, MIRROR_MOVE
	learnset_move 29, DRILL_PECK
	learnset_move 36, AGILITY
	db 0

VoltorbEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 30, ELECTRODE
	db 0
; Learnset
	learnset_move 17, SONICBOOM
	learnset_move 22, SELFDESTRUCT
	learnset_move 29, LIGHT_SCREEN
	learnset_move 36, SWIFT
	learnset_move 43, EXPLOSION
	db 0

NidokingEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 8, HORN_ATTACK
	learnset_move 14, POISON_STING
	learnset_move 23, THRASH
	db 0

SlowbroEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 18, DISABLE
	learnset_move 22, HEADBUTT
	learnset_move 27, GROWL
	learnset_move 33, WATER_GUN
	learnset_move 37, WITHDRAW
	learnset_move 44, AMNESIA
	learnset_move 55, PSYCHIC_M
	db 0

IvysaurEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 32, VENUSAUR
	db 0
; Learnset
	learnset_move 7, LEECH_SEED
	learnset_move 13, VINE_WHIP
	learnset_move 22, POISONPOWDER
	learnset_move 30, RAZOR_LEAF
	learnset_move 38, GROWTH
	learnset_move 46, SLEEP_POWDER
	learnset_move 54, SOLARBEAM
	db 0

ExeggutorEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 28, STOMP
	db 0

LickitungEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 7, STOMP
	learnset_move 15, DISABLE
	learnset_move 23, DEFENSE_CURL
	learnset_move 31, SLAM
	learnset_move 39, SCREECH
	db 0

ExeggcuteEvosMoves:
; Evolutions
	db EVOLVE_ITEM, LEAF_STONE, 1, EXEGGUTOR
	db 0
; Learnset
	learnset_move 25, REFLECT
	learnset_move 28, LEECH_SEED
	learnset_move 32, STUN_SPORE
	learnset_move 37, POISONPOWDER
	learnset_move 42, SOLARBEAM
	learnset_move 48, SLEEP_POWDER
	db 0

GrimerEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 38, MUK
	db 0
; Learnset
	learnset_move 30, POISON_GAS
	learnset_move 33, MINIMIZE
	learnset_move 37, SLUDGE
	learnset_move 42, HARDEN
	learnset_move 48, SCREECH
	learnset_move 55, ACID_ARMOR
	db 0

GengarEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 29, HYPNOSIS
	learnset_move 38, DREAM_EATER
	db 0

NidoranFEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 16, NIDORINA
	db 0
; Learnset
	learnset_move 8, SCRATCH
	learnset_move 14, POISON_STING
	learnset_move 21, TAIL_WHIP
	learnset_move 29, BITE
	learnset_move 36, FURY_SWIPES
	learnset_move 43, DOUBLE_KICK
	db 0

NidoqueenEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 8, SCRATCH
	learnset_move 14, POISON_STING
	learnset_move 23, BODY_SLAM
	db 0

CuboneEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 28, MAROWAK
	db 0
; Learnset
	learnset_move 25, LEER
	learnset_move 31, FOCUS_ENERGY
	learnset_move 38, THRASH
	learnset_move 43, BONEMERANG
	learnset_move 46, RAGE
	db 0

RhyhornEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 42, RHYDON
	db 0
; Learnset
	learnset_move 30, STOMP
	learnset_move 35, TAIL_WHIP
	learnset_move 40, FURY_ATTACK
	learnset_move 45, HORN_DRILL
	learnset_move 50, LEER
	learnset_move 55, TAKE_DOWN
	db 0

LaprasEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 16, SING
	learnset_move 20, MIST
	learnset_move 25, BODY_SLAM
	learnset_move 31, CONFUSE_RAY
	learnset_move 38, ICE_BEAM
	learnset_move 46, HYDRO_PUMP
	db 0

ArcanineEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MewEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 10, TRANSFORM
	learnset_move 20, MEGA_PUNCH
	learnset_move 30, METRONOME
	learnset_move 40, PSYCHIC_M
	db 0

GyaradosEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 20, BITE
	learnset_move 25, DRAGON_RAGE
	learnset_move 32, LEER
	learnset_move 41, HYDRO_PUMP
	learnset_move 52, HYPER_BEAM
	db 0

ShellderEvosMoves:
; Evolutions
	db EVOLVE_ITEM, WATER_STONE, 1, CLOYSTER
	db 0
; Learnset
	learnset_move 18, SUPERSONIC
	learnset_move 23, CLAMP
	learnset_move 30, AURORA_BEAM
	learnset_move 39, LEER
	learnset_move 50, ICE_BEAM
	db 0

TentacoolEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 30, TENTACRUEL
	db 0
; Learnset
	learnset_move 7, SUPERSONIC
	learnset_move 13, WRAP
	learnset_move 18, POISON_STING
	learnset_move 22, WATER_GUN
	learnset_move 27, CONSTRICT
	learnset_move 33, BARRIER
	learnset_move 40, SCREECH
	learnset_move 48, HYDRO_PUMP
	db 0

GastlyEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 25, HAUNTER
	db 0
; Learnset
	learnset_move 27, HYPNOSIS
	learnset_move 35, DREAM_EATER
	db 0

ScytherEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 17, LEER
	learnset_move 20, FOCUS_ENERGY
	learnset_move 24, DOUBLE_TEAM
	learnset_move 29, SLASH
	learnset_move 35, SWORDS_DANCE
	learnset_move 42, AGILITY
	db 0

StaryuEvosMoves:
; Evolutions
	db EVOLVE_ITEM, WATER_STONE, 1, STARMIE
	db 0
; Learnset
	learnset_move 17, WATER_GUN
	learnset_move 22, HARDEN
	learnset_move 27, RECOVER
	learnset_move 32, SWIFT
	learnset_move 37, MINIMIZE
	learnset_move 42, LIGHT_SCREEN
	learnset_move 47, HYDRO_PUMP
	db 0

BlastoiseEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 8, BUBBLE
	learnset_move 15, WATER_GUN
	learnset_move 24, BITE
	learnset_move 31, WITHDRAW
	learnset_move 42, SKULL_BASH
	learnset_move 52, HYDRO_PUMP
	db 0

PinsirEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 25, SEISMIC_TOSS
	learnset_move 30, GUILLOTINE
	learnset_move 36, FOCUS_ENERGY
	learnset_move 43, HARDEN
	learnset_move 49, SLASH
	learnset_move 54, SWORDS_DANCE
	db 0

TangelaEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 29, ABSORB
	learnset_move 32, POISONPOWDER
	learnset_move 36, STUN_SPORE
	learnset_move 39, SLEEP_POWDER
	learnset_move 45, SLAM
	learnset_move 49, GROWTH
	db 0

MissingNo1FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo20EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

GrowlitheEvosMoves:
; Evolutions
	db EVOLVE_ITEM, FIRE_STONE, 1, ARCANINE
	db 0
; Learnset
	learnset_move 18, EMBER
	learnset_move 23, LEER
	learnset_move 30, TAKE_DOWN
	learnset_move 39, AGILITY
	learnset_move 50, FLAMETHROWER
	db 0

OnixEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 15, BIND
	learnset_move 19, ROCK_THROW
	learnset_move 25, RAGE
	learnset_move 33, SLAM
	learnset_move 43, HARDEN
	db 0

FearowEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 9, LEER
	learnset_move 15, FURY_ATTACK
	learnset_move 25, MIRROR_MOVE
	learnset_move 34, DRILL_PECK
	learnset_move 43, AGILITY
	db 0

PidgeyEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 18, PIDGEOTTO
	db 0
; Learnset
	learnset_move 5, SAND_ATTACK
	learnset_move 12, QUICK_ATTACK
	learnset_move 19, WHIRLWIND
	learnset_move 28, WING_ATTACK
	learnset_move 36, AGILITY
	learnset_move 44, MIRROR_MOVE
	db 0

SlowpokeEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 37, SLOWBRO
	db 0
; Learnset
	learnset_move 18, DISABLE
	learnset_move 22, HEADBUTT
	learnset_move 27, GROWL
	learnset_move 33, WATER_GUN
	learnset_move 40, AMNESIA
	learnset_move 48, PSYCHIC_M
	db 0

KadabraEvosMoves:
; Evolutions
	db EVOLVE_TRADE, 1, ALAKAZAM
	db 0
; Learnset
	learnset_move 16, CONFUSION
	learnset_move 20, DISABLE
	learnset_move 27, PSYBEAM
	learnset_move 31, RECOVER
	learnset_move 38, PSYCHIC_M
	learnset_move 42, REFLECT
	db 0

GravelerEvosMoves:
; Evolutions
	db EVOLVE_TRADE, 1, GOLEM
	db 0
; Learnset
	learnset_move 11, DEFENSE_CURL
	learnset_move 16, ROCK_THROW
	learnset_move 21, SELFDESTRUCT
	learnset_move 29, HARDEN
	learnset_move 36, EARTHQUAKE
	learnset_move 43, EXPLOSION
	db 0

ChanseyEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 24, SING
	learnset_move 30, GROWL
	learnset_move 38, MINIMIZE
	learnset_move 44, DEFENSE_CURL
	learnset_move 48, LIGHT_SCREEN
	learnset_move 54, DOUBLE_EDGE
	db 0

MachokeEvosMoves:
; Evolutions
	db EVOLVE_TRADE, 1, MACHAMP
	db 0
; Learnset
	learnset_move 20, LOW_KICK
	learnset_move 25, LEER
	learnset_move 36, FOCUS_ENERGY
	learnset_move 44, SEISMIC_TOSS
	learnset_move 52, SUBMISSION
	db 0

MrMimeEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 15, CONFUSION
	learnset_move 23, LIGHT_SCREEN
	learnset_move 31, DOUBLESLAP
	learnset_move 39, MEDITATE
	learnset_move 47, SUBSTITUTE
	db 0

HitmonleeEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 33, ROLLING_KICK
	learnset_move 38, JUMP_KICK
	learnset_move 43, FOCUS_ENERGY
	learnset_move 48, HI_JUMP_KICK
	learnset_move 53, MEGA_KICK
	db 0

HitmonchanEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 33, FIRE_PUNCH
	learnset_move 38, ICE_PUNCH
	learnset_move 43, THUNDERPUNCH
	learnset_move 48, MEGA_PUNCH
	learnset_move 53, COUNTER
	db 0

ArbokEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 10, POISON_STING
	learnset_move 17, BITE
	learnset_move 27, GLARE
	learnset_move 36, SCREECH
	learnset_move 47, ACID
	db 0

ParasectEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 13, STUN_SPORE
	learnset_move 20, LEECH_LIFE
	learnset_move 30, SPORE
	learnset_move 39, SLASH
	learnset_move 48, GROWTH
	db 0

PsyduckEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 33, GOLDUCK
	db 0
; Learnset
	learnset_move 28, TAIL_WHIP
	learnset_move 31, DISABLE
	learnset_move 36, CONFUSION
	learnset_move 43, FURY_SWIPES
	learnset_move 52, HYDRO_PUMP
	db 0

DrowzeeEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 26, HYPNO
	db 0
; Learnset
	learnset_move 12, DISABLE
	learnset_move 17, CONFUSION
	learnset_move 24, HEADBUTT
	learnset_move 29, POISON_GAS
	learnset_move 32, PSYCHIC_M
	learnset_move 37, MEDITATE
	db 0

GolemEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 11, DEFENSE_CURL
	learnset_move 16, ROCK_THROW
	learnset_move 21, SELFDESTRUCT
	learnset_move 29, HARDEN
	learnset_move 36, EARTHQUAKE
	learnset_move 43, EXPLOSION
	db 0

MissingNo32EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MagmarEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 36, LEER
	learnset_move 39, CONFUSE_RAY
	learnset_move 43, FIRE_PUNCH
	learnset_move 48, SMOKESCREEN
	learnset_move 52, SMOG
	learnset_move 55, FLAMETHROWER
	db 0

MissingNo34EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

ElectabuzzEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 34, THUNDERSHOCK
	learnset_move 37, SCREECH
	learnset_move 42, THUNDERPUNCH
	learnset_move 49, LIGHT_SCREEN
	learnset_move 54, THUNDER
	db 0

MagnetonEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 21, SONICBOOM
	learnset_move 25, THUNDERSHOCK
	learnset_move 29, SUPERSONIC
	learnset_move 38, THUNDER_WAVE
	learnset_move 46, SWIFT
	learnset_move 54, SCREECH
	db 0

KoffingEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 35, WEEZING
	db 0
; Learnset
	learnset_move 32, SLUDGE
	learnset_move 37, SMOKESCREEN
	learnset_move 40, SELFDESTRUCT
	learnset_move 45, HAZE
	learnset_move 48, EXPLOSION
	db 0

MissingNo38EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MankeyEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 28, PRIMEAPE
	db 0
; Learnset
	learnset_move 15, KARATE_CHOP
	learnset_move 21, FURY_SWIPES
	learnset_move 27, FOCUS_ENERGY
	learnset_move 33, SEISMIC_TOSS
	learnset_move 39, THRASH
	db 0

SeelEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 34, DEWGONG
	db 0
; Learnset
	learnset_move 30, GROWL
	learnset_move 35, AURORA_BEAM
	learnset_move 40, REST
	learnset_move 45, TAKE_DOWN
	learnset_move 50, ICE_BEAM
	db 0

DiglettEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 26, DUGTRIO
	db 0
; Learnset
	learnset_move 15, GROWL
	learnset_move 19, DIG
	learnset_move 24, SAND_ATTACK
	learnset_move 31, SLASH
	learnset_move 40, EARTHQUAKE
	db 0

TaurosEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 21, STOMP
	learnset_move 28, TAIL_WHIP
	learnset_move 35, LEER
	learnset_move 44, RAGE
	learnset_move 51, TAKE_DOWN
	db 0

MissingNo3DEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo3EEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo3FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

FarfetchdEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 7, LEER
	learnset_move 15, FURY_ATTACK
	learnset_move 23, SWORDS_DANCE
	learnset_move 31, AGILITY
	learnset_move 39, SLASH
	db 0

VenonatEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 31, VENOMOTH
	db 0
; Learnset
	learnset_move 24, POISONPOWDER
	learnset_move 27, LEECH_LIFE
	learnset_move 30, STUN_SPORE
	learnset_move 35, PSYBEAM
	learnset_move 38, SLEEP_POWDER
	learnset_move 43, PSYCHIC_M
	db 0

DragoniteEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 10, THUNDER_WAVE
	learnset_move 20, AGILITY
	learnset_move 35, SLAM
	learnset_move 45, DRAGON_RAGE
	learnset_move 60, HYPER_BEAM
	db 0

MissingNo43EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo44EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo45EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

DoduoEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 31, DODRIO
	db 0
; Learnset
	learnset_move 20, GROWL
	learnset_move 24, FURY_ATTACK
	learnset_move 30, DRILL_PECK
	learnset_move 36, RAGE
	learnset_move 40, TRI_ATTACK
	learnset_move 44, AGILITY
	db 0

PoliwagEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 25, POLIWHIRL
	db 0
; Learnset
	learnset_move 16, HYPNOSIS
	learnset_move 19, WATER_GUN
	learnset_move 25, DOUBLESLAP
	learnset_move 31, BODY_SLAM
	learnset_move 38, AMNESIA
	learnset_move 45, HYDRO_PUMP
	db 0

JynxEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 18, LICK
	learnset_move 23, DOUBLESLAP
	learnset_move 31, ICE_PUNCH
	learnset_move 39, BODY_SLAM
	learnset_move 47, THRASH
	learnset_move 58, BLIZZARD
	db 0

MoltresEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 51, LEER
	learnset_move 55, AGILITY
	learnset_move 60, SKY_ATTACK
	db 0

ArticunoEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 51, BLIZZARD
	learnset_move 55, AGILITY
	learnset_move 60, MIST
	db 0

ZapdosEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 51, THUNDER
	learnset_move 55, AGILITY
	learnset_move 60, LIGHT_SCREEN
	db 0

DittoEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MeowthEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 28, PERSIAN
	db 0
; Learnset
	learnset_move 12, BITE
	learnset_move 17, PAY_DAY
	learnset_move 24, SCREECH
	learnset_move 33, FURY_SWIPES
	learnset_move 44, SLASH
	db 0

KrabbyEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 28, KINGLER
	db 0
; Learnset
	learnset_move 20, VICEGRIP
	learnset_move 25, GUILLOTINE
	learnset_move 30, STOMP
	learnset_move 35, CRABHAMMER
	learnset_move 40, HARDEN
	db 0

MissingNo4FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo50EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo51EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

VulpixEvosMoves:
; Evolutions
	db EVOLVE_ITEM, FIRE_STONE, 1, NINETALES
	db 0
; Learnset
	learnset_move 16, QUICK_ATTACK
	learnset_move 21, ROAR
	learnset_move 28, CONFUSE_RAY
	learnset_move 35, FLAMETHROWER
	learnset_move 42, FIRE_SPIN
	db 0

NinetalesEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

PikachuEvosMoves:
; Evolutions
	db EVOLVE_ITEM, THUNDER_STONE, 1, RAICHU
	db 0
; Learnset
	learnset_move 9, THUNDER_WAVE
	learnset_move 16, QUICK_ATTACK
	learnset_move 26, SWIFT
	learnset_move 33, AGILITY
	learnset_move 43, THUNDER
	db 0

RaichuEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo56EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo57EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

DratiniEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 30, DRAGONAIR
	db 0
; Learnset
	learnset_move 10, THUNDER_WAVE
	learnset_move 20, AGILITY
	learnset_move 30, SLAM
	learnset_move 40, DRAGON_RAGE
	learnset_move 50, HYPER_BEAM
	db 0

DragonairEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 55, DRAGONITE
	db 0
; Learnset
	learnset_move 10, THUNDER_WAVE
	learnset_move 20, AGILITY
	learnset_move 35, SLAM
	learnset_move 45, DRAGON_RAGE
	learnset_move 55, HYPER_BEAM
	db 0

KabutoEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 40, KABUTOPS
	db 0
; Learnset
	learnset_move 34, ABSORB
	learnset_move 39, SLASH
	learnset_move 44, LEER
	learnset_move 49, HYDRO_PUMP
	db 0

KabutopsEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 34, ABSORB
	learnset_move 39, SLASH
	learnset_move 46, LEER
	learnset_move 53, HYDRO_PUMP
	db 0

HorseaEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 32, SEADRA
	db 0
; Learnset
	learnset_move 19, SMOKESCREEN
	learnset_move 24, LEER
	learnset_move 30, WATER_GUN
	learnset_move 37, AGILITY
	learnset_move 45, HYDRO_PUMP
	db 0

SeadraEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 19, SMOKESCREEN
	learnset_move 24, LEER
	learnset_move 30, WATER_GUN
	learnset_move 41, AGILITY
	learnset_move 52, HYDRO_PUMP
	db 0

MissingNo5EEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo5FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

SandshrewEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 22, SANDSLASH
	db 0
; Learnset
	learnset_move 10, SAND_ATTACK
	learnset_move 17, SLASH
	learnset_move 24, POISON_STING
	learnset_move 31, SWIFT
	learnset_move 38, FURY_SWIPES
	db 0

SandslashEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 10, SAND_ATTACK
	learnset_move 17, SLASH
	learnset_move 27, POISON_STING
	learnset_move 36, SWIFT
	learnset_move 47, FURY_SWIPES
	db 0

OmanyteEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 40, OMASTAR
	db 0
; Learnset
	learnset_move 34, HORN_ATTACK
	learnset_move 39, LEER
	learnset_move 46, SPIKE_CANNON
	learnset_move 53, HYDRO_PUMP
	db 0

OmastarEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 34, HORN_ATTACK
	learnset_move 39, LEER
	learnset_move 44, SPIKE_CANNON
	learnset_move 49, HYDRO_PUMP
	db 0

JigglypuffEvosMoves:
; Evolutions
	db EVOLVE_ITEM, MOON_STONE, 1, WIGGLYTUFF
	db 0
; Learnset
	learnset_move 9, POUND
	learnset_move 14, DISABLE
	learnset_move 19, DEFENSE_CURL
	learnset_move 24, DOUBLESLAP
	learnset_move 29, REST
	learnset_move 34, BODY_SLAM
	learnset_move 39, DOUBLE_EDGE
	db 0

WigglytuffEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

EeveeEvosMoves:
; Evolutions
	db EVOLVE_ITEM, FIRE_STONE, 1, FLAREON
	db EVOLVE_ITEM, THUNDER_STONE, 1, JOLTEON
	db EVOLVE_ITEM, WATER_STONE, 1, VAPOREON
	db 0
; Learnset
	learnset_move 27, QUICK_ATTACK
	learnset_move 31, TAIL_WHIP
	learnset_move 37, BITE
	learnset_move 45, TAKE_DOWN
	db 0

FlareonEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 27, QUICK_ATTACK
	learnset_move 31, EMBER
	learnset_move 37, TAIL_WHIP
	learnset_move 40, BITE
	learnset_move 42, LEER
	learnset_move 44, FIRE_SPIN
	learnset_move 48, RAGE
	learnset_move 54, FLAMETHROWER
	db 0

JolteonEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 27, QUICK_ATTACK
	learnset_move 31, THUNDERSHOCK
	learnset_move 37, TAIL_WHIP
	learnset_move 40, THUNDER_WAVE
	learnset_move 42, DOUBLE_KICK
	learnset_move 44, AGILITY
	learnset_move 48, PIN_MISSILE
	learnset_move 54, THUNDER
	db 0

VaporeonEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 27, QUICK_ATTACK
	learnset_move 31, WATER_GUN
	learnset_move 37, TAIL_WHIP
	learnset_move 40, BITE
	learnset_move 42, ACID_ARMOR
	learnset_move 44, HAZE
	learnset_move 48, MIST
	learnset_move 54, HYDRO_PUMP
	db 0

MachopEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 28, MACHOKE
	db 0
; Learnset
	learnset_move 20, LOW_KICK
	learnset_move 25, LEER
	learnset_move 32, FOCUS_ENERGY
	learnset_move 39, SEISMIC_TOSS
	learnset_move 46, SUBMISSION
	db 0

ZubatEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 22, GOLBAT
	db 0
; Learnset
	learnset_move 10, SUPERSONIC
	learnset_move 15, BITE
	learnset_move 21, CONFUSE_RAY
	learnset_move 28, WING_ATTACK
	learnset_move 36, HAZE
	db 0

EkansEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 22, ARBOK
	db 0
; Learnset
	learnset_move 10, POISON_STING
	learnset_move 17, BITE
	learnset_move 24, GLARE
	learnset_move 31, SCREECH
	learnset_move 38, ACID
	db 0

ParasEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 24, PARASECT
	db 0
; Learnset
	learnset_move 13, STUN_SPORE
	learnset_move 20, LEECH_LIFE
	learnset_move 27, SPORE
	learnset_move 34, SLASH
	learnset_move 41, GROWTH
	db 0

PoliwhirlEvosMoves:
; Evolutions
	db EVOLVE_ITEM, WATER_STONE, 1, POLIWRATH
	db 0
; Learnset
	learnset_move 16, HYPNOSIS
	learnset_move 19, WATER_GUN
	learnset_move 26, DOUBLESLAP
	learnset_move 33, BODY_SLAM
	learnset_move 41, AMNESIA
	learnset_move 49, HYDRO_PUMP
	db 0

PoliwrathEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 16, HYPNOSIS
	learnset_move 19, WATER_GUN
	db 0

WeedleEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 7, KAKUNA
	db 0
; Learnset
	db 0

KakunaEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 10, BEEDRILL
	db 0
; Learnset
	db 0

BeedrillEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 12, FURY_ATTACK
	learnset_move 16, FOCUS_ENERGY
	learnset_move 20, TWINEEDLE
	learnset_move 25, RAGE
	learnset_move 30, PIN_MISSILE
	learnset_move 35, AGILITY
	db 0

MissingNo73EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

DodrioEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 20, GROWL
	learnset_move 24, FURY_ATTACK
	learnset_move 30, DRILL_PECK
	learnset_move 39, RAGE
	learnset_move 45, TRI_ATTACK
	learnset_move 51, AGILITY
	db 0

PrimeapeEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 15, KARATE_CHOP
	learnset_move 21, FURY_SWIPES
	learnset_move 27, FOCUS_ENERGY
	learnset_move 37, SEISMIC_TOSS
	learnset_move 46, THRASH
	db 0

DugtrioEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 15, GROWL
	learnset_move 19, DIG
	learnset_move 24, SAND_ATTACK
	learnset_move 35, SLASH
	learnset_move 47, EARTHQUAKE
	db 0

VenomothEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 24, POISONPOWDER
	learnset_move 27, LEECH_LIFE
	learnset_move 30, STUN_SPORE
	learnset_move 38, PSYBEAM
	learnset_move 43, SLEEP_POWDER
	learnset_move 50, PSYCHIC_M
	db 0

DewgongEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 30, GROWL
	learnset_move 35, AURORA_BEAM
	learnset_move 44, REST
	learnset_move 50, TAKE_DOWN
	learnset_move 56, ICE_BEAM
	db 0

MissingNo79EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo7AEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

CaterpieEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 7, METAPOD
	db 0
; Learnset
	db 0

MetapodEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 10, BUTTERFREE
	db 0
; Learnset
	db 0

ButterfreeEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 12, CONFUSION
	learnset_move 15, POISONPOWDER
	learnset_move 16, STUN_SPORE
	learnset_move 17, SLEEP_POWDER
	learnset_move 21, SUPERSONIC
	learnset_move 26, WHIRLWIND
	learnset_move 32, PSYBEAM
	db 0

MachampEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 20, LOW_KICK
	learnset_move 25, LEER
	learnset_move 36, FOCUS_ENERGY
	learnset_move 44, SEISMIC_TOSS
	learnset_move 52, SUBMISSION
	db 0

MissingNo7FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

GolduckEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 28, TAIL_WHIP
	learnset_move 31, DISABLE
	learnset_move 39, CONFUSION
	learnset_move 48, FURY_SWIPES
	learnset_move 59, HYDRO_PUMP
	db 0

HypnoEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 12, DISABLE
	learnset_move 17, CONFUSION
	learnset_move 24, HEADBUTT
	learnset_move 33, POISON_GAS
	learnset_move 37, PSYCHIC_M
	learnset_move 43, MEDITATE
	db 0

GolbatEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 10, SUPERSONIC
	learnset_move 15, BITE
	learnset_move 21, CONFUSE_RAY
	learnset_move 32, WING_ATTACK
	learnset_move 43, HAZE
	db 0

MewtwoEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 63, BARRIER
	learnset_move 66, PSYCHIC_M
	learnset_move 70, RECOVER
	learnset_move 75, MIST
	learnset_move 81, AMNESIA
	db 0

SnorlaxEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 35, BODY_SLAM
	learnset_move 41, HARDEN
	learnset_move 48, DOUBLE_EDGE
	learnset_move 56, HYPER_BEAM
	db 0

MagikarpEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 20, GYARADOS
	db 0
; Learnset
	learnset_move 15, TACKLE
	db 0

MissingNo86EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNo87EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MukEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 30, POISON_GAS
	learnset_move 33, MINIMIZE
	learnset_move 37, SLUDGE
	learnset_move 45, HARDEN
	learnset_move 53, SCREECH
	learnset_move 60, ACID_ARMOR
	db 0

MissingNo8AEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

KinglerEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 20, VICEGRIP
	learnset_move 25, GUILLOTINE
	learnset_move 34, STOMP
	learnset_move 42, CRABHAMMER
	learnset_move 49, HARDEN
	db 0

CloysterEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 50, SPIKE_CANNON
	db 0

MissingNo8CEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

ElectrodeEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 17, SONICBOOM
	learnset_move 22, SELFDESTRUCT
	learnset_move 29, LIGHT_SCREEN
	learnset_move 40, SWIFT
	learnset_move 50, EXPLOSION
	db 0

ClefableEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

WeezingEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 32, SLUDGE
	learnset_move 39, SMOKESCREEN
	learnset_move 43, SELFDESTRUCT
	learnset_move 49, HAZE
	learnset_move 53, EXPLOSION
	db 0

PersianEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 12, BITE
	learnset_move 17, PAY_DAY
	learnset_move 24, SCREECH
	learnset_move 37, FURY_SWIPES
	learnset_move 51, SLASH
	db 0

MarowakEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 25, LEER
	learnset_move 33, FOCUS_ENERGY
	learnset_move 41, THRASH
	learnset_move 48, BONEMERANG
	learnset_move 55, RAGE
	db 0

MissingNo92EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

HaunterEvosMoves:
; Evolutions
	db EVOLVE_TRADE, 1, GENGAR
	db 0
; Learnset
	learnset_move 29, HYPNOSIS
	learnset_move 38, DREAM_EATER
	db 0

AbraEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 16, KADABRA
	db 0
; Learnset
	db 0

AlakazamEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 16, CONFUSION
	learnset_move 20, DISABLE
	learnset_move 27, PSYBEAM
	learnset_move 31, RECOVER
	learnset_move 38, PSYCHIC_M
	learnset_move 42, REFLECT
	db 0

PidgeottoEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 36, PIDGEOT
	db 0
; Learnset
	learnset_move 5, SAND_ATTACK
	learnset_move 12, QUICK_ATTACK
	learnset_move 21, WHIRLWIND
	learnset_move 31, WING_ATTACK
	learnset_move 40, AGILITY
	learnset_move 49, MIRROR_MOVE
	db 0

PidgeotEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 5, SAND_ATTACK
	learnset_move 12, QUICK_ATTACK
	learnset_move 21, WHIRLWIND
	learnset_move 31, WING_ATTACK
	learnset_move 44, AGILITY
	learnset_move 54, MIRROR_MOVE
	db 0

StarmieEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

BulbasaurEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 16, IVYSAUR
	db 0
; Learnset
	learnset_move 7, LEECH_SEED
	learnset_move 13, VINE_WHIP
	learnset_move 20, POISONPOWDER
	learnset_move 27, RAZOR_LEAF
	learnset_move 34, GROWTH
	learnset_move 41, SLEEP_POWDER
	learnset_move 48, SOLARBEAM
	db 0

VenusaurEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 7, LEECH_SEED
	learnset_move 13, VINE_WHIP
	learnset_move 22, POISONPOWDER
	learnset_move 30, RAZOR_LEAF
	learnset_move 43, GROWTH
	learnset_move 55, SLEEP_POWDER
	learnset_move 65, SOLARBEAM
	db 0

TentacruelEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 7, SUPERSONIC
	learnset_move 13, WRAP
	learnset_move 18, POISON_STING
	learnset_move 22, WATER_GUN
	learnset_move 27, CONSTRICT
	learnset_move 35, BARRIER
	learnset_move 43, SCREECH
	learnset_move 50, HYDRO_PUMP
	db 0

MissingNo9CEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

GoldeenEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 33, SEAKING
	db 0
; Learnset
	learnset_move 19, SUPERSONIC
	learnset_move 24, HORN_ATTACK
	learnset_move 30, FURY_ATTACK
	learnset_move 37, WATERFALL
	learnset_move 45, HORN_DRILL
	learnset_move 54, AGILITY
	db 0

SeakingEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 19, SUPERSONIC
	learnset_move 24, HORN_ATTACK
	learnset_move 30, FURY_ATTACK
	learnset_move 39, WATERFALL
	learnset_move 48, HORN_DRILL
	learnset_move 54, AGILITY
	db 0

MissingNo9FEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNoA0EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNoA1EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNoA2EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

PonytaEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 40, RAPIDASH
	db 0
; Learnset
	learnset_move 30, TAIL_WHIP
	learnset_move 32, STOMP
	learnset_move 35, GROWL
	learnset_move 39, FIRE_SPIN
	learnset_move 43, TAKE_DOWN
	learnset_move 48, AGILITY
	db 0

RapidashEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 30, TAIL_WHIP
	learnset_move 32, STOMP
	learnset_move 35, GROWL
	learnset_move 39, FIRE_SPIN
	learnset_move 47, TAKE_DOWN
	learnset_move 55, AGILITY
	db 0

RattataEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 20, RATICATE
	db 0
; Learnset
	learnset_move 7, QUICK_ATTACK
	learnset_move 14, HYPER_FANG
	learnset_move 23, FOCUS_ENERGY
	learnset_move 34, SUPER_FANG
	db 0

RaticateEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 7, QUICK_ATTACK
	learnset_move 14, HYPER_FANG
	learnset_move 27, FOCUS_ENERGY
	learnset_move 41, SUPER_FANG
	db 0

NidorinoEvosMoves:
; Evolutions
	db EVOLVE_ITEM, MOON_STONE, 1, NIDOKING
	db 0
; Learnset
	learnset_move 8, HORN_ATTACK
	learnset_move 14, POISON_STING
	learnset_move 23, FOCUS_ENERGY
	learnset_move 32, FURY_ATTACK
	learnset_move 41, HORN_DRILL
	learnset_move 50, DOUBLE_KICK
	db 0

NidorinaEvosMoves:
; Evolutions
	db EVOLVE_ITEM, MOON_STONE, 1, NIDOQUEEN
	db 0
; Learnset
	learnset_move 8, SCRATCH
	learnset_move 14, POISON_STING
	learnset_move 23, TAIL_WHIP
	learnset_move 32, BITE
	learnset_move 41, FURY_SWIPES
	learnset_move 50, DOUBLE_KICK
	db 0

GeodudeEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 25, GRAVELER
	db 0
; Learnset
	learnset_move 11, DEFENSE_CURL
	learnset_move 16, ROCK_THROW
	learnset_move 21, SELFDESTRUCT
	learnset_move 26, HARDEN
	learnset_move 31, EARTHQUAKE
	learnset_move 36, EXPLOSION
	db 0

PorygonEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 23, PSYBEAM
	learnset_move 28, RECOVER
	learnset_move 35, AGILITY
	learnset_move 42, TRI_ATTACK
	db 0

AerodactylEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 33, SUPERSONIC
	learnset_move 38, BITE
	learnset_move 45, TAKE_DOWN
	learnset_move 54, HYPER_BEAM
	db 0

MissingNoACEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MagnemiteEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 30, MAGNETON
	db 0
; Learnset
	learnset_move 21, SONICBOOM
	learnset_move 25, THUNDERSHOCK
	learnset_move 29, SUPERSONIC
	learnset_move 35, THUNDER_WAVE
	learnset_move 41, SWIFT
	learnset_move 47, SCREECH
	db 0

MissingNoAEEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MissingNoAFEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

CharmanderEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 16, CHARMELEON
	db 0
; Learnset
	learnset_move 9, EMBER
	learnset_move 15, LEER
	learnset_move 22, RAGE
	learnset_move 30, SLASH
	learnset_move 38, FLAMETHROWER
	learnset_move 46, FIRE_SPIN
	db 0

SquirtleEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 16, WARTORTLE
	db 0
; Learnset
	learnset_move 8, BUBBLE
	learnset_move 15, WATER_GUN
	learnset_move 22, BITE
	learnset_move 28, WITHDRAW
	learnset_move 35, SKULL_BASH
	learnset_move 42, HYDRO_PUMP
	db 0

CharmeleonEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 36, CHARIZARD
	db 0
; Learnset
	learnset_move 9, EMBER
	learnset_move 15, LEER
	learnset_move 24, RAGE
	learnset_move 33, SLASH
	learnset_move 42, FLAMETHROWER
	learnset_move 56, FIRE_SPIN
	db 0

WartortleEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 36, BLASTOISE
	db 0
; Learnset
	learnset_move 8, BUBBLE
	learnset_move 15, WATER_GUN
	learnset_move 24, BITE
	learnset_move 31, WITHDRAW
	learnset_move 39, SKULL_BASH
	learnset_move 47, HYDRO_PUMP
	db 0

CharizardEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 9, EMBER
	learnset_move 15, LEER
	learnset_move 24, RAGE
	learnset_move 36, SLASH
	learnset_move 46, FLAMETHROWER
	learnset_move 55, FIRE_SPIN
	db 0

MissingNoB5EvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

FossilKabutopsEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

FossilAerodactylEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

MonGhostEvosMoves:
; Evolutions
	db 0
; Learnset
	db 0

OddishEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 21, GLOOM
	db 0
; Learnset
	learnset_move 15, POISONPOWDER
	learnset_move 17, STUN_SPORE
	learnset_move 19, SLEEP_POWDER
	learnset_move 24, ACID
	learnset_move 33, PETAL_DANCE
	learnset_move 46, SOLARBEAM
	db 0

GloomEvosMoves:
; Evolutions
	db EVOLVE_ITEM, LEAF_STONE, 1, VILEPLUME
	db 0
; Learnset
	learnset_move 15, POISONPOWDER
	learnset_move 17, STUN_SPORE
	learnset_move 19, SLEEP_POWDER
	learnset_move 28, ACID
	learnset_move 38, PETAL_DANCE
	learnset_move 52, SOLARBEAM
	db 0

VileplumeEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 15, POISONPOWDER
	learnset_move 17, STUN_SPORE
	learnset_move 19, SLEEP_POWDER
	db 0

BellsproutEvosMoves:
; Evolutions
	db EVOLVE_LEVEL, 21, WEEPINBELL
	db 0
; Learnset
	learnset_move 13, WRAP
	learnset_move 15, POISONPOWDER
	learnset_move 18, SLEEP_POWDER
	learnset_move 21, STUN_SPORE
	learnset_move 26, ACID
	learnset_move 33, RAZOR_LEAF
	learnset_move 42, SLAM
	db 0

WeepinbellEvosMoves:
; Evolutions
	db EVOLVE_ITEM, LEAF_STONE, 1, VICTREEBEL
	db 0
; Learnset
	learnset_move 13, WRAP
	learnset_move 15, POISONPOWDER
	learnset_move 18, SLEEP_POWDER
	learnset_move 23, STUN_SPORE
	learnset_move 29, ACID
	learnset_move 38, RAZOR_LEAF
	learnset_move 49, SLAM
	db 0

VictreebelEvosMoves:
; Evolutions
	db 0
; Learnset
	learnset_move 13, WRAP
	learnset_move 15, POISONPOWDER
	learnset_move 18, SLEEP_POWDER
	db 0
